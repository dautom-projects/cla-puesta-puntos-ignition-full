"""
Generate project-map.json index for the Ignition project.

Walks the cla-project filesystem and extracts metadata from
view.json, code.py, query.sql, and style.json files into a
single searchable index.

Version: 1.1.0

Changelog:
	2026-07-09 | William M. | v1.1.0 - Refactored to use map_project_lib
	2026-07-09 | William M. | v1.0.0 - Initial version
"""

import json
import os
import sys
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
OUTPUT_PATH = os.path.join(PROJECT_ROOT, ".claude", "project-map.json")

sys.path.insert(0, SCRIPT_DIR)
from map_project_lib import (
	index_view, index_single_script, index_named_queries, index_styles,
	VIEWS_DIR, SCRIPTS_DIR, QUERIES_DIR, STYLES_DIR
)


def main():
	print("Indexing Ignition project...")
	print("  Project dir: {}".format(os.path.join(PROJECT_ROOT, "cla-project")))

	views = []
	errors = 0
	for dirpath, dirnames, filenames in os.walk(VIEWS_DIR):
		if "view.json" in filenames:
			result = index_view(os.path.join(dirpath, "view.json"), VIEWS_DIR)
			if result:
				views.append(result)
			else:
				errors += 1

	scripts = []
	for dirpath, dirnames, filenames in os.walk(SCRIPTS_DIR):
		if "code.py" in filenames:
			result = index_single_script(os.path.join(dirpath, "code.py"), SCRIPTS_DIR)
			if result:
				scripts.append(result)

	queries = index_named_queries(QUERIES_DIR)
	styles = index_styles(STYLES_DIR)

	project_map = {
		"generated": datetime.datetime.now().isoformat(),
		"project": "cla-project",
		"summary": {
			"views": len(views),
			"scripts": len(scripts),
			"namedQueries": len(queries),
			"styles": len(styles),
			"errors": errors,
		},
		"views": views,
		"scripts": scripts,
		"namedQueries": queries,
		"styles": styles,
	}

	os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
	with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
		json.dump(project_map, f, indent=2, ensure_ascii=False)

	print("\nDone!")
	print("  Views:         {}".format(len(views)))
	print("  Scripts:       {}".format(len(scripts)))
	print("  Named Queries: {}".format(len(queries)))
	print("  Styles:        {}".format(len(styles)))
	if errors:
		print("  Errors:        {}".format(errors))
	print("\n  Output: {}".format(OUTPUT_PATH))


if __name__ == "__main__":
	main()
