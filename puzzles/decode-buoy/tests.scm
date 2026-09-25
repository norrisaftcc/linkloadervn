;; decode-buoy/tests.scm — trusted, loaded by harness.scm after the
;; candidate is sandboxed. Not shown to players. Uses `sandbox-eval`
;; and `check`, both defined by puzzles/check/harness.scm.

(define *decode-buoy-expected* '(signal star dust drift home))

(check "decode-buoy: answer" *decode-buoy-expected* (sandbox-eval 'answer))
