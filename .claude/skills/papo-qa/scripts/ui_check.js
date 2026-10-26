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
 * numbers "7", texts "QA"; dropdowns and dates untouched) and, with save: true, saves through the
 * standard confirmation (Guardar -> Si). The same values on the original and on the pilot must give
 * the same DataAnswer (papo_qa.py --compare-db PILOT ORIGINAL --exact).
 *
 * Version: 1.1.0
 *
 * Changelog:
 *   2026-10-25 | William M. | v1.0.0 - Initial version
 *   2026-10-26 | William M. | v1.1.0 - Fields scrolled into view before the click; jumps over 100 px; numeric
 *     fields through their edit mode; form root found by its sections; visible register button only
 *
 * Usage (browser console or a javascript tool on the Template page):
 *   <contents of this file>; await papoUiCheck({register: "Inicio", fill: true, save: false})
 *
 * Returns:
 *   {form, register, sections: [{name, rows, problems, warnings}], problems, warnings, saved}
 */
window.papoUiCheck = async function (opts) {
	const o = Object.assign({register: "Inicio", fill: true, save: false, wait: 2500}, opts || {});
	const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
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
		input.dispatchEvent(new FocusEvent("focusin", {bubbles: true}));
		setter.call(input, value);
		input.dispatchEvent(new Event("input", {bubbles: true}));
		input.dispatchEvent(new Event("change", {bubbles: true}));
		input.dispatchEvent(new KeyboardEvent("keyup", {key: "Enter", keyCode: 13, bubbles: true}));
		input.dispatchEvent(new FocusEvent("focusout", {bubbles: true}));
		input.dispatchEvent(new FocusEvent("blur"));
		await sleep(300);
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
	await sleep(4000);
	// The form root holds the Section buttons (original or standard form)
	const form = (document.querySelector(".psc-button-questions, .psc-button-questions-2") || {}).parentElement;
	if (!form) {
		report.problems.push("no se encontró el formulario");
		return report;
	}
	report.standard = form.classList.contains("psc-PAPO/Form");
	const sections = all(".psc-button-questions, .psc-button-questions-2", form);

	for (const section of sections) {
		const name = text(section);
		const s = {name, rows: 0, problems: [], warnings: []};
		const group = section.nextElementSibling;
		const isOpen = () => group && getComputedStyle(group).display !== "none" && group.clientHeight > 0;
		section.click();
		await sleep(o.wait);
		// A section that starts open closes on the first click: open it again
		if (!isOpen()) {
			section.click();
			await sleep(o.wait);
		}
		if (!isOpen()) {
			s.warnings.push("la sección no abrió o está vacía");
			report.sections.push(s);
			continue;
		}
		const box = group.getBoundingClientRect();
		const kids = [...group.children];
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
			for (const field of all('[data-component="ia.input.text-field"] input, input[data-component="ia.input.text-field"]', group)) {
				if (!field.disabled && !field.readOnly) {
					await setInput(field, "QA");
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
	// Observaciones (outside the sections)
	if (o.fill) {
		const obs = all('[data-component="ia.input.text-field"]', form).filter((t) => !t.closest(".psc-button-questions, .psc-button-questions-2")).pop();
		const input = obs && (obs.tagName === "INPUT" ? obs : obs.querySelector("input"));
		if (input) {
			await setInput(input, "QA");
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
