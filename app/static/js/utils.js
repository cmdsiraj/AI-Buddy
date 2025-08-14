export function initTerminalInputs(root = document) {
  const inputs = root.querySelectorAll("input.t-input");
  inputs.forEach((el) => setupTerminalInput(el));
}

function setupTerminalInput(el) {
  const grow = el.classList.contains("t-input--grow");

  updateChars(el, grow);

  el.addEventListener("input", () => updateChars(el, grow));
  el.addEventListener("change", () => updateChars(el, grow));
}

function updateChars(el, grow) {
  if (!grow) return;
  const n = Math.max(1, (el.value || "").length + 1);
  el.style.setProperty("--chars", n);
}

export function focusFirstField(root = document) {
  const el =
    root.querySelector("[autofocus]") ||
    root.querySelector('input, textarea, [contenteditable="true"]');

  if (!el) return;

  el.focus({ preventScroll: true });

  if (el.setSelectionRange && typeof el.value === "string") {
    const n = el.value.length;
    el.setSelectionRange(n, n);
  }

  el.dispatchEvent(new Event("input", { bubbles: true }));
}
