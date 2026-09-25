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
;; That is the whole guarantee of the sandbox itself. Two more guards
;; sit around it:
;;   - Before loading, `check-candidate` (below) reads the candidate's
;;     forms and rejects any symbol, form or datum outside the Rill
;;     subset: no define, lambda, let, strings, vectors, multi-body
;;     rig or one-armed reckon. This keeps chibi in step with rill.js.
;;   - run.sh stops each check after RILL_TIMEOUT seconds (default 5),
;;     so an infinite loop fails instead of hanging.
;;   There is no memory limit.
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

(import (scheme eval) (scheme file) (scheme cxr))

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

;; ---- Rill subset check ------------------------------------------
;; The sandbox below is full r7rs, so chibi alone would accept `let`,
;; `lambda`, strings and the rest. The browser's rill.js does not. To
;; keep the two in step, reject any candidate that uses a form outside
;; the Rill subset before it is loaded. The rules follow the SUPPORTED
;; FORMS list in puzzles/rill/prelude.scm.

(define *rill-roots*
  '(stake rig reckon bind hesh tull chain sum less seal husk? same?))

(define (read-all-forms path)
  (call-with-input-file path
    (lambda (port)
      (let loop ((acc '()))
        (let ((form (read port)))
          (if (eof-object? form) (reverse acc) (loop (cons form acc))))))))

(define (not-rill what)
  (display "  FAIL  not Rill: ") (write what) (newline)
  (error "candidate uses a form outside the Rill subset" what))

(define (proper-list? x)
  (or (null? x) (and (pair? x) (proper-list? (cdr x)))))

;; Check one expression. `bound` holds the names the candidate may use
;; besides the grammar roots: its own stake names and enclosing rig
;; parameters.
(define (check-expr x bound)
  (cond
    ((symbol? x)
     (if (not (or (memq x *rill-roots*) (memq x bound))) (not-rill x)))
    ((or (number? x) (boolean? x)) #t)
    ((pair? x)
     (if (not (proper-list? x)) (not-rill x))
     (let ((head (car x)) (args (cdr x)))
       (cond
         ((or (eq? head 'seal) (eq? head 'quote))
          (if (not (= (length args) 1)) (not-rill x))
          (check-datum (car args)))
         ((eq? head 'stake) (not-rill x))  ; only allowed at top level
         ((eq? head 'rig)
          (if (not (and (= (length args) 2)
                        (proper-list? (car args))
                        (let all-symbols ((ps (car args)))
                          (or (null? ps)
                              (and (symbol? (car ps)) (all-symbols (cdr ps)))))))
              (not-rill x))
          (check-expr (cadr args) (append (car args) bound)))
         ((eq? head 'reckon)
          (if (not (= (length args) 3)) (not-rill x))
          (for-each (lambda (a) (check-expr a bound)) args))
         (else
          (for-each (lambda (a) (check-expr a bound)) x)))))
    (else (not-rill x))))

;; Quoted data may hold only symbols, integers, booleans and lists.
(define (check-datum d)
  (cond ((or (symbol? d) (number? d) (boolean? d) (null? d)) #t)
        ((pair? d) (check-datum (car d)) (check-datum (cdr d)))
        (else (not-rill d))))

(define (check-candidate forms)
  (let ((names (let collect ((fs forms) (acc '()))
                 (cond ((null? fs) acc)
                       ((and (pair? (car fs)) (eq? (caar fs) 'stake)
                             (proper-list? (car fs)) (= (length (car fs)) 3)
                             (symbol? (cadar fs)))
                        (collect (cdr fs) (cons (cadar fs) acc)))
                       (else (collect (cdr fs) acc))))))
    (for-each
      (lambda (f)
        (if (and (pair? f) (eq? (car f) 'stake))
            (if (and (proper-list? f) (= (length f) 3) (symbol? (cadr f)))
                (check-expr (caddr f) names)
                (not-rill f))
            (check-expr f names)))
      forms)))

(check-candidate (read-all-forms *candidate-file*))

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
