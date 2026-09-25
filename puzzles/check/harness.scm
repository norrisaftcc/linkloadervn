;; puzzles/check/harness.scm — the generic Rill puzzle checker.
;;
;; Usage:
;;   chibi-scheme -q harness.scm <puzzle-dir> <candidate-file> <prelude-path>
;;
;; What it does, in order:
;;   1. Builds a sandbox environment: plain r7rs (scheme base) plus the
;;      Rill prelude, nothing else.
;;   2. Loads the candidate's file (a starter, an answer, or a wrong
;;      answer) into that sandbox.
;;   3. Loads the puzzle's own tests.scm — trusted content, written by
;;      the puzzle author, never shown to a player — which reads
;;      whatever the candidate defined out of the sandbox with
;;      `sandbox-eval` and checks it with `check`.
;;   4. Prints a pass/fail line per check, then a summary line, then
;;      exits nonzero (via `error`, per chibi -q's own limits — see
;;      below) if any check failed.
;;
;; SANDBOX — WHAT IT PROTECTS AND WHAT IT DOESN'T:
;;
;; The candidate is loaded into its own `environment` object, not into
;; this script's top level. That is real isolation for one thing only:
;; the candidate's top-level `stake`/`define` forms land in the
;; sandbox environment, so they cannot overwrite THIS harness's own
;; `check`, `*pass*`, `*fail*`, or a puzzle's reference implementation
;; in tests.scm — those live in a different environment entirely, and
;; chibi-scheme's `environment` objects do not leak definitions back
;; out.
;;
;; That is the whole guarantee. It does NOT mean the candidate is
;; running inside "Rill" as a restricted language:
;;   - The sandbox's base library is r7rs (scheme base), which is far
;;     bigger than the 12 Rill grammar roots (it has call/cc, strings,
;;     vectors, higher-order procedures, and more). A candidate could
;;     use any of it. Nothing here parses or restricts syntax to the
;;     Rill subset; the prelude only offers convenient aliases. Full
;;     enforcement would need a real parser/allowlist, which this
;;     small a game doesn't have yet.
;;   - There is no time limit or memory limit. An infinite loop in a
;;     candidate hangs the chibi-scheme process. Run puzzles/check/
;;     run.sh (or any single check) under `timeout` if you don't
;;     trust the input.
;;   - A candidate can still break ITS OWN code by shadowing a Rill
;;     grammar root before using it (e.g. redefining `hesh` inside its
;;     own answer) — that only affects that one candidate's sandbox,
;;     not the harness, so it is a code-review problem for that
;;     answer, not a security hole.
;;
;; chibi-scheme's `-q` ("quick load") mode has no working exception
;; system in practice (`guard` and `with-exception-handler` do not
;; behave as R7RS describes under it — verified against this chibi
;; build; see puzzles/check/run.sh's header for the check). So this
;; harness does not try to catch errors from the candidate or from
;; tests.scm. A candidate that errors while loading, or while a check
;; calls into it, kills this whole process with a nonzero exit code —
;; that IS the fail signal. `run.sh` reads the exit code, not any
;; caught condition.

(import (scheme eval))

(define *harness-args* (command-line))
(if (< (length *harness-args*) 4)
    (error "usage: chibi-scheme -q harness.scm <puzzle-dir> <candidate-file> <prelude-path>"))

(define *puzzle-dir* (list-ref *harness-args* 1))
(define *candidate-file* (list-ref *harness-args* 2))
(define *prelude-path* (list-ref *harness-args* 3))

(define (join-path a b) (string-append a "/" b))

(define *pass* 0)
(define *fail* 0)

;; Puzzle tests.scm files call this to record one check.
(define (check label expected actual)
  (if (equal? expected actual)
      (begin
        (set! *pass* (+ *pass* 1))
        (display "  PASS  ") (display label) (newline))
      (begin
        (set! *fail* (+ *fail* 1))
        (display "  FAIL  ") (display label)
        (display "  expected=") (write expected)
        (display "  actual=") (write actual)
        (newline))))

;; The sandbox: r7rs base + the Rill prelude. The candidate's file is
;; loaded into it below, before tests.scm ever runs.
(define *sandbox* (environment '(scheme base)))
(load *prelude-path* *sandbox*)
(load *candidate-file* *sandbox*)

;; Puzzle tests.scm files call this to read a value, or run a form,
;; out of the candidate's sandbox.
(define (sandbox-eval form) (eval form *sandbox*))

(display "-- checking ") (display *candidate-file*)
(display " against ") (display *puzzle-dir*) (display " --") (newline)

(load (join-path *puzzle-dir* "tests.scm"))

(newline)
(display "-- ") (display *pass*) (display " pass, ")
(display *fail*) (display " fail --") (newline)

(if (> *fail* 0)
    (error "puzzle checks failed" *candidate-file* *fail*)
    (display "OK\n"))
