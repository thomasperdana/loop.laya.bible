# MANIFEST — Loop Engineering: From Zero to Hero

Every file in this folder, what it's for, and where it's used. Built by LOOP-FORGE v1.0 (`docs/prompt.1.md`) at DEPTH `complete`.

## Chapters

| File | Purpose | Used by |
|---|---|---|
| `README.md` | Cover, Start Here, Meet the Council, The Map | Entry point |
| `00-level-0-zero.md` | Level 0 · ZERO: what a loop is, and why prompting by hand runs out | README path |
| `01-level-1-starter.md` | Level 1 · STARTER: design a loop on one page | README path |
| `02-level-2-apprentice.md` | Level 2 · APPRENTICE: check the work (CALC-1) | README path |
| `03-level-3-engineer.md` | Level 3 · ENGINEER: stop rules, state, and isolation (CALC-2) | README path |
| `04-level-4-author.md` | Level 4 · AUTHOR: build and run real loops (CALC-3) | README path |
| `05-level-5-expert.md` | Level 5 · EXPERT: observe, debug, and improve (CALC-4) | README path |
| `06-level-6-hero.md` | Level 6 · HERO: loop systems and meta-loops | README path |
| `07-case-study-lab.md` | CS-1, CS-2, CS-3, CS-META (all ILLUSTRATIVE) | Levels 1–6 cite it |
| `08-faq.md` | FAQ-1 to FAQ-30, grouped by level | All levels |
| `09-calculator-toolkit.md` | Blank worksheets and spreadsheet formulas for CALC-1 to CALC-4 | Levels 2–5, workbook |
| `10-quick-reference.md` | Poster, build checklist, nine boxes, stop families, autonomy ladder, top items by ID | Whole guide |
| `11-glossary.md` | Every term the guide defines | Whole guide |
| `12-sources.md` | Sources, marked as opened or reported | Topic history, ⚠VERIFY items |
| `13-council-qa-report.md` | Coverage, checks run, ⚠VERIFY list, FIELD WORK, limitations | Final check |
| `MANIFEST.md` | This file | — |
| `BUILD-LOG.md` | The build's memory: checklist, checks, errata | Resuming a build |

## Figures (`assets/`)

| File | ID and title | Used in |
|---|---|---|
| `cover.svg` | Cover | `README.md` |
| `poster.svg` | Loop engineering on one page | `10-quick-reference.md` |
| `fig-0-1-core-cycle.svg` | FIG-0.1 The core cycle | Level 0 |
| `fig-0-2-four-layers.svg` | FIG-0.2 Four layers: prompt, context, harness, loop | Level 0 |
| `fig-0-3-you-are-the-loop.svg` | FIG-0.3 You have been the loop | Level 0 |
| `fig-1-1-loop-spec.svg` | FIG-1.1 The Loop Spec: nine boxes | Level 1, kit |
| `fig-1-2-loop-worthiness.svg` | FIG-1.2 Is it loop-worthy? Five questions | Level 1 |
| `fig-1-3-four-triggers.svg` | FIG-1.3 Four ways a loop starts | Level 1 |
| `fig-2-1-maker-checker.svg` | FIG-2.1 Maker and checker | Level 2 |
| `fig-2-2-checker-ladder.svg` | FIG-2.2 The checker ladder | Level 2 |
| `fig-2-3-verifier-trust.svg` | FIG-2.3 Trust vs false-pass rate (CALC-1 chart) | Level 2 |
| `fig-3-1-stop-rules.svg` | FIG-3.1 The five stop families | Level 3 |
| `fig-3-2-tries-to-success.svg` | FIG-3.2 Chance of success within n tries (CALC-2 chart) | Level 3 |
| `fig-3-3-fresh-context-state.svg` | FIG-3.3 Fresh context, memory in files | Level 3 |
| `fig-4-1-ralph-pattern.svg` | FIG-4.1 The Ralph pattern | Level 4 |
| `fig-4-2-claude-code-loop-features.svg` | FIG-4.2 Claude Code's loop features | Level 4 |
| `fig-4-3-loop-budget.svg` | FIG-4.3 Typical run, ceiling, and monthly ceiling (CALC-3 chart) | Level 4 |
| `fig-5-1-failure-modes.svg` | FIG-5.1 Failure-mode gallery | Level 5 |
| `fig-5-2-eval-loop.svg` | FIG-5.2 The eval loop | Level 5 |
| `fig-5-3-scorecard-v1-v2.svg` | FIG-5.3 CS-1 scorecard, v1 vs v2 (CALC-4 chart) | Level 5, CS-1 |
| `fig-6-1-loops-of-loops.svg` | FIG-6.1 Loops of loops | Level 6 |
| `fig-6-2-team-shapes.svg` | FIG-6.2 Team shapes | Level 6 |
| `fig-6-3-autonomy-ladder.svg` | FIG-6.3 The autonomy ladder | Level 6, CS-3 |

## Workbook (`workbook/`)

| File | Purpose | Used by |
|---|---|---|
| `loop-engineering-workbook.xlsx` | Seven sheets: README, CALC-1 Verifier Trust, CALC-2 Tries, CALC-3 Budget, CALC-4 Scorecard, Loop Canvas, Run Log | Levels 2–5, `09-calculator-toolkit.md` |
| `csv/1-readme.csv` … `csv/7-run-log.csv` | One CSV per sheet, formulas kept as text | Fallback for any spreadsheet app |

## Starter kit (`kit/`)

| File | Purpose | Autonomy rung |
|---|---|---|
| `kit/README.md` | What each kit file does, the order to use them in, safety notes | — |
| `kit/LOOP-SPEC.md` | The nine-box Loop Spec template, plus a filled version for CS-1 | Any |
| `kit/PROMPT.md` | The per-run loop prompt template | Suggest or higher |
| `kit/progress.md` | The state file template | Any |
| `kit/loop.sh` | A minimal loop runner: dry run by default, hard caps, stop file, CSV log | Watch (dry run) → act with approval |
| `kit/loop-generator.prompt.md` | The Loop Generator: a one-paragraph goal in, a scored loop design out | Design only |
