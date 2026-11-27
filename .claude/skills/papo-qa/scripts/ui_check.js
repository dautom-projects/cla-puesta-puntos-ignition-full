/*
 * UI and save check of a PAPO form, run inside the Perspective client (Digitalizacion_Template page).
 *
 * Opens one register (e.g. "Inicio"), walks every section and checks what the operator sees:
 *   - the open section fits its rows (nothing cut at the end, no row squeezed below its height)
 *   - no text cut inside its label, no checkbox without text, repeated questions reported
 *   - option groups in one line, fields inside the section width
 *   - clicking a checkbox or radio does not scroll the page
 *   - values survive closing and reopening the section
 * Then fills every field with the same fixed values (checkboxes checked, last option of each group,
 * numbers "7", texts "QA", time pickers 08:15 (the seconds stay those of the opening), last option of each
 * dropdown, the supervisor included when the session user source has supervisors) and,
 * with save: true, saves through the standard confirmation (Guardar -> Si). The same values on the original
 * and on the pilot must give the same DataAnswer (papo_qa.py --compare-db PILOT ORIGINAL --exact).
 * Each section also reports its opening time (openMs) and the range color of its numerics (numericColors),
 * to compare between the two forms. Run it at 1920 x 1080, the size the application is built for.
 * With minTouchPx (e.g. 40) it also reports, per section, the controls shorter than that (tablet mode).
 *
 * papoUiAudit(list, opts) walks many PAPOs in the background without reloading the page (in-app navigation):
 * per PAPO it opens every register button and runs papoUiCheck with fill/save off. Progress and compact results
 * in window.papoAuditState (set papoAuditState.stop = true to stop it); nothing is saved.
 *
 * Version: 1.4.0
 *
 * Changelog:
 *   2026-10-25 | William M. | v1.0.0 - Initial version
 *   2026-10-26 | William M. | v1.1.0 - Fields scrolled into view before the click; jumps over 100 px; numeric
 *     fields through their edit mode; form root found by its sections; visible register button only
 *   2026-10-26 | William M. | v1.2.0 - Text fields and Observaciones committed with Enter key down (they kept
 *     the old text); a text that does not stay is reported
 *   2026-10-26 | William M. | v1.3.0 - Dropdowns (a warning when there is no option to choose), time pickers
 *     at a fixed time, section opening time and numeric range colors
 *   2026-10-26 | William M. | v1.3.1 - Hidden rows (display none) are not reported as squeezed nor as the end
 *   2026-10-26 | William M. | v1.3.2 - Forms without sections (an _end with only Observaciones) are found by their
 *     Guardar button
 *   2026-11-14 | William M. | v1.4.0 - minTouchPx (controls shorter than the touch minimum, tablet mode) and
 *     papoUiAudit (many PAPOs in one run, no fill, no save); waits keep their pace in a background page
 *
 * Usage (browser console or a javascript tool on the Template page):
 *   <contents of this file>; await papoUiCheck({register: "Inicio", fill: true, save: false})
 *
 * Returns:
 *   {form, register, sections: [{name, rows, openMs, numericColors, problems, warnings}], problems, warnings, saved}
 */
// Sleep that keeps its pace when the page is in the background (hidden tabs run setTimeout at most once per second):
// a MessageChannel loop instead of a timer while the document is hidden
window.papoSleep = (ms) => {
	if (!document.hidden) {
		return new Promise((r) => setTimeout(r, ms));
	}
	return new Promise((resolve) => {
		const end = performance.now() + ms;
		const ch = new MessageChannel();
		ch.port1.onmessage = () => {
			if (performance.now() >= end) {
				ch.port1.close();
				resolve();
			} else {
				ch.port2.postMessage(0);
			}
		};
		ch.port2.postMessage(0);
	});
};

window.papoUiCheck = async function (opts) {
	const o = Object.assign({register: "Inicio", fill: true, save: false, wait: 2500, openWait: 4000, time: ["08", "15"], minTouchPx: 0}, opts || {});
	const sleep = window.papoSleep;
	const all = (sel, root) => [...(root || document).querySelectorAll(sel)];
	const text = (e) => (e && e.innerText || "").trim();
	const report = {form: document.title, register: o.register, sections: [], problems: [], warnings: [], saved: false};
	// Page jump: the largest scroll change of the containers that scroll (small moves that bring the
	// clicked field into view are normal; the bug was a jump of hundreds of px to a blank area)
	const JUMP = 100;
	const scrollState = () => new Map(all("*").filter((e) => e.scrollTop > 0 || e.scrollHeight > e.clientHeight + 1).map((e) => [e, e.scrollTop]));
	const jump = (before) => Math.max(0, ...[...before].map(([e, top]) => Math.abs(e.scrollTop - top)));

	// React-controlled inputs: set through the native setter so Perspective sees the change, then Enter and
	// focus out (dispatched: a page in the background does not fire focus events for focus()/blur())
	const setInput = async (input, value) => {
		const setter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, "value").set;
		const enter = {key: "Enter", code: "Enter", keyCode: 13, which: 13, bubbles: true};
		input.focus();
		input.dispatchEvent(new FocusEvent("focusin", {bubbles: true}));
		setter.call(input, value);
		input.dispatchEvent(new Event("input", {bubbles: true}));
		input.dispatchEvent(new Event("change", {bubbles: true}));
		// The text field commits on Enter key down; a blur without it puts the old text back
		input.dispatchEvent(new KeyboardEvent("keydown", enter));
		input.dispatchEvent(new KeyboardEvent("keyup", enter));
		await sleep(600);
		input.blur();
		input.dispatchEvent(new FocusEvent("focusout", {bubbles: true}));
		input.dispatchEvent(new FocusEvent("blur"));
		await sleep(300);
	};
	// Dropdowns: the option list opens only with a real click, so the choice is written to the component props
	// the way the dropdown does when an option is clicked. Options added in the browser do not count: the
	// gateway keeps its own list and the answer stays empty. Returns null when there is no option to choose
	// (e.g. no supervisors in the session user source)
	const pickDropdown = async (dd) => {
		const store = (dd[Object.keys(dd).find((k) => k.startsWith("__reactEventHandlers"))] || {}).store;
		if (!store) {
			return false;
		}
		const options = store.props.read("options") || [];
		const choice = [...options].reverse().find((op) => op.value !== "" && op.value !== null);
		if (!choice) {
			return null;
		}
		store.props.write("value", choice.value);
		await sleep(800);
		return store.props.read("value") === choice.value;
	};
	// Time pickers: hours and minutes to a fixed time, so two saves give the same answer
	const setTime = async (picker) => {
		const hours = picker.querySelector("input.hours");
		const minutes = picker.querySelector("input.minutes");
		if (!hours || !minutes || hours.disabled) {
			return false;
		}
		await setInput(hours, o.time[0]);
		await setInput(minutes, o.time[1]);
		return hours.value === o.time[0] && minutes.value === o.time[1];
	};
	// Numeric entry field: a read-only input that turns into an editable one on mouse down / focus
	const setNumeric = async (field, value) => {
		const shown = field.querySelector("input");
		if (!shown || shown.disabled) {
			return false;
		}
		["mousedown", "mouseup"].forEach((t) => shown.dispatchEvent(new MouseEvent(t, {bubbles: true, button: 0})));
		shown.dispatchEvent(new FocusEvent("focus"));
		shown.dispatchEvent(new FocusEvent("focusin", {bubbles: true}));
		await sleep(600);
		const editable = field.querySelector("input:not([readonly])");
		if (!editable) {
			return false;
		}
		await setInput(editable, value);
		return field.querySelector("input").value === value;
	};

	// Visible buttons only: the Template also has a hidden repeater with the same labels
	const button = all('[data-component="ia.input.button"]').find((e) => text(e) === o.register && e.offsetParent !== null);
	if (!button) {
		report.problems.push("no se encontró el botón " + o.register);
		return report;
	}
	button.click();
	await sleep(o.openWait);
	// The form root holds the Section buttons (original or standard form)
	let form = (document.querySelector(".psc-button-questions, .psc-button-questions-2") || {}).parentElement;
	if (!form) {
		// A form without sections (e.g. an _end with only Observaciones): the container of Guardar and the text field
		let node = all('[data-component="ia.input.button"]').find((e) => text(e) === "Guardar" && e.offsetParent !== null);
		while (node && !node.querySelector('[data-component="ia.input.text-field"]')) {
			node = node.parentElement;
		}
		form = node;
	}
	if (!form) {
		report.problems.push("no se encontró el formulario");
		return report;
	}
	report.standard = form.classList.contains("psc-PAPO/Form") || !!form.closest(".psc-PAPO\\/Form");
	const sections = all(".psc-button-questions, .psc-button-questions-2", form);

	for (const section of sections) {
		const name = text(section);
		const s = {name, rows: 0, problems: [], warnings: []};
		const group = section.nextElementSibling;
		const isOpen = () => group && getComputedStyle(group).display !== "none" && group.clientHeight > 0;
		// Opening time: from the click until the open section stops changing (rendered inputs and labels)
		const open = async () => {
			const start = performance.now();
			let count = -1, changed = start;
			section.click();
			while (performance.now() - start < o.wait) {
				await sleep(50);
				const now = isOpen() ? group.querySelectorAll("input, label").length + group.clientHeight : -1;
				if (now !== count) {
					count = now;
					changed = performance.now();
				}
			}
			return Math.round(changed - start);
		};
		s.openMs = await open();
		// A section that starts open closes on the first click: open it again
		if (!isOpen()) {
			s.openMs = await open();
		}
		if (!isOpen()) {
			s.warnings.push("la sección no abrió o está vacía");
			report.sections.push(s);
			continue;
		}
		const box = group.getBoundingClientRect();
		// Hidden rows (display none) take no space: they are neither squeezed nor the end of the section
		const kids = [...group.children].filter((k) => getComputedStyle(k).display !== "none");
		s.rows = kids.length;
		// Fit: the last row ends inside the open section and no row is squeezed below its basis
		const last = kids[kids.length - 1];
		if (last && last.getBoundingClientRect().bottom - box.top > group.clientHeight + 2) {
			s.problems.push("el final de la sección queda cortado");
		}
		const squeezed = kids.filter((k) => {
			const m = (k.getAttribute("style") || "").match(/flex: \d+ \d+ ([\d.]+)px/);
			return m && k.offsetHeight < parseFloat(m[1]) - 2;
		});
		if (squeezed.length) {
			s.problems.push(squeezed.length + " filas comprimidas por debajo de su alto");
		}
		// Texts: cut labels, checkboxes without text, repeated questions
		all('[data-component="ia.display.label"]', group).forEach((l) => {
			if (l.offsetParent && text(l) && (l.scrollHeight > l.clientHeight + 3)) {
				s.warnings.push("texto cortado: " + text(l).slice(0, 50));
			}
		});
		const boxes = all('[data-component="ia.input.checkbox"]', group);
		const seen = {};
		boxes.forEach((b) => {
			const t = text(b);
			if (!t) {
				s.problems.push("checkbox sin texto");
			} else if (t.length > 2) {
				seen[t] = (seen[t] || 0) + 1;
			}
		});
		Object.keys(seen).filter((t) => seen[t] > 1).forEach((t) => s.warnings.push("pregunta repetida x" + seen[t] + ": " + t.slice(0, 50)));
		// Layout: option groups in one line, inputs inside the section
		all('[data-component="ia.input.radio-group"]', group).forEach((g) => {
			const tops = new Set(all(".ia_radioGroupComponent_radioWrapper", g).map((w) => Math.round(w.getBoundingClientRect().top)));
			if (tops.size > 1) {
				s.problems.push("opciones en varias líneas");
			}
		});
		all("input", group).forEach((i) => {
			const r = i.getBoundingClientRect();
			if (r.width && r.right > box.right + 2) {
				s.problems.push("campo fuera de la sección");
			}
		});
		// Touch targets: controls shorter than the minimum (the whole checkbox component is its hit area)
		if (o.minTouchPx) {
			const kinds = {"ia.input.checkbox": "checkbox", "ia.input.numeric-entry-field": "numérico", "ia.input.text-field": "texto",
				"ia.input.dropdown": "dropdown", "ia.input.date-time-input": "fecha", "ia.input.radio-group": "opción"};
			const small = {};
			Object.keys(kinds).forEach((k) => all('[data-component="' + k + '"]', group).forEach((c) => {
				const h = c.getBoundingClientRect().height;
				if (c.offsetParent && h > 0 && h < o.minTouchPx) {
					small[kinds[k]] = (small[kinds[k]] || 0) + 1;
				}
			}));
			const parts = Object.keys(small).map((k) => k + " x" + small[k]);
			if (parts.length) {
				s.warnings.push("controles de menos de " + o.minTouchPx + " px: " + parts.join(", "));
			}
		}

		if (o.fill) {
			// Checkboxes: check every unchecked one; the page must not move
			for (const b of boxes) {
				const input = b.querySelector("input");
				if (!input || input.disabled || input.checked) {
					continue;
				}
				// Like a person: the field is in view before the click
				b.scrollIntoView({block: "center"});
				await sleep(100);
				const before = scrollState();
				(b.querySelector("label") || input).click();
				await sleep(200);
				if (jump(before) > JUMP) {
					s.problems.push("la página saltó " + Math.round(jump(before)) + " px al marcar: " + text(b).slice(0, 40));
				}
				if (!input.checked) {
					s.problems.push("no quedó marcado: " + text(b).slice(0, 40));
				}
			}
			// Option groups: the last option (a native group of checkboxes ends with the last one checked too)
			for (const g of all('[data-component="ia.input.radio-group"]', group)) {
				const radios = all("label.ia_radio", g);
				if (!radios.length) {
					continue;
				}
				g.scrollIntoView({block: "center"});
				await sleep(100);
				const before = scrollState();
				radios[radios.length - 1].click();
				await sleep(300);
				if (jump(before) > JUMP) {
					s.problems.push("la página saltó " + Math.round(jump(before)) + " px al elegir una opción");
				}
				if (!radios[radios.length - 1].innerHTML.includes("radio_button_checked") && !radios[radios.length - 1].querySelector(".ia_radio__selectedIcon")) {
					s.problems.push("la opción no quedó elegida");
				}
			}
			// Numeric and text inputs
			for (const field of all('[data-component="ia.input.numeric-entry-field"]', group)) {
				if (!(await setNumeric(field, "7")) && !(field.querySelector("input") || {}).disabled) {
					s.problems.push("no se pudo escribir en un numérico");
				}
			}
			// Range color of each numeric after the fill (out of range in red): the same list on both forms
			await sleep(800);
			s.numericColors = all('[data-component="ia.input.numeric-entry-field"]', group).map((field) => {
				const input = field.querySelector("input");
				const style = getComputedStyle(input || field);
				return [input && input.value, style.color, style.backgroundColor, style.borderColor].join(" | ");
			});
			for (const picker of all('[data-component="ia.input.date-time-input"]', group)) {
				if (!(await setTime(picker))) {
					s.problems.push("no se pudo fijar la hora");
				}
			}
			for (const dd of all('[data-component="ia.input.dropdown"]', group)) {
				const picked = await pickDropdown(dd);
				if (picked === null) {
					s.warnings.push("dropdown sin opciones para elegir");
				} else if (!picked) {
					s.problems.push("no se pudo elegir en un dropdown");
				}
			}
			for (const field of all('[data-component="ia.input.text-field"] input, input[data-component="ia.input.text-field"]', group)) {
				if (!field.disabled && !field.readOnly) {
					await setInput(field, "QA");
					if (field.value !== "QA") {
						s.problems.push("no se pudo escribir en un campo de texto");
					}
				}
			}
			// Close and reopen: values must survive
			const checked = boxes.filter((b) => (b.querySelector("input") || {}).checked).length;
			section.click();
			await sleep(1000);
			section.click();
			await sleep(o.wait);
			const after = all('[data-component="ia.input.checkbox"]', section.nextElementSibling).filter((b) => (b.querySelector("input") || {}).checked).length;
			if (after !== checked) {
				s.problems.push("al cerrar y reabrir: " + checked + " marcados antes, " + after + " después");
			}
		}
		section.click();
		await sleep(800);
		report.sections.push(s);
	}
	// Supervisor dropdown and Observaciones (outside the sections)
	if (o.fill) {
		for (const dd of all('[data-component="ia.input.dropdown"]', form).filter((d) => !sections.some((sec) => sec.nextElementSibling && sec.nextElementSibling.contains(d)))) {
			const picked = await pickDropdown(dd);
			if (picked === null) {
				report.warnings.push("supervisor sin opciones (el user source de la sesión no tiene supervisores)");
			} else if (!picked) {
				report.problems.push("no se pudo elegir el supervisor");
			}
		}
		const obs = all('[data-component="ia.input.text-field"]', form).filter((t) => !t.closest(".psc-button-questions, .psc-button-questions-2")).pop();
		const input = obs && (obs.tagName === "INPUT" ? obs : obs.querySelector("input"));
		if (input) {
			await setInput(input, "QA");
			if (input.value !== "QA") {
				report.problems.push("no se pudo escribir en Observaciones");
			}
		}
	}
	report.sections.forEach((s) => {
		s.problems.forEach((p) => report.problems.push(s.name + ": " + p));
		s.warnings.forEach((w) => report.warnings.push(s.name + ": " + w));
	});
	if (o.save) {
		const save = all('[data-component="ia.input.button"]', form).find((e) => text(e) === "Guardar");
		if (!save) {
			report.problems.push("no se encontró Guardar");
			return report;
		}
		save.click();
		await sleep(2500);
		const yes = all('[data-component="ia.input.button"], button').find((e) => text(e) === "Si");
		if (!yes) {
			report.problems.push("no apareció la confirmación");
			return report;
		}
		yes.click();
		await sleep(4000);
		report.saved = true;
	}
	return report;
};

// Audit of many PAPOs at the current window size: list = [{ref, url}] (url = Template path of one station).
// Runs in the background; poll window.papoAuditState ({running, done, total, current, results}).
window.papoUiAudit = function (list, opts) {
	const o = Object.assign({wait: 1500, openWait: 4000, navWait: 5000, minTouchPx: 40}, opts || {});
	const sleep = window.papoSleep;
	const state = window.papoAuditState = {running: true, done: 0, total: list.length, current: null, results: [], size: [innerWidth, innerHeight]};
	(async () => {
		for (const item of list) {
			if (state.stop) {
				break;
			}
			state.current = item.ref;
			const entry = {ref: item.ref, registers: {}};
			try {
				history.pushState({}, "", item.url);
				dispatchEvent(new PopStateEvent("popstate", {state: {}}));
				await sleep(o.navWait);
				const regs = [...document.querySelectorAll('[data-component="ia.display.flex-repeater"] [data-component="ia.input.button"]')]
					.filter((e) => e.offsetParent !== null).map((e) => e.innerText.trim());
				for (const reg of regs) {
					if (state.stop) {
						break;
					}
					const r = await window.papoUiCheck({register: reg, fill: false, save: false, wait: o.wait, openWait: o.openWait, minTouchPx: o.minTouchPx});
					entry.registers[reg] = {form: r.form, sections: r.sections.length, problems: r.problems, warnings: r.warnings};
				}
			} catch (e) {
				entry.error = String(e);
			}
			state.results.push(entry);
			state.done++;
		}
		state.running = false;
		state.current = null;
	})();
	return "audit started: " + list.length + " PAPOs";
};

// Markdown summary of papoUiAudit results: one row per PAPO and register with the counts that matter for a screen
// size (cut texts, squeezed rows or cut section end, fields outside the section, small controls, others)
window.papoAuditMarkdown = function (results) {
	const rows = [];
	const total = {forms: 0, cut: 0, squeezed: 0, outside: 0, small: 0, formsWithIssues: 0};
	for (const r of results) {
		if (r.error) {
			rows.push("| " + r.ref + " | — | error: " + r.error.slice(0, 60) + " | | | | |");
			continue;
		}
		for (const [reg, v] of Object.entries(r.registers)) {
			const all = v.problems.concat(v.warnings);
			const cut = all.filter((t) => t.includes("texto cortado")).length;
			const squeezed = all.filter((t) => t.includes("filas comprimidas") || t.includes("queda cortado")).length;
			const outside = all.filter((t) => t.includes("campo fuera")).length;
			let small = 0;
			all.filter((t) => t.includes("controles de menos")).forEach((t) => (t.match(/x(\d+)/g) || []).forEach((m) => (small += parseInt(m.slice(1), 10))));
			const other = all.filter((t) => !/texto cortado|filas comprimidas|queda cortado|campo fuera|controles de menos|pregunta repetida/.test(t));
			total.forms++;
			total.cut += cut;
			total.squeezed += squeezed;
			total.outside += outside;
			total.small += small;
			if (cut || squeezed || outside) {
				total.formsWithIssues++;
			}
			rows.push("| " + r.ref + " | " + reg + " | " + v.sections + " | " + (cut || "") + " | " + (squeezed || "") + " | " + (outside || "") + " | " + (small || "") + " | " + other.map((t) => t.replace(/\|/g, "/")).join("; ").slice(0, 120) + " |");
		}
	}
	return {total, table: "| PAPO | Registro | Secciones | Textos cortados | Filas apretadas / final cortado | Campos fuera | Controles < 40 px | Otros |\n|---|---|---|---|---|---|---|---|\n" + rows.join("\n")};
};
