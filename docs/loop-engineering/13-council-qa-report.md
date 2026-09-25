# Council QA Report

⬅ [Sources](12-sources.md) · 🏠 [README](README.md) · [Level 0](00-level-0-zero.md) ➡

*RAZOR and GOVERNOR lead. This is the build's honest self-assessment: what was delivered, how it was checked, what's still unverified, and where it falls short.*

Build: LOOP-FORGE v1.0 (`docs/prompt.1.md`), DEPTH `complete`, autopilot, run on September 24, 2026 by an AI agent with file tools in a Linux cloud session. The full record of every item, check, erratum, and shakedown finding is in [`BUILD-LOG.md`](BUILD-LOG.md).

---

## 1 · Coverage

| Component or artifact | Target (complete) | Delivered | Where |
|---|---|---|---|
| Best Practices | 21 | 21 (3 per level) | Levels 0–6 |
| Tips | 21 | 21 (3 per level) | Levels 0–6 |
| Tricks | 14 | 14 (2 per level) | Levels 0–6 |
| Hacks | 7 | 7 (1 per level) | Levels 0–6 |
| Things to Avoid | 21 | 21 (3 per level) | Levels 0–6 |
| Examples | 14 | 14 (2 per level) | Levels 0–6 |
| Case Studies | CS-1, CS-2, CS-3 + CS-META | All four | [Case Study Lab](07-case-study-lab.md) |
| FAQ | 30 | 30, each 120 words or fewer | [FAQ](08-faq.md) |
| Calculators | 4 | 4, with worksheets, spreadsheet formulas, and checksums | Levels 2–5, [Toolkit](09-calculator-toolkit.md) |
| Figures | 23 (cover + poster + 21) | 23 SVG files | [`assets/`](assets/) |
| Workbook sheets | 7 | 7, plus one CSV per sheet | [`workbook/`](workbook/) |
| Kit files | 6 | 6 | [`kit/`](kit/) |

Total: about 33,000 words across the README and the 14 chapter files (this report included), above the 25,000–30,000 target for `complete`: the item counts at this depth need the room. The largest file (Level 4) is about 3,900 words, inside the 5,000-word file budget.

## 2 · Definition of Done check

| The guide promised that a reader can… | Where that's taught and practiced |
|---|---|
| 1. explain loop engineering, including its lineage from prompt, context, and harness engineering | [Level 0](00-level-0-zero.md) (FIG-0.2, the working definition, a dated history), FAQ-1, FAQ-5 |
| 2. turn a one-paragraph goal into a one-page Loop Spec with a checkable done condition, a separate checker, stop rules, a budget, state, and escalation | [Level 1](01-level-1-starter.md) (the nine boxes), [Levels 2–4](02-level-2-apprentice.md), [`kit/LOOP-SPEC.md`](kit/LOOP-SPEC.md), the [Loop Generator](kit/loop-generator.prompt.md) |
| 3. run a first loop safely and read its log | [Level 4](04-level-4-author.md) (the `loop.sh` walkthrough and five dry-run demos), [Level 5](05-level-5-expert.md) (the run log and workbook Run Log sheet) |
| 4. score a loop on CALC-4, reach 75 or higher, and fix what's weak | [Level 5](05-level-5-expert.md) (CALC-4, worked examples at 20, 89, and 62), the Case Study Lab (v1 → v2 in every case) |

## 3 · Checks run

| Check | Method | Result |
|---|---|---|
| Links and images | A script resolved every relative link, image, and anchor in all 22 markdown files | All resolve |
| Manifest | Every file in `MANIFEST.md` exists, and every file on disk is listed | Clean |
| Figures, level 1 | `xmllint` on all 23 SVGs | All parse |
| Figures, level 2 | Every SVG rendered with headless Chromium on a dark page and looked at | 15 of 23 needed a fix (text collisions, overflow, or low contrast); all fixed and re-rendered |
| Figure text | Alt text on every embed (40+ characters); a caption with "What to notice" on all 21 level figures | Pass |
| IDs and counts | A script counted every item per level and checked every cited ID | Counts exact; 98 cited IDs, none dangling; no ID defined twice |
| Calculators | Every worked example recomputed in Python before writing | All match the checksums |
| Workbook | LibreOffice was installed as `libreoffice-core` only, with no Calc module, so it couldn't open spreadsheets. Every formula in the saved file was evaluated with the `formulas` Python engine instead | 53 of 53 checksum checks pass, plus the ROUNDUP whole-number guard on 4 cases |
| Starter kit | `bash -n`; ShellCheck 0.11; five dry-run demos from a fresh copy of the final kit; a real-mode test with plain shell commands | Clean; all exits correct (transcript below) |
| Templates | Scanned for "…" gaps and TODOs; checked that every placeholder has an example | No gaps. Examples were missing for 27 placeholders (8 in `PROMPT.md`, 17 in `progress.md`, 2 in `LOOP-SPEC.md`); all added, and a coverage script now confirms none is missing |
| FAQ | Word count per answer | All 30 at 120 words or fewer |

**Kit dry-run transcript** (fresh copy of the final `kit/`, bash 5.2 on Linux):
```text
DONE   MOCK_PASS_AT=3                        → exit 0 · DONE on iteration 3: PASS: all checks green
CAP    MOCK_PASS_AT=99                       → exit 2 · CAP: 5 iterations used without a pass
STUCK  MOCK_STUCK=1                          → exit 3 · STUCK: the same failure 3 times in a row: FAIL: test_refund_rounding expected 10.01, got 10.00
HUMAN  (with .loop-stop present)             → exit 4 · HUMAN: .loop-stop found, stopping before iteration 1
DANGER MOCK_TAMPER=1 PROTECT=fake-check.sh   → exit 5 · DANGER: a protected file changed on iteration 1
```

**Errata fixed during the build:** HCK-2.1's snippet used exit code 3 (STUCK) for DANGER; it now uses 5. Level 4 told the agent to report DONE; it now reports only NOT YET or STUCK, because the checker decides DONE.

## 4 · ⚠VERIFY list

Every version-sensitive statement in the guide, grouped by where to confirm it:

| What | Where it appears | Confirm at |
|---|---|---|
| The term's history: Steinberger's post, Osmani's essay, Cherny's quote, the arXiv paper, IBM's definition, Sonar's title | Level 0, Level 2, FAQ-1, [`12-sources.md`](12-sources.md) | The source links in `12-sources.md` (these weren't opened during the build) |
| Wording quoted from Anthropic's loops guide | Level 0, Level 2, Level 6 | https://claude.com/blog/getting-started-with-loops |
| `/goal`: the evaluator, condition advice, turn clauses, the no-progress stop, `/goal clear` | Levels 1–4, FAQ-9, FAQ-16, FAQ-17, Glossary | https://code.claude.com/docs/en/goal |
| `/loop`: intervals, self-pacing, 7-day expiry, Esc; cloud routines and desktop tasks | Levels 1, 3, 4, 6, FAQ-16, FAQ-17, Glossary | https://code.claude.com/docs/en/scheduled-tasks |
| `claude -p` flags: `--allowedTools`, permission modes, `--bare`, `--output-format json` and `total_cost_usd`, `--dangerously-skip-permissions` | Level 4, kit files, FAQ-19, FAQ-21 | https://code.claude.com/docs/en/headless and the CLI reference |
| Hooks: the Stop-hook block format, the 8-block cap, `PreToolUse` denies in bypass mode | Levels 2–4, Glossary | https://code.claude.com/docs/en/hooks-guide |
| The Ralph loop plugin: `/ralph-loop`, `--max-iterations` defaulting to unlimited | Levels 3–4, FAQ-18 | The plugin README (link in `12-sources.md`) |
| Auto mode, skills, subagents, MCP connectors | Level 4, Glossary | Claude Code docs |
| Prices, prompt-caching discounts, subscription usage limits | Level 4 (CALC-3), Toolkit, workbook, FAQ-21 | Anthropic's current pricing and plan pages |
| Broker export formats | CS-3 | Your own broker's documentation |

## 5 · FIELD WORK list (yours)

1. **Current prices** per million input and output tokens, entered in the workbook's CALC-3 "Yours" column. Every example in the guide uses invented prices ($4 and $20), labeled as invented.
2. **A hand-graded sample** (10 good and 10 bad outputs, or more) for each checker you build, to measure S and F for CALC-1.
3. **For CS-2:** a plain-text, public-domain KJV file, if you want the verse checker to run for real.
4. **For CS-3:** your own broker export and your own written rules. Paper-trade first. This guide isn't financial advice.
5. **Clear the ⚠VERIFY list** above against current documentation before relying on any tool detail.

## 6 · Known limitations

1. **The writing was checked by the model that wrote it.** Deterministic checks covered the artifacts (figures, workbook, script, links, counts), but the red-team and clarity passes on the prose were done by the same agent that wrote it. CS-META scores this honestly (checker: 3 of 5). A fresh reviewer, human or agent, should read the chapters.
2. **Some history is second-hand.** Several sources on the term's origin couldn't be opened from the build environment. They're paraphrased, dated loosely, and marked ⚠VERIFY.
3. **The workbook was verified by a formula engine, not by Excel, Google Sheets, or LibreOffice Calc.** The formulas are standard, but app-specific behavior (formatting, CSV formula import) wasn't tested in those apps.
4. **`loop.sh` was tested on bash 5.2 (Linux).** It avoids bash-4-only features by design and passes ShellCheck, but it wasn't run on macOS's bash 3.2.
5. **Figures were rendered on Linux with its default fonts.** The system font stack may lay out slightly differently on macOS or Windows.
6. **The case studies are illustrative.** Their people, logs, and numbers are invented to teach design lessons. Only CS-META describes real events (this build).

## 7 · First practice runs

1. **`BUILD-LOOP`** with the [Loop Generator](kit/loop-generator.prompt.md): *"Every Sunday night, check next week's small-group lesson file for a Scripture reference on every quotation, three discussion questions, and a closing prayer. Suggest fixes; never publish without me."* Expect rung 2, a deterministic checker, and a CAP from CALC-2.
2. **`GRADE-LOOP`** on CS-1's v1 (from the [Case Study Lab](07-case-study-lab.md)). Paste the one-line prompt and its missing boxes; you should land near 20 / 100. Then do the same for v2 (about 89).
3. **`BUILD-LOOP`** for a publishing chore of your own: *"Each time I add a coloring-book draft to `drafts/`, check that the listing file has every field my template requires, and list what's missing."* Keep it at rung 1 or 2, and write the template's required fields yourself; marketplace rules change, so ⚠VERIFY any platform limit.

## Shakedown findings for LOOP-FORGE (the prompt that built this guide)

This run doubled as the prompt's first live test. Its findings, recorded in `BUILD-LOG.md`, feed LOOP-FORGE v1.1:
- **SF-1:** the kit spec gave DANGER no exit code (now 5).
- **SF-2:** "if LibreOffice is installed" isn't the right test (check for Calc with a tiny CSV, and name a second formula engine).
- **SF-3:** the kit spec asked `PROMPT.md` to let the agent say DONE, contradicting maker/checker.

CS-META adds two design fixes: run the red-team and clarity passes in a fresh subagent, and give the build its own STUCK rule and rewrite budget.

⬅ [Sources](12-sources.md) · 🏠 [README](README.md) · [Level 0](00-level-0-zero.md) ➡
