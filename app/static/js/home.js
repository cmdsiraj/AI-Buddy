import { focusFirstField, initTerminalInputs } from "./utils.js";

const mount = document.getElementById("app");

initTerminalInputs(mount);

document.getElementById("logout-btn").addEventListener("click", async () => {
  const resp = await fetch("/auth/logout", {
    method: "POST",
  });

  if (resp.redirected) {
    window.location.href = resp.url;
  }
});

const messagesView = document.getElementById("messages");
messagesView.scrollTo({
  top: messagesView.scrollHeight,
  behavior: "smooth",
});
console.log(messagesView.innerHTML);

requestAnimationFrame(() => focusFirstField());
