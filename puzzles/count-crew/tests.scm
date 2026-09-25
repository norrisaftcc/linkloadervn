;; count-crew/tests.scm — trusted, loaded by harness.scm after the
;; candidate is sandboxed. Not shown to players.

(check "count-crew: empty roster" 0
       (sandbox-eval '(haan-count (chain))))
(check "count-crew: 1 kin" 1
       (sandbox-eval '(haan-count (chain (seal haan)))))
(check "count-crew: 3 kin" 3
       (sandbox-eval '(haan-count (chain (seal haan) (seal haan) (seal haan)))))
(check "count-crew: 5 kin" 5
       (sandbox-eval '(haan-count (chain (seal haan) (seal haan) (seal haan)
                                          (seal haan) (seal haan)))))
