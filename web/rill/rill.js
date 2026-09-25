// web/rill/rill.js — Rill evaluator for the browser build. No dependencies.
//
// Rill is the strict Scheme subset defined in puzzles/rill/prelude.scm.
// This file implements a reader, evaluator and chibi-scheme-compatible
// printer for exactly that subset. Read prelude.scm before changing the
// set of supported forms; the JS and Python evaluators and chibi-scheme
// must agree on every case in puzzles/cases.json.
//
// Exports (contract C1):
//   evaluate(source, env?) -> string
//   makeEnv() -> env
//   checkAnswer(cases, answerText) -> { pass, results, error? }
//   class RillError extends Error
//
// The evaluator is an explicit-stack (CEK-style) machine, not native JS
// recursion, so a candidate's own recursion depth (e.g. counting a
// 1000-element list) never grows the JS call stack — it grows a plain
// array on the heap instead. Function application always resumes through
// the same loop, so both tail and non-tail Rill-level recursion are safe
// at that depth. This machine is not itself doing tail-call optimization
// in the traditional sense (a non-tail call like `(sum 1 (f x))` really
// does keep a pending continuation frame on the stack until `f x`
// finishes) — but that pending frame lives in our own array, not in V8's
// native stack, so it cannot overflow it.

// ---------------------------------------------------------------------
// Errors
// ---------------------------------------------------------------------

export class RillError extends Error {
  constructor(message) {
    super(message);
    this.name = "RillError";
  }
}

const STEP_LIMIT = 1000000;

// ---------------------------------------------------------------------
// Data types
// ---------------------------------------------------------------------

class Sym {
  constructor(name) {
    this.name = name;
  }
}

class Pair {
  constructor(car, cdr) {
    this.car = car;
    this.cdr = cdr;
  }
}

// The empty list. A singleton; compare with `===`.
const NIL = { nil: true };

class Closure {
  constructor(params, body, env) {
    this.params = params; // array of parameter name strings
    this.body = body; // the single body expression (unevaluated)
    this.env = env; // defining environment
  }
}

function listToArray(lst) {
  const out = [];
  let cur = lst;
  while (cur instanceof Pair) {
    out.push(cur.car);
    cur = cur.cdr;
  }
  if (cur !== NIL) {
    throw new RillError("improper list where a proper list was expected");
  }
  return out;
}

function arrayToList(arr, tail = NIL) {
  let result = tail;
  for (let i = arr.length - 1; i >= 0; i--) {
    result = new Pair(arr[i], result);
  }
  return result;
}

// ---------------------------------------------------------------------
// Reader
// ---------------------------------------------------------------------

const DELIMITER_RE = /[\s()'";]/;

class Reader {
  constructor(text) {
    this.text = text;
    this.pos = 0;
    this.len = text.length;
  }

  skipAtmosphere() {
    while (this.pos < this.len) {
      const c = this.text[this.pos];
      if (c === ";") {
        while (this.pos < this.len && this.text[this.pos] !== "\n") this.pos++;
        continue;
      }
      if (/\s/.test(c)) {
        this.pos++;
        continue;
      }
      break;
    }
  }

  atEnd() {
    this.skipAtmosphere();
    return this.pos >= this.len;
  }

  readForm() {
    this.skipAtmosphere();
    if (this.pos >= this.len) {
      throw new RillError("unexpected end of input");
    }
    const c = this.text[this.pos];
    if (c === "(") {
      this.pos++;
      return this.readList();
    }
    if (c === ")") {
      throw new RillError("unexpected )");
    }
    if (c === "'") {
      this.pos++;
      const inner = this.readForm();
      // Expand to (quote ...), not (seal ...): chibi-scheme's own reader
      // expands ' to (quote ...), and the printer prints the symbol
      // `quote` bare. Nested quoting (e.g. ''x) prints its outer datum
      // as (quote x); expanding to (seal ...) here would instead print
      // (seal x), a mismatch with the chibi reference on every case
      // with more than one level of quoting. `quote` and `seal` are
      // already synonyms in the evaluator, so this loses nothing.
      return arrayToList([new Sym("quote"), inner]);
    }
    if (c === '"') {
      throw new RillError("strings are not part of Rill");
    }
    if (c === "#") {
      if (this.text.startsWith("#t", this.pos)) {
        this.pos += 2;
        return true;
      }
      if (this.text.startsWith("#f", this.pos)) {
        this.pos += 2;
        return false;
      }
      throw new RillError("unsupported reader syntax starting with #");
    }
    return this.readAtom();
  }

  readAtom() {
    const start = this.pos;
    while (this.pos < this.len && !DELIMITER_RE.test(this.text[this.pos])) {
      this.pos++;
    }
    const raw = this.text.slice(start, this.pos);
    if (raw.length === 0) {
      throw new RillError("unexpected character: " + this.text[this.pos]);
    }
    if (/^-?\d+$/.test(raw)) {
      return parseInt(raw, 10);
    }
    return new Sym(raw);
  }

  readList() {
    const items = [];
    let tail = NIL;
    while (true) {
      this.skipAtmosphere();
      if (this.pos >= this.len) {
        throw new RillError("unexpected end of input in list");
      }
      if (this.text[this.pos] === ")") {
        this.pos++;
        break;
      }
      if (
        this.text[this.pos] === "." &&
        (this.pos + 1 >= this.len || DELIMITER_RE.test(this.text[this.pos + 1]))
      ) {
        this.pos++; // consume the dot
        tail = this.readForm();
        this.skipAtmosphere();
        if (this.text[this.pos] !== ")") {
          throw new RillError("malformed dotted list");
        }
        this.pos++;
        break;
      }
      items.push(this.readForm());
    }
    return arrayToList(items, tail);
  }
}

function readAll(source) {
  const reader = new Reader(source);
  const forms = [];
  while (!reader.atEnd()) {
    forms.push(reader.readForm());
  }
  return forms;
}

function readOne(source) {
  const reader = new Reader(source);
  const form = reader.readForm();
  return form;
}

// ---------------------------------------------------------------------
// Printer (chibi-scheme `write`-compatible, for the values Rill produces)
// ---------------------------------------------------------------------

export function writeValue(v) {
  if (v === NIL) return "()";
  if (v === true) return "#t";
  if (v === false) return "#f";
  if (typeof v === "number") return String(v);
  if (v instanceof Sym) return v.name;
  if (v instanceof Pair) {
    let out = "(";
    let cur = v;
    let first = true;
    while (cur instanceof Pair) {
      if (!first) out += " ";
      out += writeValue(cur.car);
      first = false;
      cur = cur.cdr;
    }
    if (cur === NIL) {
      out += ")";
    } else {
      out += " . " + writeValue(cur) + ")";
    }
    return out;
  }
  if (v instanceof Closure || typeof v === "function") return "#<procedure>";
  return String(v);
}

// ---------------------------------------------------------------------
// Equality (same? / equal?)
// ---------------------------------------------------------------------

function equalRill(a, b) {
  while (true) {
    if (a === b) return true;
    if (typeof a === "number" && typeof b === "number") return a === b;
    if (typeof a === "boolean" || typeof b === "boolean") return a === b;
    if (a instanceof Sym && b instanceof Sym) return a.name === b.name;
    if (a instanceof Pair && b instanceof Pair) {
      if (!equalRill(a.car, b.car)) return false;
      a = a.cdr;
      b = b.cdr;
      continue;
    }
    if (a === NIL || b === NIL) return a === b;
    return false;
  }
}

// ---------------------------------------------------------------------
// Environment
// ---------------------------------------------------------------------

class Env {
  constructor(parent = null) {
    this.vars = new Map();
    this.parent = parent;
  }

  define(name, value) {
    this.vars.set(name, value);
  }

  lookup(name) {
    let e = this;
    while (e) {
      if (e.vars.has(name)) return e.vars.get(name);
      e = e.parent;
    }
    throw new RillError("unbound variable: " + name);
  }
}

function checkArgCount(name, args, n) {
  if (args.length !== n) {
    throw new RillError(
      name + ": expected " + n + " argument(s), got " + args.length
    );
  }
}

function requirePair(name, v) {
  if (!(v instanceof Pair)) {
    throw new RillError(name + ": not a pair");
  }
  return v;
}

function requireNumber(name, v) {
  if (typeof v !== "number") {
    throw new RillError(name + ": not a number");
  }
  return v;
}

export function makeEnv() {
  const env = new Env(null);
  env.define("bind", (args) => {
    checkArgCount("bind", args, 2);
    return new Pair(args[0], args[1]);
  });
  env.define("hesh", (args) => {
    checkArgCount("hesh", args, 1);
    return requirePair("hesh", args[0]).car;
  });
  env.define("tull", (args) => {
    checkArgCount("tull", args, 1);
    return requirePair("tull", args[0]).cdr;
  });
  env.define("chain", (args) => arrayToList(args));
  env.define("sum", (args) => {
    checkArgCount("sum", args, 2);
    return requireNumber("sum", args[0]) + requireNumber("sum", args[1]);
  });
  env.define("less", (args) => {
    checkArgCount("less", args, 2);
    return requireNumber("less", args[0]) - requireNumber("less", args[1]);
  });
  env.define("husk?", (args) => {
    checkArgCount("husk?", args, 1);
    return args[0] === NIL;
  });
  env.define("same?", (args) => {
    checkArgCount("same?", args, 2);
    return equalRill(args[0], args[1]);
  });
  return env;
}

// ---------------------------------------------------------------------
// Evaluator — explicit-stack CEK-style machine.
//
// `stack` holds continuation frames describing what to do once the
// value currently being computed (`expr` under `env`, in 'eval' mode,
// or the freshly produced `value`, in 'cont' mode) is ready. Function
// application resumes through this same loop (via the `isTail` flag
// from applyProc), so no JS-native recursion is used for Rill-level
// recursion of any kind, tail or not.
// ---------------------------------------------------------------------

function applyProc(proc, args) {
  if (typeof proc === "function") {
    return { value: proc(args) };
  }
  if (proc instanceof Closure) {
    if (args.length !== proc.params.length) {
      throw new RillError(
        "wrong number of arguments: expected " +
          proc.params.length +
          ", got " +
          args.length
      );
    }
    const newEnv = new Env(proc.env);
    for (let i = 0; i < proc.params.length; i++) {
      newEnv.define(proc.params[i], args[i]);
    }
    return { isTail: true, expr: proc.body, env: newEnv };
  }
  throw new RillError("not applicable");
}

function evalTop(startExpr, startEnv) {
  const stack = [];
  let expr = startExpr;
  let env = startEnv;
  let mode = "eval";
  let value;
  let steps = 0;

  while (true) {
    steps++;
    if (steps > STEP_LIMIT) {
      throw new RillError("ran too long");
    }

    if (mode === "eval") {
      if (expr instanceof Sym) {
        value = env.lookup(expr.name);
        mode = "cont";
        continue;
      }

      if (expr instanceof Pair) {
        const op = expr.car;
        const formName = op instanceof Sym ? op.name : null;

        if (formName === "stake") {
          const parts = listToArray(expr.cdr);
          if (parts.length !== 2) {
            throw new RillError("stake: expected a name and one expression");
          }
          const [nameExpr, valueExpr] = parts;
          if (!(nameExpr instanceof Sym)) {
            throw new RillError("stake: name must be a symbol");
          }
          stack.push({ type: "stake", name: nameExpr.name, env });
          expr = valueExpr;
          mode = "eval";
          continue;
        }

        if (formName === "rig") {
          const parts = listToArray(expr.cdr);
          if (parts.length !== 2) {
            throw new RillError(
              "rig: expected one params list and exactly one body expression"
            );
          }
          const [paramsExpr, body] = parts;
          const paramSyms = listToArray(paramsExpr);
          const seen = new Set();
          const params = paramSyms.map((p) => {
            if (!(p instanceof Sym)) {
              throw new RillError("rig: parameters must be symbols");
            }
            if (seen.has(p.name)) {
              throw new RillError("rig: duplicate parameter: " + p.name);
            }
            seen.add(p.name);
            return p.name;
          });
          value = new Closure(params, body, env);
          mode = "cont";
          continue;
        }

        if (formName === "reckon") {
          const parts = listToArray(expr.cdr);
          if (parts.length !== 3) {
            throw new RillError(
              "reckon: expected exactly a test, a then and an else"
            );
          }
          const [test, then, elseE] = parts;
          stack.push({ type: "reckon", then, elseE, env });
          expr = test;
          mode = "eval";
          continue;
        }

        if (formName === "seal" || formName === "quote") {
          const parts = listToArray(expr.cdr);
          if (parts.length !== 1) {
            throw new RillError(formName + ": expected exactly one datum");
          }
          value = parts[0];
          mode = "cont";
          continue;
        }

        // Ordinary application: evaluate the operator, then each
        // argument in order, then apply.
        const argExprs = listToArray(expr.cdr);
        stack.push({
          type: "apply",
          argExprs,
          argIndex: 0,
          argVals: [],
          evaluatingOp: true,
          opVal: undefined,
          env,
        });
        expr = op;
        mode = "eval";
        continue;
      }

      // Self-evaluating: numbers, booleans, the empty list.
      value = expr;
      mode = "cont";
      continue;
    }

    // mode === "cont": `value` is ready; deliver it to the top frame.
    if (stack.length === 0) {
      return value;
    }
    const frame = stack[stack.length - 1];

    if (frame.type === "stake") {
      stack.pop();
      frame.env.define(frame.name, value);
      value = new Sym(frame.name);
      continue;
    }

    if (frame.type === "reckon") {
      stack.pop();
      expr = value !== false ? frame.then : frame.elseE;
      env = frame.env;
      mode = "eval";
      continue;
    }

    if (frame.type === "apply") {
      if (frame.evaluatingOp) {
        frame.opVal = value;
        frame.evaluatingOp = false;
      } else {
        frame.argVals.push(value);
      }
      if (frame.argIndex < frame.argExprs.length) {
        expr = frame.argExprs[frame.argIndex++];
        env = frame.env;
        mode = "eval";
        continue;
      }
      stack.pop();
      const result = applyProc(frame.opVal, frame.argVals);
      if (result.isTail) {
        expr = result.expr;
        env = result.env;
        mode = "eval";
      } else {
        value = result.value;
        mode = "cont";
      }
      continue;
    }

    throw new RillError("internal error: unknown continuation frame");
  }
}

function asRillError(e) {
  if (e instanceof RillError) return e;
  const err = new RillError(e && e.message ? e.message : String(e));
  return err;
}

// ---------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------

export function evaluate(source, env) {
  const e = env || makeEnv();
  try {
    const forms = readAll(source);
    let result = NIL;
    for (const form of forms) {
      result = evalTop(form, e);
    }
    return writeValue(result);
  } catch (err) {
    throw asRillError(err);
  }
}

export function checkAnswer(cases, answerText) {
  let env;
  try {
    env = makeEnv();
    const forms = readAll(answerText);
    for (const form of forms) {
      evalTop(form, env);
    }
  } catch (err) {
    return { pass: false, results: [], error: asRillError(err).message };
  }

  let topError;
  const results = cases.map((c) => {
    let got;
    let threw = false;
    let msg;
    try {
      const form = readOne(c.input);
      const value = evalTop(form, env);
      got = writeValue(value);
    } catch (err) {
      threw = true;
      msg = asRillError(err).message;
    }

    let ok;
    if (msg === "ran too long") {
      ok = false;
      if (!topError) topError = msg;
    } else if (c.expected === "error") {
      ok = threw;
    } else {
      ok = !threw && got === c.expected;
    }

    return {
      input: c.input,
      expected: c.expected,
      got: threw ? undefined : got,
      ok,
    };
  });

  const pass = results.every((r) => r.ok);
  const out = { pass, results };
  if (topError) out.error = topError;
  return out;
}
