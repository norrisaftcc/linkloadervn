;; read-brand/tests.scm — trusted, loaded by harness.scm after the
;; candidate is sandboxed. Not shown to players.

(check "read-brand: kessa voth sil fen -> sil" 'sil
       (sandbox-eval '(read-brand (seal (kessa voth sil fen)))))
(check "read-brand: haan haan drev -> drev" 'drev
       (sandbox-eval '(read-brand (seal (haan haan drev)))))
(check "read-brand: mora dray fen -> fen" 'fen
       (sandbox-eval '(read-brand (seal (mora dray fen)))))
