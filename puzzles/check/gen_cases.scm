;; puzzles/check/gen_cases.scm — emit puzzles/cases.json.
;;
;; Run: chibi-scheme -q puzzles/check/gen_cases.scm > puzzles/cases.json
;;
;; Every case is language-neutral: an input form as text, and the
;; expected printed result as text (or the literal string "error").
;; A future JavaScript or Python Rill evaluator can replay every case
;; here and diff its output against this chibi-scheme reference,
;; without anyone re-deriving the cases by hand.
;;
;; Most cases below are computed for real, against the Rill prelude
;; loaded into a sandbox, and against the same reference
;; implementations of haan-count/find-signal/answer that the puzzle
;; tests use. The one deliberate error case is NOT evaluated here: as
;; documented in puzzles/check/harness.scm, chibi -q's exception
;; system does not behave well enough to catch it safely inside this
;; script, so its "error" expectation is asserted by hand instead. Any
;; evaluator being parity-tested against this file must independently
;; confirm that (hesh (chain)) — car of an empty list — is an error.

(import (scheme eval))

(define *sandbox* (environment '(scheme base)))
(load "puzzles/rill/prelude.scm" *sandbox*)

(eval '(stake haan-count
         (rig (roster)
           (reckon (husk? roster)
                   0
                   (sum 1 (haan-count (tull roster))))))
      *sandbox*)

(eval '(stake find-signal
         (rig (chain-in)
           (reckon (husk? chain-in)
                   (seal fen)
                   (reckon (same? (hesh chain-in) (seal voth))
                           (find-signal (tull chain-in))
                           (hesh chain-in)))))
      *sandbox*)

(eval '(stake answer (seal (signal star dust drift home))) *sandbox*)

(define (printed-of form)
  (call-with-output-string
   (lambda (port) (write (eval form *sandbox*) port))))

;; label . input-form . (either 'eval or a literal expected string)
(define *prelude-cases*
  (list
   (list "(bind 1 2)"                              '(bind 1 2))
   (list "(hesh (bind 1 2))"                        '(hesh (bind 1 2)))
   (list "(tull (bind 1 2))"                        '(tull (bind 1 2)))
   (list "(chain)"                                  '(chain))
   (list "(chain 1 2 3)"                            '(chain 1 2 3))
   (list "(sum 2 3)"                                '(sum 2 3))
   (list "(less 5 2)"                               '(less 5 2))
   (list "(seal fen)"                               '(seal fen))
   (list "(husk? (chain))"                          '(husk? (chain)))
   (list "(husk? (chain 1))"                        '(husk? (chain 1)))
   (list "(same? (seal fen) (seal fen))"            '(same? (seal fen) (seal fen)))
   (list "(same? (seal fen) (seal voth))"           '(same? (seal fen) (seal voth)))
   (list "(reckon (husk? (chain)) (seal empty) (seal full))"
         '(reckon (husk? (chain)) (seal empty) (seal full)))))

(define *puzzle-cases*
  (list
   (list "decode-buoy"
         (list (list "answer" 'answer)))
   (list "count-crew"
         (list
          (list "(haan-count (chain))" '(haan-count (chain)))
          (list "(haan-count (chain (seal haan)))" '(haan-count (chain (seal haan))))
          (list "(haan-count (chain (seal haan) (seal haan) (seal haan)))"
                '(haan-count (chain (seal haan) (seal haan) (seal haan))))
          (list "(haan-count (chain (seal haan) (seal haan) (seal haan) (seal haan) (seal haan)))"
                '(haan-count (chain (seal haan) (seal haan) (seal haan) (seal haan) (seal haan))))))
   (list "find-signal"
         (list
          (list "(find-signal (seal ()))" '(find-signal (seal ())))
          (list "(find-signal (seal (voth)))" '(find-signal (seal (voth))))
          (list "(find-signal (seal (voth voth voth)))" '(find-signal (seal (voth voth voth))))
          (list "(find-signal (seal (sil)))" '(find-signal (seal (sil))))
          (list "(find-signal (seal (voth voth sil)))" '(find-signal (seal (voth voth sil))))
          (list "(find-signal (seal (sil voth voth)))" '(find-signal (seal (sil voth voth))))
          (list "(find-signal (seal (voth sil voth sil)))" '(find-signal (seal (voth sil voth sil))))))))

(define (json-string s)
  (string-append "\"" s "\""))

(define (case->json c)
  (string-append "{\"input\": " (json-string (car c))
                  ", \"expected\": " (json-string (printed-of (cadr c)))
                  "}"))

(define (join-with sep strs)
  (if (null? strs)
      ""
      (let loop ((acc (car strs)) (rest (cdr strs)))
        (if (null? rest)
            acc
            (loop (string-append acc sep (car rest)) (cdr rest))))))

(display "{\n")
(display "  \"generated_by\": \"puzzles/check/gen_cases.scm\",\n")
(display "  \"note\": \"Language-neutral Rill test cases for parity-testing future JS/Python evaluators against chibi-scheme. expected is the printed value (write), or the literal string \\\"error\\\" if the reference evaluator raises.\",\n")

(display "  \"prelude_cases\": [\n    ")
(display (join-with ",\n    " (map case->json *prelude-cases*)))
(display ",\n    {\"input\": \"(hesh (chain))\", \"expected\": \"error\"}")
(display ",\n    {\"input\": \"(sum 1 2 3)\", \"expected\": \"error\"}")
(display ",\n    {\"input\": \"(less 5)\", \"expected\": \"error\"}\n")
(display "  ],\n")

(display "  \"puzzles\": {\n")
(display (join-with ",\n"
  (map (lambda (pc)
         (string-append "    " (json-string (car pc)) ": [\n      "
                         (join-with ",\n      " (map case->json (cadr pc)))
                         "\n    ]"))
       *puzzle-cases*)))
(display "\n  }\n")
(display "}\n")
