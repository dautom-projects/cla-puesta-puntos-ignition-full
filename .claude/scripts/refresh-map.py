"""
Incremental update of project-map.json based on git changes.

Detects modified, added, and deleted view.json files via git status/diff,
then updates only those entries in the existing map. Also detects changes
in scripts, named queries, and styles.

Version: 1.0.0

Changelog:
	2026-07-09 | William M. | v1.0.0 - Initial version
"""

import json
import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
MAP_PATH = os.path.join(PROJECT_ROOT, ".claude", "project-map.json")

sys.path.insert(0, SCRIPT_DIR)
from map_project_lib import index_view, index_single_script, VIEWS_DIR, SCRIPTS_DIR, QUERIES_DIR, STYLES_DIR


def git_changed_files():
	"""Get list of changed files from git (staged + unstaged + untracked), filtered to cla-project/ only."""
	result = subprocess.check_output(
		["git", "status", "--porcelain", "-u"],
		cwd=PROJECT_ROOT
	).decode("utf-8", errors="replace")

	files = {"modified": [], "deleted": []}
	for line in result.strip().split("\n"):
		if not line.strip():
			continue
		status = line[:2].strip()
		filepath = line[3:].strip().strip('"')
		# Only process files under cla-project/
		if not filepath.replace("\\", "/").startswith("cla-project/"):
			continue
		if status == "D":
			files["deleted"].append(filepath)
		else:
			files["modified"].append(filepath)
	return files


def classify_changed_file(filepath):
	"""Classify a changed file into view, script, query, style, or other."""
	normalized = filepath.replace("\\", "/")
	if normalized.endswith("view.json") and "/views/" in normalized:
		return "view"
	elif normalized.endswith("code.py") and "/script-python/" in normalized:
		return "script"
	elif "/named-query/" in normalized:
		return "query"
	elif "/style-classes/" in normalized and normalized.endswith("style.json"):
		return "style"
	return None


def get_view_rel_path(filepath):
	"""Extract the view relative path from a full filepath."""
	normalized = filepath.replace("\\", "/")
	parts = normalized.split("/views/")
	if len(parts) == 2:
		view_dir = parts[1].replace("/view.json", "")
		return view_dir
	return None


def get_script_rel_path(filepath):
	"""Extract the script relative path from a full filepath."""
	normalized = filepath.replace("\\", "/")
	parts = normalized.split("/script-python/")
	if len(parts) == 2:
		script_dir = os.path.dirname(parts[1])
		return script_dir
	return None


def main():
	if not os.path.isfile(MAP_PATH):
		print("ERROR: project-map.json not found. Run /map-project first.")
		sys.exit(1)

	with open(MAP_PATH, "r", encoding="utf-8") as f:
		project_map = json.load(f)

	changes = git_changed_files()
	all_files = changes["modified"] + changes["deleted"]

	if not all_files:
		print("No changes detected in git. Map is up to date.")
		return

	# Classify changes
	view_updates = []
	view_deletes = []
	script_updates = []
	script_deletes = []
	query_changes = False
	style_changes = False

	for filepath in changes["modified"]:
		category = classify_changed_file(filepath)
		if category == "view":
			view_updates.append(filepath)
		elif category == "script":
			script_updates.append(filepath)
		elif category == "query":
			query_changes = True
		elif category == "style":
			style_changes = True

	for filepath in changes["deleted"]:
		category = classify_changed_file(filepath)
		if category == "view":
			view_deletes.append(filepath)
		elif category == "script":
			script_deletes.append(filepath)
		elif category == "query":
			query_changes = True
		elif category == "style":
			style_changes = True

	updated = 0
	added = 0
	deleted = 0

	# Update views
	views_by_path = {v["path"]: i for i, v in enumerate(project_map["views"])}

	for filepath in view_updates:
		rel_path = get_view_rel_path(filepath)
		if rel_path is None:
			continue
		abs_path = os.path.join(PROJECT_ROOT, filepath.replace("/", os.sep))
		if not os.path.isfile(abs_path):
			abs_path = os.path.join(VIEWS_DIR, rel_path, "view.json")
		if not os.path.isfile(abs_path):
			continue

		new_entry = index_view(abs_path, VIEWS_DIR)
		if new_entry is None:
			continue

		if rel_path in views_by_path:
			project_map["views"][views_by_path[rel_path]] = new_entry
			updated += 1
			print("  UPDATED view: {}".format(rel_path))
		else:
			project_map["views"].append(new_entry)
			views_by_path[rel_path] = len(project_map["views"]) - 1
			added += 1
			print("  ADDED view: {}".format(rel_path))

	for filepath in view_deletes:
		rel_path = get_view_rel_path(filepath)
		if rel_path is not None and rel_path in views_by_path:
			idx = views_by_path[rel_path]
			project_map["views"].pop(idx)
			# Rebuild index after removal
			views_by_path = {v["path"]: i for i, v in enumerate(project_map["views"])}
			deleted += 1
			print("  DELETED view: {}".format(rel_path))

	# Update scripts
	scripts_by_path = {s["path"]: i for i, s in enumerate(project_map["scripts"])}

	for filepath in script_updates:
		rel_path = get_script_rel_path(filepath)
		if rel_path is None:
			continue
		abs_path = os.path.join(SCRIPTS_DIR, rel_path, "code.py")
		if not os.path.isfile(abs_path):
			continue
		new_entry = index_single_script(abs_path, SCRIPTS_DIR)
		if new_entry is None:
			continue
		if rel_path in scripts_by_path:
			project_map["scripts"][scripts_by_path[rel_path]] = new_entry
			updated += 1
			print("  UPDATED script: {}".format(rel_path))
		else:
			project_map["scripts"].append(new_entry)
			added += 1
			print("  ADDED script: {}".format(rel_path))

	for filepath in script_deletes:
		rel_path = get_script_rel_path(filepath)
		if rel_path is not None and rel_path in scripts_by_path:
			idx = scripts_by_path[rel_path]
			project_map["scripts"].pop(idx)
			scripts_by_path = {s["path"]: i for i, s in enumerate(project_map["scripts"])}
			deleted += 1
			print("  DELETED script: {}".format(rel_path))

	# Re-index queries and styles fully if any changed (they're small)
	if query_changes:
		from map_project_lib import index_named_queries
		project_map["namedQueries"] = index_named_queries(QUERIES_DIR)
		print("  RE-INDEXED named queries: {}".format(len(project_map["namedQueries"])))

	if style_changes:
		from map_project_lib import index_styles
		project_map["styles"] = index_styles(STYLES_DIR)
		print("  RE-INDEXED styles: {}".format(len(project_map["styles"])))

	# Update summary
	import datetime
	project_map["generated"] = datetime.datetime.now().isoformat()
	project_map["summary"]["views"] = len(project_map["views"])
	project_map["summary"]["scripts"] = len(project_map["scripts"])
	project_map["summary"]["namedQueries"] = len(project_map["namedQueries"])
	project_map["summary"]["styles"] = len(project_map["styles"])

	with open(MAP_PATH, "w", encoding="utf-8") as f:
		json.dump(project_map, f, indent=2, ensure_ascii=False)

	print("\nRefresh complete:")
	print("  Updated: {}".format(updated))
	print("  Added:   {}".format(added))
	print("  Deleted: {}".format(deleted))
	print("  Total views: {}".format(len(project_map["views"])))
	print("  Total scripts: {}".format(len(project_map["scripts"])))


if __name__ == "__main__":
	main()
