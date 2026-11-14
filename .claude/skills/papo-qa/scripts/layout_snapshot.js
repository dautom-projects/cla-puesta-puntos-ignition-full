/*
 * Layout snapshot of a Perspective page, run inside the client: takes the position, size and computed styles of
 * every visible component and compares them later with the same page, to prove a change leaves a screen size
 * untouched (e.g. the tablet mode must not move anything at 1920 x 1080).
 *
 * Each component is keyed by its data-component-path (docks L[0], T[0]...; center C). For the component and its
 * first inner element it keeps the rect (x, y, width, height rounded to 0.5 px) and 14 computed properties. The
 * text is kept apart: a component whose text changed (live data, clock) is reported as "text" and its
 * position/size differences are listed under textMoved, not as layout differences.
 *
 * Snapshots live in the tab's IndexedDB (database "papoLayout"), so they survive reloads and the comparison
 * returns only the differences. The script keeps its own source in localStorage ("papoLayoutSrc"): after a
 * reload, eval(localStorage.papoLayoutSrc) loads it again without pasting the file.
 *
 * Usage (paste the file, then; every call returns a Promise):
 *   await papoLayout.take("overview-1920")      -> {name, components, viewport}
 *   await papoLayout.compare("overview-1920")   -> {name, components, missing, added, diffs, textChanged, ...}
 *   await papoLayout.list() / await papoLayout.remove("overview-1920")
 *   await papoLayout.form("take" | "compare", "ej11-0101-inicio", "Inicio")  (Template: form + each section)
 *
 * Version: 1.0.0
 *
 * Changelog:
 *   2026-11-14 | William M. | v1.0.0 - Initial version (tablet mode, phase 0)
 */
(function () {
	var PROPS = [
		"display", "color", "backgroundColor", "fontSize", "fontWeight", "fontFamily", "lineHeight",
		"borderTopWidth", "borderTopColor", "borderTopLeftRadius", "paddingTop", "paddingLeft",
		"minHeight", "overflow"
	];
	function idb() {
		return new Promise(function (resolve, reject) {
			var req = indexedDB.open("papoLayout", 1);
			req.onupgradeneeded = function () {
				req.result.createObjectStore("snaps");
			};
			req.onsuccess = function () {
				resolve(req.result);
			};
			req.onerror = function () {
				reject(req.error);
			};
		});
	}

	function store(mode, action) {
		return idb().then(function (db) {
			return new Promise(function (resolve, reject) {
				var tx = db.transaction("snaps", mode);
				var req = action(tx.objectStore("snaps"));
				tx.oncomplete = function () {
					resolve(req ? req.result : undefined);
				};
				tx.onerror = function () {
					reject(tx.error);
				};
			});
		});
	}

	function round(v) {
		return Math.round(v * 2) / 2;
	}

	function box(el) {
		var r = el.getBoundingClientRect();
		var cs = getComputedStyle(el);
		var out = [round(r.x), round(r.y), round(r.width), round(r.height)];
		for (var i = 0; i < PROPS.length; i++) {
			out.push(cs[PROPS[i]]);
		}
		return out;
	}

	function visible(el) {
		var r = el.getBoundingClientRect();
		return r.width > 0 && r.height > 0 && getComputedStyle(el).visibility !== "hidden";
	}

	function collect() {
		var snap = {};
		var els = document.querySelectorAll("[data-component]");
		for (var i = 0; i < els.length; i++) {
			var el = els[i];
			if (!visible(el)) {
				continue;
			}
			var path = el.getAttribute("data-component-path");
			var inner = el.firstElementChild;
			snap[path] = {
				t: el.getAttribute("data-component"),
				b: box(el),
				i: inner ? box(inner) : null,
				x: (el.innerText || "").replace(/\s+/g, " ").trim().slice(0, 200)
			};
		}
		return snap;
	}

	function fieldDiffs(a, b, prefix) {
		var names = ["x", "y", "width", "height"].concat(PROPS);
		var out = [];
		if (!a || !b) {
			if (a !== b) {
				out.push(prefix + "inner element");
			}
			return out;
		}
		for (var i = 0; i < names.length; i++) {
			if (a[i] !== b[i]) {
				out.push(prefix + names[i] + ": " + a[i] + " -> " + b[i]);
			}
		}
		return out;
	}

	window.papoLayout = {
		take: function (name) {
			var snap = collect();
			var data = {viewport: [innerWidth, innerHeight], url: location.pathname, snap: snap, at: new Date().toISOString()};
			return store("readwrite", function (s) {
				return s.put(data, name);
			}).then(function () {
				return {name: name, components: Object.keys(snap).length, viewport: data.viewport};
			});
		},
		compare: function (name, maxItems) {
			maxItems = maxItems || 40;
			return store("readonly", function (s) {
				return s.get(name);
			}).then(function (base) {
				return base ? diff(name, base, maxItems) : {name: name, error: "no snapshot"};
			});
		},
		list: function () {
			return store("readonly", function (s) {
				return s.getAllKeys();
			});
		},
		remove: function (name) {
			return store("readwrite", function (s) {
				return s.delete(name);
			});
		},
		// On the Template page: opens a register (e.g. "Inicio") and takes or compares one snapshot with the form as
		// it opens (<prefix>-0) and one per section opened (<prefix>-1, -2...). mode: "take" or "compare"
		form: async function (mode, prefix, register, wait) {
			wait = wait || 2500;
			var sleep = function (ms) {
				return new Promise(function (r) {
					setTimeout(r, ms);
				});
			};
			var buttons = document.querySelectorAll('[data-component="ia.input.button"]');
			var button = Array.prototype.find.call(buttons, function (e) {
				return (e.innerText || "").trim() === register && e.offsetParent !== null;
			});
			if (!button) {
				return {error: "no se encontró el botón " + register};
			}
			button.click();
			await sleep(4000);
			var out = [];
			var run = async function (name) {
				if (mode === "take") {
					out.push(await window.papoLayout.take(name));
				} else {
					var r = await window.papoLayout.compare(name, 5);
					out.push({name: name, counts: r.counts, diffs: r.diffs, missing: r.missing, added: r.added, error: r.error});
				}
			};
			var sections = document.querySelectorAll(".psc-button-questions, .psc-button-questions-2");
			// The Template keeps the form alive between visits: close any open section so -0 is always "all closed"
			for (var c = 0; c < sections.length; c++) {
				var openGroup = sections[c].nextElementSibling;
				if (openGroup && getComputedStyle(openGroup).display !== "none" && openGroup.clientHeight > 0) {
					sections[c].click();
					await sleep(wait);
				}
			}
			await run(prefix + "-0");
			for (var i = 0; i < sections.length; i++) {
				var group = sections[i].nextElementSibling;
				sections[i].click();
				await sleep(wait);
				// A section that starts open closes on the first click: open it again
				if (!group || getComputedStyle(group).display === "none" || group.clientHeight === 0) {
					sections[i].click();
					await sleep(wait);
				}
				await run(prefix + "-" + (i + 1));
			}
			return out;
		}
	};

	function diff(name, base, maxItems) {
		var now = collect();
		var res = {
			name: name, components: Object.keys(now).length, baseComponents: Object.keys(base.snap).length,
			viewport: [innerWidth, innerHeight], baseViewport: base.viewport,
			missing: [], added: [], diffs: [], textChanged: [], textMoved: []
		};
		var path;
		for (path in base.snap) {
			if (!(path in now)) {
				res.missing.push(path + " " + base.snap[path].t);
				continue;
			}
			var a = base.snap[path];
			var b = now[path];
			var d = fieldDiffs(a.b, b.b, "").concat(fieldDiffs(a.i, b.i, "inner."));
			if (a.x !== b.x) {
				res.textChanged.push(path + " " + a.t + ": \"" + a.x.slice(0, 40) + "\" -> \"" + b.x.slice(0, 40) + "\"");
				if (d.length) {
					res.textMoved.push(path + " " + d.join("; "));
				}
			} else if (d.length) {
				res.diffs.push(path + " " + a.t + " | " + d.join("; "));
			}
		}
		for (path in now) {
			if (!(path in base.snap)) {
				res.added.push(path + " " + now[path].t);
			}
		}
		res.counts = {
			missing: res.missing.length, added: res.added.length, diffs: res.diffs.length,
			textChanged: res.textChanged.length, textMoved: res.textMoved.length
		};
		["missing", "added", "diffs", "textChanged", "textMoved"].forEach(function (k) {
			res[k] = res[k].slice(0, maxItems);
		});
		return res;
	}

	return "papoLayout ready";
})();
