# Loop Spec: {{LOOP_NAME}}

A one-page design for one loop. Fill in the boxes in this order: DONE WHEN → CHECKER → LIMITS → GOAL → TRIGGER → ACTOR → CONTEXT → STATE → ESCALATION. Replace every `{{PLACEHOLDER}}`; the text after each one is an example.

| Header | Your answer |
|---|---|
| Name | {{LOOP_NAME}} (example: `docs-links`) |
| Version | {{VERSION}} (start at `v0.1`; bump on every change) |
| Owner | {{OWNER}} (a person, not "the team") |
| Autonomy rung | {{RUNG}} (1 watch · 2 suggest · 3 act with approval · 4 act alone; money, health, legal, or production work stays at 3 or lower) |
| Risk level | {{RISK}} (what a bad run costs: low · medium · high) |

## 1 · GOAL
{{GOAL}}
*The end state, in one sentence. Example: "Every link in docs/ points somewhere that exists."*

## 2 · DONE WHEN
{{DONE_WHEN}}
*How a machine can tell the goal is reached: the success exit. Example: "The link checker reports 0 broken links, and no file outside docs/ changed."*

## 3 · TRIGGER
{{TRIGGER}}
*By hand · on a goal (`/goal`) · on a schedule · on an event. Example: "Weekly, Monday 7 a.m."*

## 4 · ACTOR
{{ACTOR}}
*The agent, the model, and exactly which tools it may use. Example: "Claude Code, allowed to read and edit docs/ and run the link checker."*

## 5 · CONTEXT
{{CONTEXT}}
*What each run reads first. Example: "PROMPT.md, progress.md, the checker's last report."*

## 6 · CHECKER
{{CHECKER}}
*Who checks, how, and the default answer ("not yet"). Add the CALC-1 estimate. Example: "The link-check script (deterministic). Trust about 99% (F close to 0)."*

## 7 · STATE
{{STATE}}
*What gets written down between runs, and where. Example: "progress.md, one commit per fixed link on branch loop/docs-links, loop-log.csv."*

## 8 · LIMITS
| Family | Rule |
|---|---|
| DONE | {{DONE_RULE}} (example: the checker exits 0) |
| CAP | {{MAX_ITERS}} iterations (from CALC-2) · {{MAX_MINUTES}} minutes · ceiling {{CEILING_PER_RUN}} per run (from CALC-3, current prices) |
| STUCK | the same failure {{STUCK_LIMIT}} times in a row (example: 3) |
| DANGER | {{PROTECTED_FILES}} change, or {{RISKY_ACTION}} is attempted (example: tests/ and check.sh; any push) |
| HUMAN | {{STOP_FILE}} exists (example: `.loop-stop`), or checkpoint: {{CHECKPOINT}} (example: you approve before anything merges) |

## 9 · ESCALATION
{{ESCALATION}}
*Who gets called, with what evidence: the goal, why it stopped, what it tried, the last checker message and diff, and its best guess, marked as a guess.*

## Changelog
| Version | Date | What changed, and why |
|---|---|---|
| {{VERSION}} | {{DATE}} (example: 2026-09-24) | First version |

---

# Filled example: CS-1 · `fix-tests` v2.0

*ILLUSTRATIVE. The story behind it, including what went wrong in v1, is in the [Case Study Lab](../07-case-study-lab.md). Layer: this is a **Loop** design.*

| Header | |
|---|---|
| Name | `fix-tests` |
| Version | v2.0 |
| Owner | you |
| Autonomy rung | 3, act with approval (changes land on a branch; you merge) |
| Risk level | medium (API spend, and changes to working code) |

## 1 · GOAL
Every test in `tests/` passes on branch `loop/fix-tests`.

## 2 · DONE WHEN
`pytest -q` exits 0, **and** no file under `tests/` has changed, **and** the reviewer agent approves the diff.

## 3 · TRIGGER
By hand, in the evening, with `loop.sh`.

## 4 · ACTOR
Claude Code in headless mode (`claude -p`), allowed to read and edit files and run only `pytest` and `git diff` (⚠VERIFY the `--allowedTools` syntax).

## 5 · CONTEXT
`PROMPT.md`, `progress.md`, `check-output.txt` (the checker's last message), and `git log --oneline -5`.

## 6 · CHECKER
`check.sh` runs `pytest -q`; `loop.sh` stops with DANGER if anything in `tests/` or `check.sh` changes (`PROTECT`); then a reviewer subagent with its own rubric reads the diff ("no skipped tests, no special cases, the fix matches the test's intent"). Default: NOT YET.
CALC-1, calibrated on 40 known-good and 40 known-bad past changes: S = 38 ÷ 40 = 0.95, F = 1 ÷ 40 = 0.025, and p = 0.40 → 0.38 ÷ (0.38 + 0.015) = 0.38 ÷ 0.395 = **0.962, about 96%**.

## 7 · STATE
`progress.md`, one commit per iteration on `loop/fix-tests`, and `loop-log.csv`.

## 8 · LIMITS
| Family | Rule |
|---|---|
| DONE | `check.sh` exits 0 and the reviewer approves |
| CAP | 5 iterations (CALC-2: p = 0.4, C = 0.90 → 4.51 → 5) · 20 minutes · ceiling $0.90 per run (CALC-3 with invented prices: 5 × $0.18) |
| STUCK | the same failure 3 times in a row |
| DANGER | any change under `tests/` or to `check.sh` |
| HUMAN | `.loop-stop` exists |

## 9 · ESCALATION
The loop writes `escalation.md`: the goal, the stop family and rule, one line per attempt, the last checker message, the last diff summary, and its best guess, marked as a guess. You read it and decide.

## Changelog
| Version | Date | What changed, and why |
|---|---|---|
| v1.0 | 2026-09-10 | A single prompt: "Fix the failing tests. Keep going until everything passes." No caps. |
| v2.0 | 2026-09-14 | All nine boxes: protected tests, a reviewer agent, five stop families, a branch. After v1 "passed" by skipping a test. |
