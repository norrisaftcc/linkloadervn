;; rebalance-coupling/tests.scm — trusted, loaded by harness.scm after
;; the candidate is sandboxed. Not shown to players.

(check "rebalance-coupling: empty coupling" '()
       (sandbox-eval '(rebalance (chain))))
(check "rebalance-coupling: all wrecks" '()
       (sandbox-eval '(rebalance (seal (voth voth)))))
(check "rebalance-coupling: wreck in the middle" '(kessa kessa)
       (sandbox-eval '(rebalance (seal (kessa voth kessa)))))
(check "rebalance-coupling: two wrecks, two sound links" '(sil fen)
       (sandbox-eval '(rebalance (seal (voth sil voth fen)))))
