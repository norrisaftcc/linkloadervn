;; Rill prelude — the loader-tongue's grammar roots, aliased onto
;; chibi-scheme's core forms and procedures.
;;
;; Rill is a strict small subset of Scheme, re-skinned with different
;; keywords. A legal Rill sentence is a legal Scheme s-expression once
;; this prelude is loaded. Nothing here is clever; the point is that
;; the subset is small enough to reimplement, byte for byte, in
;; JavaScript and Python later, with identical results on every case
;; in puzzles/cases.json. Keep this list exact if you ever change it.
;;
;; SUPPORTED FORMS — this is the whole language:
;;
;;   (stake name expr)        define a name.                  = define
;;   (rig (params ...) body)  one params list, ONE body expr.  = lambda
;;   (reckon test then else)  a branch, BOTH arms required.    = if
;;   (bind a b)                                                = cons
;;   (hesh pair)                                               = car
;;   (tull pair)                                               = cdr
;;   (chain a ...)            zero or more arguments.          = list
;;   (sum a b)                arithmetic on two numbers.       = +
;;   (less a b)                arithmetic on two numbers.       = -
;;   (seal datum)              hold a datum, don't run it.      = quote
;;   (husk? x)                                                 = null?
;;   (same? a b)                                               = equal?
;;
;; plus symbols, integers, and lists built from `bind`/`chain`/`seal`.
;;
;; NOT Rill, even though nothing here stops chibi-scheme from running
;; it: strings, vectors, call/cc, set!, do/let/named-let loops, ports,
;; multi-body `rig` forms, one-armed `reckon` forms, or any other
;; Scheme special form or procedure. A puzzle answer that reaches for
;; any of those is off the reservation — see puzzles/check/harness.scm
;; for how far this file's sandbox actually stops that, and how far it
;; doesn't.
;;
;; `stake`, `rig`, `reckon`, and `seal` are macros because they alias
;; special forms (define/lambda/if/quote), which don't evaluate all
;; their parts. Everything else is an ordinary procedure alias.

(define-syntax stake
  (syntax-rules ()
    ((_ name expr) (define name expr))))

(define-syntax rig
  (syntax-rules ()
    ((_ params body) (lambda params body))))

(define-syntax reckon
  (syntax-rules ()
    ((_ test then else) (if test then else))))

(define-syntax seal
  (syntax-rules ()
    ((_ x) (quote x))))

(define bind cons)
(define hesh car)
(define tull cdr)
(define chain list)
;; sum and less take exactly two numbers. A plain alias of + or - would
;; accept (sum 1 2 3), which the JS and Python ports would then have to copy.
(define (sum a b) (+ a b))
(define (less a b) (- a b))
(define husk? null?)
(define same? equal?)
