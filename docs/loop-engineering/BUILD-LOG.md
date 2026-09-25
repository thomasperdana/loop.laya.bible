# BUILD-LOG — the build's memory

Run by LOOP-FORGE v1.0 (`docs/prompt.1.md`). Settings: DEPTH `complete` · DELIVERY `autopilot` · ENVIRONMENT `agent` · FIGURE STYLE `svg` · LANGUAGE English · OUTPUT FOLDER `docs/loop-engineering/`.

A fresh session resumes from the first item that isn't `checked`. Status values: `todo` · `written` · `checked`.

**Build status: CLOSED.** All 20 items checked on 2026-09-24. See `13-council-qa-report.md` for the summary.

## Checklist

| # | Item | Status | Checks |
|---|---|---|---|
| 1 | `MANIFEST.md` | checked | every listed file exists; every file on disk is listed |
| 2 | `BUILD-LOG.md` | checked | resumable record of every item, check, erratum, and finding |
| 3 | `README.md` + `assets/cover.svg` | checked | cover: XML ok, rendered + viewed (contrast fix); links resolve |
| 4 | `00-level-0-zero.md` + FIG-0.1–0.3 | checked | 3 figs: XML ok, rendered + viewed (2 layout fixes) |
| 5 | `01-level-1-starter.md` + FIG-1.1–1.3 | checked | 3 figs: XML ok, rendered + viewed (1 label fix) |
| 6 | `02-level-2-apprentice.md` + FIG-2.1–2.3 | checked | 3 figs: XML ok, rendered + viewed (label plates, chart labels moved); CALC-1 checksums match |
| 7 | `03-level-3-engineer.md` + FIG-3.1–3.3 | checked | 3 figs: XML ok, rendered + viewed (overflow + callout fixes); CALC-2 checksums match |
| 8 | `04-level-4-author.md` + FIG-4.1–4.3 | checked | 3 figs: XML ok, rendered + viewed (label + card fixes); CALC-3 checksums match; loop.sh excerpt verbatim |
| 9 | `05-level-5-expert.md` + FIG-5.1–5.3 | checked | 3 figs: XML ok, rendered + viewed (glyph + label fixes); CALC-4 scores 20/89/62 verified |
| 10 | `workbook/` (xlsx + 7 CSVs) | checked | 7 sheets + 7 CSVs; formulas evaluated with the 'formulas' engine: 53/53 checks + guard test 4/4 (LibreOffice Calc unavailable) |
| 11 | `06-level-6-hero.md` + FIG-6.1–6.3 | checked | 3 figs: XML ok, rendered + viewed (spacing + ladder rebuilt); kit links checked in item 20 |
| 12 | `kit/` (6 files) | checked | 6 files: shellcheck clean; 5 dry-run exits verified from a fresh copy; no gaps; every placeholder has an example |
| 13 | `07-case-study-lab.md` | checked | 4 case studies, ILLUSTRATIVE; every number recomputed in Python; CS-META figure count verified (15 of 23) |
| 14 | `08-faq.md` | checked | 30 entries, all ≤120 words, answer first |
| 15 | `09-calculator-toolkit.md` | checked | 4 worksheets + formulas + checksum table; no lessons repeated |
| 16 | `10-quick-reference.md` + `assets/poster.svg` | checked | poster: XML ok, rendered + viewed (banner collision fixed) |
| 17 | `11-glossary.md` | checked | every defined term, with its level |
| 18 | `12-sources.md` | checked | opened vs reported sources separated; ⚠VERIFY kept on reported ones |
| 19 | `13-council-qa-report.md` | checked | coverage, DoD, checks, ⚠VERIFY, FIELD WORK, 6 limitations, practice runs; its own counts re-verified (2 corrected) |
| 20 | Whole-folder pass: links, images, IDs, counts, checksums | checked | folder_check.py: ALL PASS (links, manifest, 23 SVGs, IDs, counts, FAQ, sections, nav, labels, budgets) |

## Checks run

- README + cover.svg: cover parsed with xmllint, rendered with headless Chromium on a dark page, text contrast fixed (dark text tones added) before release.
- Level 0: FIG-0.1–0.3 parsed and rendered; fixed a label collision (FIG-0.1) and an icon overlap (FIG-0.3).
- Level 1: FIG-1.1–1.3 parsed and rendered; shortened one wrapped label in FIG-1.1. Replaced a personal name in EX-1.2 with 'you'.
- Level 2: FIG-2.1–2.3 parsed and rendered; label plates added so lifelines pass behind text; FIG-2.3 labels moved off the curves; CALC-1 numbers (0.659 / 0.951 / 0.818) match the Python checksums. HCK-2.1 exit code corrected to 5 (DANGER), see SF-1.
- Level 3: FIG-3.1–3.3 parsed and rendered; fixed text overflow in two exit boxes and moved chart callouts into a legend; CALC-2 numbers (5 tries/0.969; 11 tries/0.914; practice 4.51→5) recomputed.
- Level 4: FIG-4.1–4.3 parsed and rendered; card text shortened to two lines; CALC-3 ($0.12 / $0.24 / $0.60 / $18.00 / 15 min) matches; the settings excerpt matches kit/loop.sh line for line. kit/loop.sh built early (Level 4 walks through it): bash -n ok, shellcheck 0.11 clean, dry-run demos DONE 0 · CAP 2 · STUCK 3 · HUMAN 4 · DANGER 5, guards exit 1, real-mode test with shell commands DONE on iteration 3.
- Level 5: FIG-5.1–5.3 parsed and rendered; moved one glyph off its curve and moved the weights note into the subtitle; CALC-4 scores (CS-1 v1 20, v2 89, kit default 62) and TIP-5.2 costs ($0.37 per run, $0.53 per success) recomputed.
- Workbook: built with openpyxl (throwaway venv). LibreOffice is installed as libreoffice-core only (no Calc module), so it can't open spreadsheets; verified instead by evaluating every formula in the saved file with the 'formulas' Python engine: CALC-1 0.659/0.951/0.818, CALC-2 5/0.969 · 11/0.914 · 5/0.922, CALC-3 0.12/0.24/0.60/18.00/15, CALC-4 20/89/62 with bands, Run Log costs and summary; plus the ROUNDUP whole-number guard on 4 cases. All pass.
- Level 6: FIG-6.1–6.3 parsed and rendered; fixed column collision and footer overflow (FIG-6.1); rebuilt FIG-6.3 as an indented ladder so the evidence labels fit. TIP-6.3 alerts ($9.00 / $14.40) recomputed.
- Kit: README, LOOP-SPEC (template + CS-1 v2.0 filled), PROMPT, progress, loop.sh, loop-generator.prompt.md. loop.sh re-tested from a fresh copy of the final kit: DONE 0 · CAP 2 · STUCK 3 · HUMAN 4 · DANGER 5 (transcript in the QA report). No '…' gaps or TODOs; placeholder examples were missing for 27 placeholders (8 in PROMPT.md, 17 in progress.md, 2 in LOOP-SPEC.md, the last 2 caught by a coverage script); all added.
- Case Study Lab: CS-1 trust 0.679/0.962, cap 5 (0.922), $0.18/$0.45/$0.90/$18.00; CS-2 trust 0.889, cap 4 (0.974), $0.098/$0.392/$2.35; CS-3 trust 0.996, cap 4 (0.992), $0.062/$0.248/$5.21; scores 20/89, 31/86, 12/91, CS-META 79. CS-1 calibration changed to a 40 + 40 sample (F = 1/40) because F = 0.03 was impossible from 20 samples; kit and Level 5 aligned.
- Whole-folder pass: links and anchors resolve in 22 markdown files; manifest matches disk; 23 SVGs parse and are embedded with alt text; per-level counts exact at complete depth; 98 cited IDs, none dangling; 30 FAQ ≤120 words; template sections present; every chapter has nav lines; case studies labeled; largest file 3,938 words; about 33,000 words total.

## Errata

- **BUILD-LOG.md itself · Checks run:** four lines had dollar amounts mangled by shell expansion when they were logged (`$0.12` became `/bin/bash.12`); restored from the verified values.
- **Level 2 · HCK-2.1:** the DANGER snippet exited with code 3 (STUCK's code); changed to 5, matching kit/loop.sh.
- **Level 4 · PROMPT.md Report section and EX-4.1:** told the agent to end with DONE; changed to `STATUS: NOT YET` or `STATUS: STUCK`, since only the checker decides DONE (Level 2's maker/checker rule, and kit/PROMPT.md).

## Shakedown findings for LOOP-FORGE (feed into v1.1)

- **SF-1 · DANGER has no exit code.** §7.3 defines exits for DONE 0, CAP 2, STUCK 3, HUMAN 4 (1 = error) but the five stop families also include DANGER. This build uses exit 5 for DANGER (a protected checker file changed).
- **SF-2 · "If LibreOffice is installed" isn't the right test.** §7.2 says to recalculate with LibreOffice when it's installed. Here only `libreoffice-core` was present (no Calc), so `soffice` printed its version but couldn't open any spreadsheet. v1.1 should say: test with a two-line CSV first, and name a second engine (the `formulas` Python package) before falling back to hand-recomputed checks.
- **SF-3 · The kit spec tells the agent to say DONE.** §7.3 asks `PROMPT.md` to say "how to say DONE or STUCK", which contradicts the maker/checker rule. This build's `PROMPT.md` reports only `NOT YET` or `STUCK`; the checker decides DONE.
