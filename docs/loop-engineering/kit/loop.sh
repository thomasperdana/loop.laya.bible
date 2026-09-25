#!/usr/bin/env bash
# loop.sh: a minimal, safe loop runner from "Loop Engineering: From Zero to Hero".
#
# What it does: runs an agent command, then a check command, again and again,
# until the check passes (DONE) or a stop rule fires (CAP, STUCK, HUMAN, DANGER).
# Every iteration appends one row to a CSV run log whose columns match the
# workbook's Run Log sheet.
#
# Safe by default: DRY_RUN=1 runs a harmless mock instead of an agent, so you can
# watch every exit for free. A dry run makes no network or API calls and needs no account.
#
# Exit codes: 0 DONE · 1 script error · 2 CAP · 3 STUCK · 4 HUMAN · 5 DANGER
#
# Try it (dry run, in a scratch folder):
#   MOCK_PASS_AT=3 ./loop.sh     # DONE on iteration 3 (exit 0)
#   MOCK_PASS_AT=99 ./loop.sh    # CAP after MAX_ITERS iterations (exit 2)
#   MOCK_STUCK=1 ./loop.sh       # STUCK after 3 identical failures (exit 3)
#   touch .loop-stop; ./loop.sh  # HUMAN (exit 4); then: rm .loop-stop
#   echo 'exit 0' > fake-check.sh; MOCK_TAMPER=1 PROTECT=fake-check.sh ./loop.sh   # DANGER (exit 5)
#
# Real mode: only after a dry run, and only in a branch or worktree. Set DRY_RUN=0,
# AGENT_CMD, and CHECK_CMD yourself (see the example under the settings).
# Works with the bash that ships with macOS (3.2) and with Linux.

set -euo pipefail

# ---- settings: override any of these with environment variables ----
MAX_ITERS="${MAX_ITERS:-5}"          # CAP: most iterations per run (hard ceiling 50)
MAX_MINUTES="${MAX_MINUTES:-20}"     # CAP: most wall-clock minutes per run (hard ceiling 240)
STUCK_LIMIT="${STUCK_LIMIT:-3}"      # STUCK: the same failure this many times in a row
STOP_FILE="${STOP_FILE:-.loop-stop}" # HUMAN: create this file to stop the loop
PROTECT="${PROTECT:-}"               # DANGER: files the agent must never change (space-separated)
LOG_FILE="${LOG_FILE:-loop-log.csv}" # the run log
DRY_RUN="${DRY_RUN:-1}"              # 1 = mock agent and mock check (safe); 0 = real commands
AGENT_CMD="${AGENT_CMD:-}"           # real mode: the command that runs one agent turn
CHECK_CMD="${CHECK_CMD:-}"           # real mode: the check (exit code 0 means pass)
MOCK_PASS_AT="${MOCK_PASS_AT:-3}"    # dry run: the iteration on which the mock check passes
MOCK_STUCK="${MOCK_STUCK:-0}"        # dry run: 1 = the mock check fails the same way every time
MOCK_TAMPER="${MOCK_TAMPER:-0}"      # dry run: 1 = the mock agent edits the first PROTECT file

# Real-mode example (⚠VERIFY the flags against current Claude Code docs before use):
#   DRY_RUN=0 \
#   AGENT_CMD='claude -p "$(cat PROMPT.md)" --allowedTools "Read,Edit,Bash(npm test *)"' \
#   CHECK_CMD='npm test' \
#   PROTECT='test/auth.test.js' ./loop.sh
# Never add permission-skipping flags unless this runs inside a disposable container or VM.

# ---- guard rails: refuse settings that break the stop rules ----
whole_number() { case "$2" in ''|*[!0-9]*) echo "$1 must be a whole number, got '$2'" >&2; exit 1 ;; esac; }
whole_number MAX_ITERS "$MAX_ITERS"
whole_number MAX_MINUTES "$MAX_MINUTES"
whole_number STUCK_LIMIT "$STUCK_LIMIT"
whole_number MOCK_PASS_AT "$MOCK_PASS_AT"
if [ "$MAX_ITERS" -lt 1 ] || [ "$MAX_ITERS" -gt 50 ]; then echo "MAX_ITERS must be 1-50" >&2; exit 1; fi
if [ "$MAX_MINUTES" -lt 1 ] || [ "$MAX_MINUTES" -gt 240 ]; then echo "MAX_MINUTES must be 1-240" >&2; exit 1; fi
if [ "$STUCK_LIMIT" -lt 1 ]; then echo "STUCK_LIMIT must be at least 1" >&2; exit 1; fi
if [ "$DRY_RUN" != "1" ] && { [ -z "$AGENT_CMD" ] || [ -z "$CHECK_CMD" ]; }; then
  echo "Real mode (DRY_RUN=0) needs both AGENT_CMD and CHECK_CMD" >&2; exit 1
fi

# ---- helpers ----
now() { date -u +%Y-%m-%dT%H:%M:%SZ; }

# A fingerprint of the protected files. Any edit, or a deletion, changes it.
fingerprint() {
  if [ -n "$PROTECT" ]; then
    # shellcheck disable=SC2086  # word splitting is intended: PROTECT is a list of paths
    cksum $PROTECT 2>&1 || true
  fi
}

# Lines changed in the git working tree, if we're inside a git repository.
diff_lines() {
  if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git diff --numstat 2>/dev/null | awk '{ s += $1 + $2 } END { print s + 0 }'
  fi
}

# One CSV row: iteration, started_at, action, check_result, stop_reason, tokens_in, tokens_out, diff_lines, note
log_row() {
  note=$(printf '%s' "$6" | tr '"\n' "' " | cut -c1-120)
  printf '%s,%s,%s,%s,%s,,,%s,"%s"\n' "$1" "$2" "$3" "$4" "$5" "$(diff_lines)" "$note" >> "$LOG_FILE"
}

# ---- start ----
[ -f "$LOG_FILE" ] || echo "iteration,started_at,action,check_result,stop_reason,tokens_in,tokens_out,diff_lines,note" > "$LOG_FILE"
mode="real"; [ "$DRY_RUN" = "1" ] && mode="dry run"
echo "loop.sh ($mode) · MAX_ITERS=$MAX_ITERS · MAX_MINUTES=$MAX_MINUTES · STUCK_LIMIT=$STUCK_LIMIT · stop file: $STOP_FILE"
baseline=$(fingerprint)
start=$(date +%s)
last_fp=""
same=0
i=1

while [ "$i" -le "$MAX_ITERS" ]; do
  started=$(now)

  # HUMAN: a person can stop the loop at any time by creating the stop file.
  if [ -f "$STOP_FILE" ]; then
    log_row "$i" "$started" "none" "skipped" "HUMAN" "stop file found"
    echo "HUMAN: $STOP_FILE found, stopping before iteration $i"; exit 4
  fi

  # CAP (time): the whole run gets MAX_MINUTES, no matter how many iterations are left.
  if [ $(( $(date +%s) - start )) -ge $(( MAX_MINUTES * 60 )) ]; then
    log_row "$i" "$started" "none" "skipped" "CAP" "time limit reached"
    echo "CAP: $MAX_MINUTES minutes used"; exit 2
  fi

  # ACT: one agent turn (or the mock).
  if [ "$DRY_RUN" = "1" ]; then
    action="mock-agent"
    if [ "$MOCK_TAMPER" = "1" ] && [ -n "$PROTECT" ]; then
      first_protected=${PROTECT%% *}
      echo "# edited by the mock agent" >> "$first_protected"
    fi
  else
    action="agent"
    bash -c "$AGENT_CMD" || echo "(the agent command exited non-zero; the check still decides)"
  fi

  # DANGER: stop at once if a protected file changed (the agent may be gaming the check).
  if [ "$(fingerprint)" != "$baseline" ]; then
    log_row "$i" "$started" "$action" "fail" "DANGER" "protected file changed"
    echo "DANGER: a protected file changed on iteration $i"; exit 5
  fi

  # VERIFY: the check decides, never the agent.
  if [ "$DRY_RUN" = "1" ]; then
    if [ "$MOCK_STUCK" = "1" ]; then
      out="FAIL: test_refund_rounding expected 10.01, got 10.00"; ok=1
    elif [ "$i" -ge "$MOCK_PASS_AT" ]; then
      out="PASS: all checks green"; ok=0
    else
      out="FAIL: $(( MOCK_PASS_AT - i )) left to fix"; ok=1
    fi
  else
    if out=$(bash -c "$CHECK_CMD" 2>&1); then ok=0; else ok=1; fi
  fi
  last_line=$(printf '%s\n' "$out" | tail -n 1)

  # DECIDE: DONE, STUCK, CAP, or go again.
  if [ "$ok" -eq 0 ]; then
    log_row "$i" "$started" "$action" "pass" "DONE" "$last_line"
    echo "DONE on iteration $i: $last_line"; exit 0
  fi
  fp=$(printf '%s' "$out" | cksum)
  if [ "$fp" = "$last_fp" ]; then same=$(( same + 1 )); else same=1; last_fp="$fp"; fi
  if [ "$same" -ge "$STUCK_LIMIT" ]; then
    log_row "$i" "$started" "$action" "fail" "STUCK" "$last_line"
    echo "STUCK: the same failure $same times in a row: $last_line"; exit 3
  fi
  reason=""
  if [ "$i" -eq "$MAX_ITERS" ]; then reason="CAP"; fi
  log_row "$i" "$started" "$action" "fail" "$reason" "$last_line"
  echo "iteration $i: not yet · $last_line"
  i=$(( i + 1 ))
done

echo "CAP: $MAX_ITERS iterations used without a pass"
exit 2
