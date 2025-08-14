import { initTerminalInputs, focusFirstField } from "./utils.js";

const mount = document.getElementById("app");

initTerminalInputs(mount);
requestAnimationFrame(() => focusFirstField());
