;; count-herd/tests.scm — trusted, loaded by harness.scm after the
;; candidate is sandboxed. Not shown to players.

(check "count-herd: empty chest" 0
       (sandbox-eval '(herd-count (chain))))
(check "count-herd: one wreck, no kin" 0
       (sandbox-eval '(herd-count (seal (voth)))))
(check "count-herd: two kin, one wreck" 2
       (sandbox-eval '(herd-count (seal (haan voth haan)))))
(check "count-herd: three kin, two wrecks" 3
       (sandbox-eval '(herd-count (seal (voth haan voth haan haan)))))
