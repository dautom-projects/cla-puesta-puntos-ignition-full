"""
Shared indexing functions for map-project.py and refresh-map.py.

Version: 1.0.0

Changelog:
	2026-07-09 | William M. | v1.0.0 - Extracted from map-project.py
"""

import json
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
PROJECT_DIR = os.path.join(PROJECT_ROOT, "cla-project")

VIEWS_DIR = os.path.join(PROJECT_DIR, "com.inductiveautomation.perspective", "views")
SCRIPTS_DIR = os.path.join(PROJECT_DIR, "ignition", "script-python")
QUERIES_DIR = os.path.join(PROJECT_DIR, "ignition", "named-query")
STYLES_DIR = os.path.join(PROJECT_DIR, "com.inductiveautomation.perspective", "style-classes")

FORM_TYPE_SUFFIXES = [
	"_start", "_end", "_1h", "_2h", "_30min", "_4h", "_SKU", "_mmto",
	"_reject", "_dia", "_barcada", "_paro", "_mitad", "_input", "_output",
	"_hallazgo", "_defects", "_multi"
]

LEGACY_CUSTOM_KEYS = {"answers", "formato", "test", "flexGroupCount", "flexCount", "refreshSecond", "dsTable_v3", "dsTable_vJ", "changedRegister"}
STANDARD_CUSTOM_KEYS = {"dbConnection", "initialPapoDateTime", "registerTypeID", "insights", "user", "sign", "referencePapo"}


def classify_form(view_name):
	for suffix in FORM_TYPE_SUFFIXES:
		if view_name.endswith(suffix):
			return suffix.lstrip("_")
	return None


def extract_form_code(view_name):
	match = re.match(r"Form_([A-Z]{2}\d{2}-\d{4})", view_name)
	if match:
		return match.group(1)
	return None


def extract_area_line(rel_path):
	parts = rel_path.replace("\\", "/").split("/")
	area = None
	line = None
	if "Embedded" in parts:
		idx = parts.index("Embedded")
		if idx + 1 < len(parts):
			area = parts[idx + 1]
		if idx + 2 < len(parts) and parts[idx + 2].startswith("Linea"):
			line = parts[idx + 2]
	return area, line


def collect_papo_item_ids(obj):
	ids = []
	if isinstance(obj, dict):
		if "custom" in obj and isinstance(obj["custom"], dict):
			item = obj["custom"].get("item", {})
			if isinstance(item, dict) and "papoItemID" in item:
				ids.append(item["papoItemID"])
			base = obj["custom"].get("basePapo")
			if base is not None:
				ids.append({"basePapo": base})
		for val in obj.values():
			ids.extend(collect_papo_item_ids(val))
	elif isinstance(obj, list):
		for item in obj:
			ids.extend(collect_papo_item_ids(item))
	return ids


def index_view(view_json_path, views_base):
	try:
		with open(view_json_path, "r", encoding="utf-8") as f:
			data = json.load(f)
	except Exception:
		return None

	view_dir = os.path.dirname(view_json_path)
	rel_path = os.path.relpath(view_dir, views_base).replace("\\", "/")
	view_name = os.path.basename(view_dir)

	area, line = extract_area_line(rel_path)
	form_type = classify_form(view_name)
	form_code = extract_form_code(view_name)

	custom = data.get("custom", {})
	custom_keys = list(custom.keys()) if isinstance(custom, dict) else []

	has_startup = False
	events = data.get("events", {})
	if isinstance(events, dict):
		system = events.get("system", {})
		if isinstance(system, dict):
			has_startup = bool(system.get("onStartup"))

	register_type_id = custom.get("registerTypeID")

	sections = []
	flex_groups = []
	has_supervisor = False

	root = data.get("root", {})
	root_children = root.get("children", [])
	for child in root_children:
		name = child.get("meta", {}).get("name", "")
		if re.match(r"^Section\d+$", name):
			sections.append(name)
		elif re.match(r"^FlexContainerGroup\d+$", name):
			flex_groups.append(name)
		elif name == "FlexContainerSupervisor":
			has_supervisor = True

	root_custom = root.get("custom", {})
	root_custom_keys = list(root_custom.keys()) if isinstance(root_custom, dict) else []

	legacy_keys = [k for k in custom_keys if k in LEGACY_CUSTOM_KEYS]
	legacy_keys += [k for k in root_custom_keys if k in LEGACY_CUSTOM_KEYS]
	missing_standard = [k for k in STANDARD_CUSTOM_KEYS if k not in custom_keys]

	raw_ids = collect_papo_item_ids(root)
	papo_ids = []
	for pid in raw_ids:
		if isinstance(pid, int):
			papo_ids.append(pid)
		elif isinstance(pid, dict) and "basePapo" in pid:
			papo_ids.append("basePapo:{}".format(pid["basePapo"]))
	papo_ids = sorted(set(str(p) for p in papo_ids))

	custom_methods = []
	message_handlers = []
	scripts = root.get("scripts", {})
	for cm in scripts.get("customMethods", []):
		custom_methods.append(cm.get("name", ""))
	for mh in scripts.get("messageHandlers", []):
		message_handlers.append(mh.get("messageType", ""))

	return {
		"path": rel_path,
		"name": view_name,
		"area": area,
		"line": line,
		"type": form_type,
		"formCode": form_code,
		"sections": sections,
		"flexGroups": flex_groups,
		"hasSupervisor": has_supervisor,
		"hasOnStartup": has_startup,
		"registerTypeID": register_type_id,
		"customKeys": custom_keys,
		"legacyKeys": legacy_keys,
		"missingStandard": missing_standard,
		"papoItemIDs": papo_ids,
		"customMethods": custom_methods,
		"messageHandlers": message_handlers,
	}


def index_single_script(code_py_path, scripts_base):
	try:
		with open(code_py_path, "r", encoding="utf-8") as f:
			content = f.read()
		funcs = re.findall(r"^def\s+(\w+)\s*\(", content, re.MULTILINE)
	except Exception:
		return None

	dirpath = os.path.dirname(code_py_path)
	rel = os.path.relpath(dirpath, scripts_base).replace("\\", "/")
	parts = rel.split("/")
	module = parts[0] if len(parts) > 1 else None

	return {
		"path": rel,
		"module": module,
		"functions": funcs,
		"publicFunctions": [fn for fn in funcs if not fn.startswith("_")],
		"privateFunctions": [fn for fn in funcs if fn.startswith("_")],
	}


def index_named_queries(queries_base):
	results = []
	if not os.path.isdir(queries_base):
		return results
	for engine_dir in os.listdir(queries_base):
		engine_path = os.path.join(queries_base, engine_dir)
		if not os.path.isdir(engine_path):
			continue
		for query_dir in os.listdir(engine_path):
			query_path = os.path.join(engine_path, query_dir)
			if os.path.isdir(query_path):
				results.append({
					"path": "{}/{}".format(engine_dir, query_dir),
					"engine": engine_dir,
					"name": query_dir,
				})
	return results


def index_styles(styles_base):
	results = []
	if not os.path.isdir(styles_base):
		return results
	for dirpath, dirnames, filenames in os.walk(styles_base):
		if "style.json" in filenames:
			rel = os.path.relpath(dirpath, styles_base).replace("\\", "/")
			results.append({
				"path": rel,
				"name": os.path.basename(dirpath),
			})
	return results
