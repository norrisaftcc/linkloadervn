#!/usr/bin/env bash
# puzzles/check/run.sh — run the Rill puzzle checks under chibi-scheme.
#
# Two modes:
#
#   run.sh
#     Full suite. For every puzzle: checks its reference answer.rill
#     passes, and every file under its wrong/ folder fails. Prints a
#     pass/fail count per case and a final summary line. Exits 0 only
#     if every reference answer passed AND every wrong answer failed.
#
#   run.sh <puzzle-id> <answer-file>
#     Checks one answer against one puzzle. Exits 0 if it passes, 1 if
#     it does not. This is the entry point a real player-facing tool
#     would call.
#
# Each check runs chibi-scheme in its own process (see
# puzzles/check/harness.scm for what that isolation does and does not
# buy you). No timeout is applied by default — an infinite loop in an
# answer will hang; wrap calls in `timeout` yourself if you're running
# untrusted input unattended.

set -euo pipefail
ORIGINAL_PWD="$(pwd)"
cd "$(dirname "${BASH_SOURCE[0]}")/.."   # now in puzzles/
PUZZLES_DIR="$(pwd)"
HARNESS="$PUZZLES_DIR/check/harness.scm"
PRELUDE="$PUZZLES_DIR/rill/prelude.scm"

# Resolve a path the caller gave us against the directory they were in
# when they ran this script, not against puzzles/ (which is our own
# cwd from here on). An already-absolute path is left alone.
resolve() {
  case "$1" in
    /*) echo "$1" ;;
    *) echo "$ORIGINAL_PWD/$1" ;;
  esac
}

check_one() {
  # $1 = puzzle id, $2 = candidate file. Prints chibi's output, returns
  # chibi's own exit code.
  local puzzle="$1" file="$2"
  # A player answer that loops forever must not hang the run.
  timeout "${RILL_TIMEOUT:-5}" chibi-scheme -q "$HARNESS" "$PUZZLES_DIR/$puzzle" "$file" "$PRELUDE"
}

# Single-answer mode.
if [ "$#" -eq 2 ]; then
  puzzle="$1"
  file="$(resolve "$2")"
  if [ ! -d "$PUZZLES_DIR/$puzzle" ]; then
    echo "no such puzzle: $puzzle" >&2
    exit 1
  fi
  if check_one "$puzzle" "$file"; then
    exit 0
  else
    exit 1
  fi
fi

if [ "$#" -ne 0 ]; then
  echo "usage: run.sh [<puzzle-id> <answer-file>]" >&2
  exit 2
fi

# Full-suite mode.
total_pass=0
total_fail=0

for puzzle_dir in "$PUZZLES_DIR"/*/; do
  id="$(basename "$puzzle_dir")"
  case "$id" in
    rill|check) continue ;;
  esac
  [ -f "${puzzle_dir}answer.rill" ] || continue

  echo "== $id: reference answer =="
  if check_one "$id" "${puzzle_dir}answer.rill"; then
    echo "  OK  reference answer passes"
    total_pass=$((total_pass + 1))
  else
    echo "  FAIL  reference answer did NOT pass (this is a bug in the puzzle)"
    total_fail=$((total_fail + 1))
  fi

  if [ -d "${puzzle_dir}wrong" ]; then
    for wrong in "${puzzle_dir}wrong"/*.rill; do
      [ -e "$wrong" ] || continue
      echo "== $id: wrong answer $(basename "$wrong") (must FAIL) =="
      if check_one "$id" "$wrong"; then
        echo "  FAIL  wrong answer incorrectly PASSED: $wrong (this is a bug in the puzzle)"
        total_fail=$((total_fail + 1))
      else
        echo "  OK  wrong answer correctly rejected"
        total_pass=$((total_pass + 1))
      fi
    done
  fi
  echo
done

echo "== puzzles/check/run.sh summary: $total_pass pass, $total_fail fail =="

if [ "$total_fail" -eq 0 ]; then
  exit 0
else
  exit 1
fi
