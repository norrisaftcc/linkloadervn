;; find-signal/tests.scm — trusted, loaded by harness.scm after the
;; candidate is sandboxed. Not shown to players. Checks the candidate
;; against a plain-Scheme reference implementation, not against a
;; second Rill implementation, so the check does not depend on Rill
;; itself being correct.

(define (reference-find-signal lst)
  (cond ((null? lst) 'fen)
        ((equal? (car lst) 'voth) (reference-find-signal (cdr lst)))
        (else (car lst))))

(define *find-signal-test-chains*
  (list '()
        '(voth)
        '(voth voth voth)
        '(sil)
        '(voth voth sil)
        '(sil voth voth)
        '(voth sil voth sil)))

(for-each
 (lambda (c)
   (check (list 'find-signal-on c)
          (reference-find-signal c)
          (sandbox-eval (list 'find-signal (list 'quote c)))))
 *find-signal-test-chains*)
