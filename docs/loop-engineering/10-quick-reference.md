# Quick Reference

⬅ [Calculator Toolkit](09-calculator-toolkit.md) · 🏠 [README](README.md) · [Glossary](11-glossary.md) ➡

![Poster: loop engineering on one page. The core cycle of trigger, plan, act, observe, verify, and decide, with state written after every turn; the five stop families with exit codes (DONE 0, CAP 2, STUCK 3, HUMAN 4, DANGER 5); the nine boxes of the Loop Spec; the four-rung autonomy ladder, with money, health, legal, and production work stopping at rung 3; and the four calculator formulas.](assets/poster.svg)

**The poster.** *What to notice:* everything on it has a home in the guide. Use the IDs below to jump back to the lesson.

---

## The loop build checklist

| # | Step | Taught in |
|---|---|---|
| 1 | Write the one-paragraph goal: what, why, how often | [Level 1](01-level-1-starter.md) |
| 2 | Rewrite it as an end state a machine can check (DONE WHEN) | [Level 1](01-level-1-starter.md) |
| 3 | Pick the trigger, the actor, and the autonomy rung | [Level 1](01-level-1-starter.md) |
| 4 | Choose the checker, make "not yet" its default, and estimate its trust with CALC-1 | [Level 2](02-level-2-apprentice.md) |
| 5 | Write the stop rules and the escalation; set the cap with CALC-2 | [Level 3](03-level-3-engineer.md) |
| 6 | Decide where state lives and how the loop is isolated | [Level 3](03-level-3-engineer.md) |
| 7 | Write `PROMPT.md` and do a dry run | [Level 4](04-level-4-author.md) |
| 8 | Set the budget with CALC-3, using current prices | [Level 4](04-level-4-author.md) |
| 9 | Run it small, log every iteration, and read the log | [Level 5](05-level-5-expert.md) |
| 10 | Score it with CALC-4, fix every criterion below 4, and version it | [Level 5](05-level-5-expert.md) |

Or let the [Loop Generator](kit/loop-generator.prompt.md) draft all ten, and review what it gives you ([Level 6](06-level-6-hero.md)).

## The nine boxes of the Loop Spec

**GOAL** (the end state) · **DONE WHEN** (a machine can tell) · **TRIGGER** (you, a goal, a schedule, an event) · **ACTOR** (agent, model, allowed tools) · **CONTEXT** (what each run reads first) · **CHECKER** (separate; "not yet" by default) · **STATE** (files, commits, run log) · **LIMITS** (the five stop families) · **ESCALATION** (who's called, with what evidence). Header: name, version, owner, autonomy rung, risk level. Template: [`kit/LOOP-SPEC.md`](kit/LOOP-SPEC.md).

## The core cycle

trigger → plan → act → observe → verify → decide (continue, retry, escalate, or stop), with state written down after every turn.

## The five stop families

| Family | Stops when | `loop.sh` exit code |
|---|---|---|
| DONE | The checker passes, with evidence | 0 |
| CAP | Iterations, spend, or time run out | 2 |
| STUCK | The same failure N times in a row | 3 |
| HUMAN | The stop file appears, or a checkpoint is due | 4 |
| DANGER | A risky action, or a protected file changed | 5 |

Exit code 1 means the script itself hit an error.

## The autonomy ladder

| Rung | May | Climb to the next rung when (adjustable) |
|---|---|---|
| 1 · Watch | Read and report | Two weeks of accurate reports |
| 2 · Suggest | Propose; you apply | A week of accepted suggestions · CALC-4 ≥ 75 |
| 3 · Act with approval | Change its own branch or outbox; you approve | 20+ approved runs, 0 reverts · trust ≥ 95% · CALC-4 ≥ 90 |
| 4 · Act alone | Act within caps; you review after | Stay only while the numbers hold |

**Money, health, legal, and production work stops at rung 3.**

## The four calculators

| Calculator | Formula | Rule of thumb |
|---|---|---|
| CALC-1 Verifier Trust | Trust = p·S ÷ (p·S + (1 − p)·F) | 95%+ to run unattended |
| CALC-2 Tries-to-Success | tries = ⌈ln(1 − C) ÷ ln(1 − p)⌉ | Over 15? Fix the checker or shrink the step |
| CALC-3 Loop Budget | ceiling per run = N × (Tin·Pin + Tout·Pout) ÷ 1,000,000 | Current prices only ⚠VERIFY |
| CALC-4 Loop Scorecard | 3 × (r1 + r2 + r3 + r4) + 2 × (r5 + r6 + r7 + r8) | 75+ unattended · 90+ for rung 4 |

Worksheets: [Calculator Toolkit](09-calculator-toolkit.md) · live formulas: [workbook](workbook/loop-engineering-workbook.xlsx).

## The five numbers that matter

Success rate · iterations per success · cost per success · human interventions per run · false-pass rate (from spot checks).

## Top ten best practices

| ID | Practice |
|---|---|
| BP-0.2 | Write the check before the first prompt |
| BP-1.1 | Write the goal as an end state a machine can check |
| BP-1.2 | Give every loop two exits: success and failure |
| BP-2.1 | Separate maker and checker |
| BP-2.2 | Make "not yet" the checker's default |
| BP-3.1 | Give every loop all five stop families |
| BP-3.2 | Keep state in files, not in the model's memory |
| BP-4.2 | Dry run first, every time you change the loop |
| BP-5.2 | Change one thing at a time, measured on a fixed task set |
| BP-6.1 | Keep the outer loop human |

## Top ten things to avoid

| ID | Mistake |
|---|---|
| AVD-0.1 | The endless polish loop (no done condition) |
| AVD-1.1 | A goal that describes work instead of a state |
| AVD-1.2 | Looping on something you can't undo |
| AVD-2.1 | Letting the maker grade itself |
| AVD-2.2 | The weakened test (gaming the check) |
| AVD-3.1 | The loop with no failure exit |
| AVD-4.2 | Real mode as the default |
| AVD-4.3 | A loop that reads the internet and can push to your repo |
| AVD-5.3 | Silent failure: the loop that stopped logging |
| AVD-6.3 | Climbing the autonomy ladder too fast |

## Before any real run

Use the safety checklist in [`kit/README.md`](kit/README.md#before-a-real-run-the-safety-checklist): its own branch, caps from CALC-2 and CALC-3, protected checker files, least-privilege tools, no permission-skipping outside a disposable container, secrets out of prompts, a known off switch, and the rung-3 ceiling for money, health, legal, and production.

⬅ [Calculator Toolkit](09-calculator-toolkit.md) · 🏠 [README](README.md) · [Glossary](11-glossary.md) ➡
