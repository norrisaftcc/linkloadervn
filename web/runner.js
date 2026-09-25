// LinkLoader web runner. Reads dist/story.json (contract C2) and
// plays it: dialogue, narration, backgrounds, sprites, choices,
// flags/if, 4dF checks, Rill puzzles, jumps, and the story's ending.
// See docs/scene-format.md for the statement grammar this walks and
// AGENTS.md / docs/style/brand.md for the UI rules this follows.
//
// Rill evaluation comes from ./rill/rill.js (contract C1): a separate
// part of the project. This file only calls checkAnswer(cases, text).

import { checkAnswer } from "./rill/rill.js";

const SAVE_KEY = "linkloader-save-v1";
const DEFAULT_FATE = 3;
const MAX_PUZZLE_ATTEMPTS = 3;

// ---------------------------------------------------------------------------
// Seedable RNG (mulberry32) — deterministic when ?seed=N is on the URL,
// and its whole state is small enough to save/restore across reloads.

function mulberry32(seed) {
  let a = seed >>> 0;
  return function next() {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function seedFromUrl() {
  const params = new URLSearchParams(window.location.search);
  const raw = params.get("seed");
  if (raw !== null && /^-?\d+$/.test(raw)) return Number(raw) >>> 0;
  return null;
}

// ---------------------------------------------------------------------------
// localStorage save/continue. Every accessor is wrapped: a private
// window, blocked storage, or a disabled API must not break the game.

function safeLoad() {
  try {
    const raw = window.localStorage.getItem(SAVE_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

function safeSave(data) {
  try {
    window.localStorage.setItem(SAVE_KEY, JSON.stringify(data));
  } catch {
    // Ignore: play continues, it just won't resume after a reload.
  }
}

function safeClear() {
  try {
    window.localStorage.removeItem(SAVE_KEY);
  } catch {
    // Ignore.
  }
}

// ---------------------------------------------------------------------------
// The ladder: reproduces linkloader/dice.py's tier_for exactly, driven
// by data the Python build emitted (see exporter.build_ladder), so
// this file has no tier-boundary numbers of its own to drift.

function tierFor(ladder, shift) {
  for (const row of ladder.tiers) {
    if ("min_shift" in row) {
      if (shift >= row.min_shift) return row.tier;
    } else if ("shift" in row) {
      if (shift === row.shift) return row.tier;
    } else {
      return row.tier; // the catch-all row (fail)
    }
  }
  return "fail";
}

function rollDice(ladder, rng) {
  const faces = ladder.faces;
  const dice = [0, 1, 2, 3].map(() => faces[Math.floor(rng() * faces.length)]);
  return dice;
}

// ---------------------------------------------------------------------------

class Game {
  constructor(story, els) {
    this.story = story;
    this.els = els;
    this.flags = {};
    this.fate = DEFAULT_FATE;
    this.stack = [];
    this.currentLabel = story.start;
    this.rng = null;
    this.rngSeed = null;
    this.puzzleAttempts = 0;
    this.puzzleRerolled = false;
    this.hintBought = false;
    this.lexiconRowsRendered = false;
  }

  // -- boot / save ---------------------------------------------------

  boot() {
    const urlSeed = seedFromUrl();
    const saved = safeLoad();
    if (saved && urlSeed === null) {
      this.flags = saved.flags || {};
      this.fate = typeof saved.fate === "number" ? saved.fate : DEFAULT_FATE;
      this.rngSeed = typeof saved.rngSeed === "number" ? saved.rngSeed : (Date.now() >>> 0);
      this.rng = mulberry32(this.rngSeed);
      this.gotoScene(saved.label || this.story.start, { fresh: false });
      return;
    }
    this.rngSeed = urlSeed !== null ? urlSeed : (Date.now() >>> 0);
    this.rng = mulberry32(this.rngSeed);
    this.gotoScene(this.story.start, { fresh: true });
  }

  save() {
    safeSave({
      label: this.currentLabel,
      flags: this.flags,
      fate: this.fate,
      rngSeed: this.rngSeed,
    });
  }

  restart() {
    safeClear();
    this.flags = {};
    this.fate = DEFAULT_FATE;
    const urlSeed = seedFromUrl();
    this.rngSeed = urlSeed !== null ? urlSeed : (Date.now() >>> 0);
    this.rng = mulberry32(this.rngSeed);
    this.hideEnding();
    this.gotoScene(this.story.start, { fresh: true });
  }

  // -- flags / conditions ---------------------------------------------

  getFlag(name) {
    return Object.prototype.hasOwnProperty.call(this.flags, name) ? this.flags[name] : false;
  }

  evalCondition(cond) {
    if (!cond) return true;
    const value = this.getFlag(cond.flag);
    if (cond.op === "truthy") return Boolean(value);
    if (cond.op === "not") return !value;
    if (cond.op === "==") return value === cond.value;
    if (cond.op === "!=") return value !== cond.value;
    const left = typeof value === "number" ? value : 0;
    if (cond.op === ">=") return left >= cond.value;
    if (cond.op === "<=") return left <= cond.value;
    if (cond.op === ">") return left > cond.value;
    if (cond.op === "<") return left < cond.value;
    return false;
  }

  applyAssignment(a) {
    if (a.op === "=") {
      this.flags[a.flag] = a.value;
      return;
    }
    const current = typeof this.flags[a.flag] === "number" ? this.flags[a.flag] : 0;
    this.flags[a.flag] = a.op === "+=" ? current + a.value : current - a.value;
  }

  // -- scene traversal --------------------------------------------------

  gotoScene(label, { fresh } = {}) {
    const scene = this.story.scenes[label];
    if (!scene) {
      this.showLoadError(`unknown scene: ${label}`);
      return;
    }
    this.currentLabel = label;
    this.stack = [{ stmts: scene.statements, i: 0 }];
    if (fresh) {
      // A brand-new scene: drop any lingering sprites from the last one.
      this.setSprite("left", null);
      this.setSprite("center", null);
      this.setSprite("right", null);
    }
    this.save();
    this.step();
  }

  step() {
    while (true) {
      if (this.stack.length === 0) {
        this.showEnding();
        return;
      }
      const frame = this.stack[this.stack.length - 1];
      if (frame.i >= frame.stmts.length) {
        this.stack.pop();
        continue;
      }
      const stmt = frame.stmts[frame.i++];
      switch (stmt.kind) {
        case "bg":
          this.setBg(stmt.name);
          continue;
        case "show":
          this.setSprite(
            stmt.position,
            this.assetFor("sprite", stmt.sprite, stmt.expression),
            stmt.sprite
          );
          continue;
        case "hide":
          this.hideSprite(stmt.sprite);
          continue;
        case "set":
          for (const a of stmt.assignments) this.applyAssignment(a);
          continue;
        case "if": {
          const branch = this.evalCondition(stmt.condition) ? stmt.then : stmt.else;
          this.stack.push({ stmts: branch, i: 0 });
          continue;
        }
        case "line":
          this.renderDialogue(stmt);
          return;
        case "narration":
          this.renderDialogue({ speaker: null, text: stmt.text });
          return;
        case "choice":
          this.renderChoice(stmt);
          return;
        case "check":
          this.renderCheck(stmt);
          return;
        case "puzzle":
          this.renderPuzzle(stmt);
          return;
        case "jump":
          this.hideAllPanels();
          this.gotoScene(stmt.target, { fresh: true });
          return;
        default:
          console.warn("unknown statement kind", stmt.kind, stmt);
          continue;
      }
    }
  }

  resolveOutcome(outcomeLabel) {
    if (outcomeLabel) {
      this.hideAllPanels();
      this.gotoScene(outcomeLabel, { fresh: true });
    } else {
      // Falls through: keep playing the current scene from here.
      this.step();
    }
  }

  assetFor(kind, a, b) {
    const assets = this.story.assets || {};
    if (kind === "bg") return (assets.bg || {})[a] || null;
    return ((assets.sprite || {})[a] || {})[b] || null;
  }

  // -- rendering: stage --------------------------------------------------

  setBg(name) {
    const path = this.assetFor("bg", name);
    this.els.bgLayer.style.backgroundImage = path ? `url("${path}")` : "none";
  }

  setSprite(position, path, spriteId) {
    const img = this.els.sprites[position];
    if (!img) return;
    if (path) {
      img.src = path;
      img.dataset.spriteId = spriteId || "";
      img.hidden = false;
    } else {
      img.removeAttribute("src");
      delete img.dataset.spriteId;
      img.hidden = true;
    }
  }

  hideSprite(spriteId) {
    // We track sprites by screen position, not by id (the format
    // allows re-showing the same sprite in a new position, which
    // replaces it there); hiding by id hides wherever its image is
    // currently showing.
    for (const pos of ["left", "center", "right"]) {
      const img = this.els.sprites[pos];
      if (img && !img.hidden && img.dataset.spriteId === spriteId) {
        this.setSprite(pos, null);
      }
    }
  }

  // -- rendering: dialogue / narration -------------------------------

  hideAllPanels() {
    for (const el of [
      this.els.dialogueBox,
      this.els.choicesWrap,
      this.els.checkPanel,
      this.els.puzzlePanel,
      this.els.endingPanel,
    ]) {
      el.hidden = true;
    }
    this.closeLexicon();
  }

  // -- rendering: lexicon (puzzle panel) --------------------------------
  // A read-only reference panel over the puzzle panel. It never
  // touches the editor's contents (rule 6, brand.md: accretion, not
  // replacement -- the player's own work stays put).

  renderLexiconTables() {
    if (this.lexiconRowsRendered) return;
    const lexicon = this.story.lexicon || [];
    this.els.lexiconGrammarBody.innerHTML = "";
    this.els.lexiconThemeBody.innerHTML = "";
    for (const entry of lexicon) {
      const tr = document.createElement("tr");
      const word = document.createElement("td");
      word.className = "lexicon-word";
      word.textContent = entry.word;
      tr.appendChild(word);
      if (entry.kind === "grammar") {
        const scheme = document.createElement("td");
        scheme.className = "lexicon-word";
        scheme.textContent = entry.scheme || "";
        tr.appendChild(scheme);
      }
      const gloss = document.createElement("td");
      gloss.textContent = entry.gloss;
      tr.appendChild(gloss);
      const body = entry.kind === "grammar" ? this.els.lexiconGrammarBody : this.els.lexiconThemeBody;
      body.appendChild(tr);
    }
    this.lexiconRowsRendered = true;
  }

  openLexicon() {
    this.renderLexiconTables();
    this.els.lexiconPanel.hidden = false;
  }

  closeLexicon() {
    this.els.lexiconPanel.hidden = true;
  }

  renderDialogue(stmt) {
    this.hideAllPanels();
    const name = stmt.speaker ? (this.story.cast[stmt.speaker] || {}).name || stmt.speaker : "";
    this.els.speakerName.textContent = name;
    this.els.dialogueText.textContent = stmt.text;
    this.els.dialogueBox.hidden = false;
    this.awaitingAdvance = true;
  }

  advanceDialogue() {
    if (!this.awaitingAdvance) return;
    this.awaitingAdvance = false;
    this.step();
  }

  // -- rendering: choice -----------------------------------------------

  renderChoice(stmt) {
    this.hideAllPanels();
    const options = stmt.options.filter((o) => this.evalCondition(o.condition));
    this.els.choicesList.innerHTML = "";
    options.forEach((opt, idx) => {
      const li = document.createElement("li");
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "choice-btn";
      btn.innerHTML = `<span class="choice-num">${idx + 1}.</span> `;
      btn.appendChild(document.createTextNode(opt.text));
      btn.addEventListener("click", () => {
        this.hideAllPanels();
        this.gotoScene(opt.target, { fresh: true });
      });
      li.appendChild(btn);
      this.els.choicesList.appendChild(li);
    });
    this.currentChoiceButtons = Array.from(this.els.choicesList.querySelectorAll("button"));
    this.els.choicesWrap.hidden = false;
    if (this.currentChoiceButtons[0]) this.currentChoiceButtons[0].focus();
  }

  pickChoiceByNumber(n) {
    const btn = this.currentChoiceButtons && this.currentChoiceButtons[n - 1];
    if (btn) btn.click();
  }

  // -- rendering: check --------------------------------------------------

  // A check's stat value is the story flag of the same name, if it
  // holds an integer, else 0 (see docs/scene-format.md, "check", and
  // the matching rule in linkloader/player.py's `_stat_value`).
  statValueFor(stat) {
    const value = this.getFlag(stat);
    return typeof value === "number" ? value : 0;
  }

  renderCheck(stmt) {
    this.hideAllPanels();
    this.checkStmt = stmt;
    this.checkRerolled = false;
    const statValue = this.statValueFor(stmt.stat);
    this.runCheck(stmt, statValue);
    this.els.checkPanel.hidden = false;
  }

  runCheck(stmt, statValue) {
    const ladder = this.story.ladder;
    const dice = rollDice(ladder, this.rng);
    const total = dice.reduce((a, b) => a + b, 0) + statValue;
    const shift = total - stmt.difficulty;
    const tier = tierFor(ladder, shift);
    this.lastCheckResult = { dice, total, shift, tier };
    this.save();

    const signedStat = statValue >= 0 ? `+${statValue}` : String(statValue);
    this.els.checkTitle.textContent = `Check: ${stmt.stat} ${signedStat} vs ${stmt.difficulty}`;
    this.els.diceRow.innerHTML = "";
    dice.forEach((face) => {
      const span = document.createElement("span");
      span.className = "die";
      span.dataset.face = String(face);
      span.textContent = face > 0 ? "+" : face < 0 ? "−" : "0";
      this.els.diceRow.appendChild(span);
    });
    this.els.checkResult.textContent =
      `dice ${dice.join(", ")} + ${stmt.stat} ${signedStat} = ${total} vs ${stmt.difficulty} -> ${tier.toUpperCase()}`;

    this.els.checkActions.innerHTML = "";
    if (this.fate > 0 && !this.checkRerolled) {
      const rerollBtn = document.createElement("button");
      rerollBtn.type = "button";
      rerollBtn.className = "btn";
      rerollBtn.textContent = "Spend a Fate point to reroll";
      rerollBtn.addEventListener("click", () => {
        this.fate -= 1;
        this.checkRerolled = true;
        this.updateFateCounter();
        this.runCheck(stmt, statValue);
      });
      this.els.checkActions.appendChild(rerollBtn);
    }
    const continueBtn = document.createElement("button");
    continueBtn.type = "button";
    continueBtn.className = "btn btn-primary";
    continueBtn.textContent = "Continue";
    continueBtn.addEventListener("click", () => {
      this.resolveOutcome(stmt.outcomes[tier]);
    });
    this.els.checkActions.appendChild(continueBtn);
    continueBtn.focus();
  }

  // -- rendering: puzzle -------------------------------------------------

  renderPuzzle(stmt) {
    this.hideAllPanels();
    this.puzzleStmt = stmt;
    this.puzzleAttempts = 0;
    this.hintBought = false;
    const data = (this.story.puzzles || {})[stmt.id];
    if (!data) {
      // No puzzle data shipped (e.g. story references an id not yet
      // built) — fall through like the terminal player's "no checker".
      this.resolveOutcome(stmt.outcomes.lockout || null);
      return;
    }
    this.els.puzzleTitle.textContent = data.title;
    this.els.puzzlePrompt.innerHTML = data.prompt;
    this.els.puzzleEditor.value = data.starter || "";
    this.els.puzzleResults.innerHTML = "";
    this.els.puzzleHintText.hidden = true;
    this.els.puzzleHintText.textContent = "";
    this.els.puzzleHintBtn.disabled = !data.hint || this.fate <= 0;
    this.els.puzzleAttempts.textContent =
      `Attempt 1 of ${MAX_PUZZLE_ATTEMPTS}. Fate: ${this.fate}.`;
    this.closeLexicon();
    const lexicon = this.story.lexicon || [];
    this.els.puzzleLexiconBtn.hidden = lexicon.length === 0;
    this.els.puzzlePanel.hidden = false;
    this.els.puzzleEditor.focus();
  }

  puzzleCheck() {
    const stmt = this.puzzleStmt;
    const data = this.story.puzzles[stmt.id];
    const answerText = this.els.puzzleEditor.value;
    const outcome = checkAnswer(data.cases, answerText);
    this.els.puzzleResults.innerHTML = "";

    if (outcome.error) {
      const chip = document.createElement("p");
      chip.className = "error-chip";
      chip.textContent = `Rill error: ${outcome.error}`;
      this.els.puzzleResults.appendChild(chip);
    } else {
      for (const r of outcome.results) {
        const row = document.createElement("p");
        row.className = `result-row ${r.ok ? "result-pass" : "result-fail"}`;
        row.textContent = `${r.input} -> got ${r.got}, expected ${r.expected}`;
        this.els.puzzleResults.appendChild(row);
      }
    }

    if (outcome.pass) {
      this.resolveOutcome(stmt.outcomes.pass);
      return;
    }

    this.puzzleAttempts += 1;
    if (this.puzzleAttempts >= MAX_PUZZLE_ATTEMPTS) {
      const note = document.createElement("p");
      note.className = "error-chip";
      note.textContent = `Three failed checks. Locked out.`;
      this.els.puzzleResults.appendChild(note);
      this.resolveOutcome(stmt.outcomes.lockout || null);
      return;
    }
    this.els.puzzleAttempts.textContent =
      `Attempt ${this.puzzleAttempts + 1} of ${MAX_PUZZLE_ATTEMPTS}. Fate: ${this.fate}.`;
  }

  puzzleHint() {
    const data = this.story.puzzles[this.puzzleStmt.id];
    if (!data.hint || this.fate <= 0) return;
    this.fate -= 1;
    this.updateFateCounter();
    this.els.puzzleHintText.innerHTML = data.hint;
    this.els.puzzleHintText.hidden = false;
    this.els.puzzleHintBtn.disabled = true;
    this.save();
  }

  // -- ending ------------------------------------------------------------

  showEnding() {
    this.hideAllPanels();
    this.els.endingLabel.textContent = `Scene: ${this.currentLabel}`;
    this.els.endingPanel.hidden = false;
    safeClear();
  }

  hideEnding() {
    this.els.endingPanel.hidden = true;
  }

  updateFateCounter() {
    this.els.fateCount.textContent = String(this.fate);
    this.save();
  }
}

// ---------------------------------------------------------------------------
// Boot.

function collectEls() {
  const $ = (id) => document.getElementById(id);
  return {
    bgLayer: $("bg-layer"),
    sprites: { left: $("sprite-left"), center: $("sprite-center"), right: $("sprite-right") },
    dialogueBox: $("dialogue-box"),
    speakerName: $("speaker-name"),
    dialogueText: $("dialogue-text"),
    choicesWrap: $("choices-wrap"),
    choicesList: $("choices-list"),
    checkPanel: $("check-panel"),
    checkTitle: $("check-title"),
    diceRow: $("dice-row"),
    checkResult: $("check-result"),
    checkActions: $("check-actions"),
    puzzlePanel: $("puzzle-panel"),
    puzzleTitle: $("puzzle-title"),
    puzzlePrompt: $("puzzle-prompt"),
    puzzleEditor: $("puzzle-editor"),
    puzzleCheckBtn: $("puzzle-check-btn"),
    puzzleHintBtn: $("puzzle-hint-btn"),
    puzzleLexiconBtn: $("puzzle-lexicon-btn"),
    puzzleAttempts: $("puzzle-attempts"),
    puzzleResults: $("puzzle-results"),
    puzzleHintText: $("puzzle-hint-text"),
    lexiconPanel: $("lexicon-panel"),
    lexiconCloseBtn: $("lexicon-close-btn"),
    lexiconGrammarBody: $("lexicon-grammar-body"),
    lexiconThemeBody: $("lexicon-theme-body"),
    endingPanel: $("ending-panel"),
    endingLabel: $("ending-label"),
    fateCount: $("fate-count"),
    restartBtn: $("restart-btn"),
    endingRestartBtn: $("ending-restart-btn"),
    loadError: $("load-error"),
  };
}

async function main() {
  const els = collectEls();
  let story;
  try {
    const res = await fetch("./story.json");
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    story = await res.json();
  } catch (err) {
    els.loadError.hidden = false;
    els.loadError.textContent = `Could not load story.json: ${err.message}`;
    return;
  }

  const game = new Game(story, els);
  window.__linkloaderGame = game; // convenience for manual/E2E poking

  els.dialogueBox.addEventListener("click", () => game.advanceDialogue());
  els.puzzleCheckBtn.addEventListener("click", () => game.puzzleCheck());
  els.puzzleHintBtn.addEventListener("click", () => game.puzzleHint());
  els.puzzleLexiconBtn.addEventListener("click", () => game.openLexicon());
  els.lexiconCloseBtn.addEventListener("click", () => game.closeLexicon());
  els.restartBtn.addEventListener("click", () => game.restart());
  els.endingRestartBtn.addEventListener("click", () => game.restart());

  document.addEventListener("keydown", (e) => {
    const tag = document.activeElement && document.activeElement.tagName;
    if (tag === "TEXTAREA" || tag === "INPUT") return; // the editor keeps its keys

    if (e.key === " " || e.key === "Enter") {
      if (game.awaitingAdvance) {
        e.preventDefault();
        game.advanceDialogue();
      }
      return;
    }
    if (/^[1-9]$/.test(e.key) && game.currentChoiceButtons && !game.els.choicesWrap.hidden) {
      game.pickChoiceByNumber(Number(e.key));
    }
  });

  game.boot();
  game.updateFateCounter();
}

main();
