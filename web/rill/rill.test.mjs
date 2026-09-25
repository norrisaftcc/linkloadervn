// web/rill/rill.test.mjs — parity and behavior tests for rill.js.
//
// Run with: node --test web/rill/
//
// Covers, per the rill-js task contract:
//   1. Every entry in puzzles/cases.json prelude_cases and every puzzle
//      case, run through evaluate(), matches the expected chibi output.
//   2. For each puzzle: checkAnswer(cases, answer.rill) passes, every
//      wrong/*.rill fails, and starter.rill fails.
//   3. Cross-check with chibi itself via puzzles/check/run.sh for every
//      answer and wrong file: JS pass/fail must equal chibi pass/fail.
//   4. A looping answer fails with "ran too long" in under 5s.
//   5. Forms outside the Rill subset raise RillError.

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync, readdirSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { evaluate, makeEnv, checkAnswer, RillError } from "./rill.js";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = path.resolve(HERE, "..", "..");
const PUZZLES_DIR = path.join(REPO_ROOT, "puzzles");

const cases = JSON.parse(
  readFileSync(path.join(PUZZLES_DIR, "cases.json"), "utf8")
);

function readText(...parts) {
  return readFileSync(path.join(...parts), "utf8");
}

// ---------------------------------------------------------------------
// 1. prelude_cases and puzzle cases via evaluate()
// ---------------------------------------------------------------------

test("prelude_cases match chibi's expected output", () => {
  for (const c of cases.prelude_cases) {
    if (c.expected === "error") {
      assert.throws(
        () => evaluate(c.input, makeEnv()),
        RillError,
        `expected ${c.input} to throw`
      );
    } else {
      const got = evaluate(c.input, makeEnv());
      assert.equal(got, c.expected, `input: ${c.input}`);
    }
  }
});

test("puzzle cases (loaded with their own answer.rill) match chibi", () => {
  for (const [id, puzzleCases] of Object.entries(cases.puzzles)) {
    const answerText = readText(PUZZLES_DIR, id, "answer.rill");
    const result = checkAnswer(puzzleCases, answerText);
    assert.equal(
      result.pass,
      true,
      `puzzle ${id} reference answer should pass all cases: ${JSON.stringify(
        result.results
      )}`
    );
    for (const r of result.results) {
      assert.equal(r.ok, true, `puzzle ${id} case ${r.input}`);
    }
  }
});

// ---------------------------------------------------------------------
// 2. checkAnswer against answer/wrong/starter files, per puzzle
// ---------------------------------------------------------------------

function puzzleIds() {
  return readdirSync(PUZZLES_DIR, { withFileTypes: true })
    .filter((d) => d.isDirectory() && d.name !== "rill" && d.name !== "check")
    .map((d) => d.name);
}

for (const id of puzzleIds()) {
  const puzzleCases = cases.puzzles[id];
  assert.ok(puzzleCases, `puzzles/cases.json must have cases for ${id}`);

  test(`${id}: reference answer.rill passes`, () => {
    const answerText = readText(PUZZLES_DIR, id, "answer.rill");
    const result = checkAnswer(puzzleCases, answerText);
    assert.equal(result.pass, true, JSON.stringify(result));
  });

  test(`${id}: starter.rill fails`, () => {
    const starterText = readText(PUZZLES_DIR, id, "starter.rill");
    const result = checkAnswer(puzzleCases, starterText);
    assert.equal(result.pass, false);
  });

  const wrongDir = path.join(PUZZLES_DIR, id, "wrong");
  let wrongFiles = [];
  try {
    wrongFiles = readdirSync(wrongDir).filter((f) => f.endsWith(".rill"));
  } catch {
    wrongFiles = [];
  }
  assert.ok(wrongFiles.length > 0, `${id} should have wrong/*.rill files`);

  for (const wf of wrongFiles) {
    test(`${id}: wrong/${wf} fails`, () => {
      const wrongText = readText(wrongDir, wf);
      const result = checkAnswer(puzzleCases, wrongText);
      assert.equal(result.pass, false, JSON.stringify(result));
    });
  }
}

// ---------------------------------------------------------------------
// 3. Cross-check with chibi via puzzles/check/run.sh for every answer
//    and wrong file: JS pass/fail must equal chibi pass/fail.
// ---------------------------------------------------------------------

function chibiPasses(id, file) {
  try {
    execFileSync("bash", [path.join(PUZZLES_DIR, "check", "run.sh"), id, file], {
      cwd: REPO_ROOT,
      stdio: "pipe",
    });
    return true;
  } catch {
    return false;
  }
}

for (const id of puzzleIds()) {
  const puzzleCases = cases.puzzles[id];

  test(`${id}: JS/chibi parity on answer.rill`, () => {
    const file = path.join(PUZZLES_DIR, id, "answer.rill");
    const jsPass = checkAnswer(puzzleCases, readFileSync(file, "utf8")).pass;
    const chibiPass = chibiPasses(id, file);
    assert.equal(jsPass, chibiPass, `${id}/answer.rill: js=${jsPass} chibi=${chibiPass}`);
  });

  const wrongDir = path.join(PUZZLES_DIR, id, "wrong");
  let wrongFiles = [];
  try {
    wrongFiles = readdirSync(wrongDir).filter((f) => f.endsWith(".rill"));
  } catch {
    wrongFiles = [];
  }

  for (const wf of wrongFiles) {
    test(`${id}: JS/chibi parity on wrong/${wf}`, () => {
      const file = path.join(wrongDir, wf);
      const jsPass = checkAnswer(puzzleCases, readFileSync(file, "utf8")).pass;
      const chibiPass = chibiPasses(id, file);
      assert.equal(jsPass, chibiPass, `${id}/wrong/${wf}: js=${jsPass} chibi=${chibiPass}`);
    });
  }
}

// ---------------------------------------------------------------------
// 4. Deep recursion must not crash; a looping answer must fail with
//    "ran too long" in under 5 seconds.
// ---------------------------------------------------------------------

test("deep recursion on a 1000-element list does not crash", () => {
  const answerText = readText(PUZZLES_DIR, "count-crew", "answer.rill");
  const env = makeEnv();
  evaluate(answerText, env);
  const bigChain =
    "(chain " + Array(1000).fill("(seal haan)").join(" ") + ")";
  const got = evaluate("(haan-count " + bigChain + ")", env);
  assert.equal(got, "1000");
});

test("a looping answer fails with 'ran too long' in under 5s", () => {
  const loopingAnswer =
    "(stake haan-count (rig (roster) (haan-count roster)))";
  const start = Date.now();
  const result = checkAnswer(cases.puzzles["count-crew"], loopingAnswer);
  const elapsed = Date.now() - start;
  assert.ok(elapsed < 5000, `took ${elapsed}ms`);
  assert.equal(result.pass, false);
  assert.equal(result.error, "ran too long");
});

test("evaluate() itself throws 'ran too long' on an infinite tail loop", () => {
  const env = makeEnv();
  evaluate("(stake spin (rig (x) (spin x)))", env);
  const start = Date.now();
  assert.throws(() => evaluate("(spin 1)", env), (err) => {
    return err instanceof RillError && err.message === "ran too long";
  });
  assert.ok(Date.now() - start < 5000);
});

// ---------------------------------------------------------------------
// 5. Forms outside the Rill subset raise RillError.
// ---------------------------------------------------------------------

test("call/cc is not part of Rill", () => {
  assert.throws(
    () => evaluate("(call/cc (rig (k) 1))"),
    RillError
  );
});

test("string-append and string literals are not part of Rill", () => {
  assert.throws(() => evaluate('(string-append "a" "b")'), RillError);
  assert.throws(() => evaluate('"a string"'), RillError);
});

test("vector literals are not part of Rill", () => {
  assert.throws(() => evaluate("#(1 2 3)"), RillError);
});

test("raw scheme special forms (define/lambda/if/quote-as-define) are unbound", () => {
  assert.throws(() => evaluate("(define x 1)"), RillError);
  assert.throws(() => evaluate("(lambda (x) x)"), RillError);
  assert.throws(() => evaluate("(if #t 1 2)"), RillError);
  assert.throws(() => evaluate("(let ((x 1)) x)"), RillError);
  assert.throws(() => evaluate("(set! x 1)"), RillError);
});

test("wrong arity to sum/less is a RillError", () => {
  assert.throws(() => evaluate("(sum 1 2 3)"), RillError);
  assert.throws(() => evaluate("(less 5)"), RillError);
});

// ---------------------------------------------------------------------
// Reader / printer sanity beyond the generated cases.
// ---------------------------------------------------------------------

test("dotted pairs print like chibi", () => {
  // A pair whose cdr is itself a pair prints as a flat list; only a
  // genuinely improper tail uses " . ".
  assert.equal(evaluate("(bind 1 2)"), "(1 . 2)");
  assert.equal(evaluate("(chain 1 2 3)"), "(1 2 3)");
  assert.equal(evaluate("(bind 1 (chain 2 3))"), "(1 2 3)");
});

test("quote shorthand reads like (seal ...)", () => {
  assert.equal(evaluate("'fen"), "fen");
  assert.equal(evaluate("'(a b c)"), "(a b c)");
});

test("quote shorthand expands to (quote ...), matching chibi on nested quotes", () => {
  // chibi's own reader expands ' to (quote ...) and prints the symbol
  // `quote` bare, so ''fen evaluates to the datum (quote fen), printed
  // "(quote fen)". Expanding to (seal ...) instead would print
  // "(seal fen)", a real parity mismatch with the reference evaluator
  // on any answer that quotes more than one level deep.
  assert.equal(evaluate("''fen"), "(quote fen)");
  assert.equal(evaluate("'''voth"), "(quote (quote voth))");
});

test("rig rejects duplicate parameter names, like chibi's lambda", () => {
  assert.throws(() => evaluate("(stake f (rig (a a) a)) (f 1 2)"), RillError);
});

test("comments are ignored", () => {
  assert.equal(evaluate("; a comment\n(sum 1 2) ; trailing"), "3");
});
