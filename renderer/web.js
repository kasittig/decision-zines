(() => {
  "use strict";
  const root = document.querySelector("[data-edition]");
  const screens = [...document.querySelectorAll(".screen")];
  const previous = document.querySelector("[data-previous]");
  const next = document.querySelector("[data-next]");
  const counter = document.querySelector("[data-counter]");
  const status = document.querySelector("[data-status]");
  const trail = [...document.querySelectorAll("[data-trail-step]")];
  const trailContents = document.querySelector(".trail__contents");
  const storageKey = `zine:${root.dataset.edition}:progress`;
  let state = { index: 0, unlocked: 0, choices: {} };

  if (trailContents && window.matchMedia("(max-width: 720px)").matches) {
    trailContents.removeAttribute("open");
  }

  try {
    const saved = JSON.parse(localStorage.getItem(storageKey));
    if (saved && Number.isInteger(saved.index) && saved.choices) state = saved;
  } catch (_) {}
  state.index = Math.max(0, Math.min(state.index, screens.length - 1));
  state.unlocked = Math.max(state.index, Math.min(state.unlocked || 0, screens.length - 1));

  function save() { try { localStorage.setItem(storageKey, JSON.stringify(state)); } catch (_) {} }
  function isLocked(index) { return index > state.unlocked; }
  function announce(message) { status.textContent = message; }
  function updateResponseRecaps() {
    document.querySelectorAll("[data-response-recap]").forEach(recap => {
      const choice = state.choices[recap.dataset.responseRecap];
      recap.hidden = !choice;
      if (!choice) return;
      recap.querySelector("[data-response-label]").textContent = `${choice.label}.`;
      recap.querySelector("[data-response-text]").textContent = choice.text;
    });
  }
  function show(index, focus = true) {
    if (index < 0 || index >= screens.length || isLocked(index)) return;
    state.index = index;
    screens.forEach((screen, i) => {
      const active = i === index;
      screen.classList.toggle("is-active", active);
      screen.hidden = !active;
      screen.setAttribute("aria-hidden", String(!active));
      if (active && focus) screen.focus({ preventScroll: true });
    });
    trail.forEach((step, i) => step.dataset.state = i < index ? "done" : i === index ? "current" : "future");
    previous.disabled = index === 0;
    const needsCommit = screens[index].dataset.decision && isLocked(index + 1);
    next.disabled = index === screens.length - 1 || Boolean(needsCommit);
    next.textContent = index === screens.length - 1 ? "Finished" : "Next";
    counter.textContent = `${index + 1} / ${screens.length}`;
    updateResponseRecaps();
    save();
    window.scrollTo({ top: 0, behavior: "instant" });
  }

  document.querySelectorAll("[data-decision]").forEach(screen => {
    const id = screen.dataset.decision;
    const radios = [...screen.querySelectorAll('input[type="radio"]')];
    const commit = screen.querySelector("[data-commit]");
    const committed = screen.querySelector("[data-committed]");
    const saved = state.choices[id];
    if (saved) {
      const selected = radios.find(radio => radio.value === saved.label);
      if (selected) selected.checked = true;
      commit.textContent = "Update response";
      commit.disabled = true;
      committed.hidden = false;
      committed.textContent = `Committed: ${saved.label}`;
    }
    radios.forEach(radio => radio.addEventListener("change", () => {
      commit.disabled = Boolean(state.choices[id] && radio.value === state.choices[id].label);
    }));
    commit.addEventListener("click", () => {
      const selected = radios.find(radio => radio.checked);
      if (!selected) return;
      state.choices[id] = { label: selected.value, text: selected.dataset.text };
      commit.textContent = "Update response";
      commit.disabled = true;
      committed.hidden = false;
      committed.textContent = `Committed: ${selected.value}`;
      const screenIndex = screens.indexOf(screen);
      state.unlocked = Math.max(state.unlocked, screenIndex + 1);
      announce(`Response ${selected.value} submitted. Showing what the record says.`);
      show(screenIndex + 1);
    });
  });

  previous.addEventListener("click", () => show(state.index - 1));
  next.addEventListener("click", () => {
    if (state.index === state.unlocked && state.unlocked < screens.length - 1) state.unlocked += 1;
    show(state.index + 1);
  });
  document.addEventListener("keydown", event => {
    if (event.target.matches("input,button") || event.altKey || event.metaKey || event.ctrlKey) return;
    if (event.key === "ArrowLeft") previous.click();
    if (event.key === "ArrowRight") next.click();
  });
  const restart = document.querySelector("[data-restart]");
  if (restart) restart.addEventListener("click", () => {
    try { localStorage.removeItem(storageKey); } catch (_) {}
    window.location.reload();
  });
  show(state.index, false);
})();
