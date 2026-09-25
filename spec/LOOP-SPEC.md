# Loop Spec: kjv-chapter-bible-study-loop

A formal Loop Specification designed according to the standards of *Loop Engineering: From Zero to Hero* (`docs/loop-engineering`).

| Header | Specification |
|---|---|
| Name | `kjv-chapter-bible-study-loop` |
| Version | `v1.0` |
| Owner | Thomas Perdana (Cash in Blue LLC) |
| Autonomy rung | `2 suggest` / `3 act with approval` (Rung 2 for human doctrinal review before teaching; Rung 3 for unattended generation to branch) |
| Risk level | `medium` (doctrinal accuracy in public teaching; API budget management) |

---

## 1 · GOAL
Generate an exhaustive, print-ready, 19-point KJV Bible study and Berean Council interactive workbook for each of the 1,189 chapters of the Holy Bible, from Genesis 1 through Revelation 22, synthesizing KJV 7.2 (Berean Council Flywheel & Detailed Doctrines) and KJV 8.2 (19-Point Workbook Builder & Question Ladder).

---

## 2 · DONE WHEN
A chapter study is marked **DONE** when and only when:
1. `verse_checker.py` reports **0 Scripture quote mismatches** against the canonical `data/kjv.json` database.
2. `structure_checker.py` confirms all **19 template points**, all **7 Berean scholar briefs**, all **5 question ladder tiers**, all **9 systematic doctrinal heads**, both **Humility/Life/Light practice sets**, both **Planners**, and both **Theological Guards** (Abundance Guard & Love Guard) are present and conformant.
3. `laya_judge.py` non-autoregressive decision engine passes the text:
   - `doctrinal_soundness`: score ≥ 2 ("sound and deep")
   - `kjv_faithfulness`: noul ≥ 0.85
   - `life_light_practicality`: choice == "actionable"
   - `humility_posture`: choice == "Christ-magnifying"
4. The verified markdown document is saved to `studies/{TESTAMENT}/{BOOK_ID}_{BOOK}/{BOOK}_{CHAPTER}.md`.
5. The overall loop is **DONE** when all 1,189 chapters in `progress/progress.json` transition from `pending` to `completed`.

---

## 3 · TRIGGER
- **Full Bible Loop**: Run via CLI `./scripts/run_loop.sh --all` (iterates sequentially from Genesis 1 to Revelation 22 with auto-resume).
- **Targeted Run**:
  - By Chapter: `./scripts/run_loop.sh --chapter "Romans 8"` or `--chapter "Genesis 1"`
  - By Book: `./scripts/run_loop.sh --book "John"`
  - By Testament: `./scripts/run_loop.sh --testament "NT"`
- **Practice / Dry Run**: `DRY_RUN=1 ./scripts/run_loop.sh --chapter "Genesis 1"` (uses mock generation with zero API spend).

---

## 4 · ACTOR
- **Engine**: Generation actor (`engine/generator.py`).
- **Permissions**: Read-only access to `data/`, `prompts/`, `spec/`, and `verifier/`. Write access strictly scoped to `studies/` and `progress/`. Network access restricted to model API.
- **Master Prompt**: Executes `prompts/kjv_master_prompt.md` with target chapter metadata and verbatim Scripture injected.

---

## 5 · CONTEXT
Each iteration injects:
1. Canonical chapter verses extracted directly from `data/kjv.json`.
2. Synthesized Master Prompt (`prompts/kjv_master_prompt.md`).
3. Evaluation Rubric (`prompts/rubric.md`).
4. Feedback from previous failed iteration (if retrying a chapter).

---

## 6 · CHECKER (MAKER/CHECKER SEPARATION & CALC-1)
Three independent checker layers (the maker NEVER grades its own work):

1. **Deterministic Scripture Verifier (`verifier/verse_checker.py`)**:
   - Parses every quoted verse with a reference tag.
   - Matches against `data/kjv.json` word-for-word and punctuation-for-punctuation.
   - CALC-1 Trust: S = 1.0, F = 0.001. Deterministic match guarantees essentially zero quote corruption.
2. **Structural Conformance Verifier (`verifier/structure_checker.py`)**:
   - Validates that the 19 points, 7 council seats, 5 question levels, and 9 doctrinal heads exist and meet minimum depth requirements.
3. **Laya System 1 Decision Engine (`verifier/laya_judge.py`)**:
   - Fast (33 ms) non-autoregressive classifier evaluating semantic adherence to Reformed doctrine, Christ-centered humility, and actionable Life/Light pathways.
   - Avoids expensive autoregressive evaluator loops.

Default Checker Answer: **NOT YET**.

---

## 7 · STATE
- `progress/progress.json`: Machine-readable state matrix of all 1,189 chapters (`pending`, `in_progress`, `completed`, `failed`, retry count, verification metrics).
- `progress/progress.md`: Formatted human-readable dashboard showing progress by Testament and Book.
- `progress/loop-log.csv`: Standard loop engineering run log recording `iteration, started_at, action, check_result, stop_reason, tokens_in, tokens_out, diff_lines, note`.
- `studies/{TESTAMENT}/{BOOK_ID}_{BOOK}/{BOOK}_{CHAPTER}.md`: Persistent generated chapter studies.

---

## 8 · LIMITS (FIVE STOP FAMILIES)

| Family | Rule |
|---|---|
| **DONE** | All 3 checkers exit 0 for the target chapter; or all 1,189 chapters completed. |
| **CAP** | **Iteration Cap**: Max 3 retries per chapter (CALC-2: p=0.75, C=0.95 -> 3 tries).<br>**Time Cap**: Max 10 minutes per chapter.<br>**Cost Ceiling**: $0.25 per chapter ceiling (CALC-3). |
| **STUCK** | Identical verification failure 3 times in a row halts that chapter, marks it `failed` in `progress.json`, logs escalation, and alerts operator. |
| **DANGER** | If any protected file (`data/kjv.json`, `prompts/*`, `verifier/*`, `scripts/*`) changes during actor execution, the loop terminates immediately with exit code 5. |
| **HUMAN** | If `.loop-stop` exists in root, the loop gracefully completes the current chapter and exits with code 4. |

---

## 9 · ESCALATION
When a chapter fails after reaching its retry cap or gets stuck:
- Details are appended to `progress/escalations.md` containing:
  - Book and Chapter reference.
  - Number of attempts made.
  - Specific failing quotes and diff against canonical KJV.
  - Missing structural components or Laya scores below threshold.
- The loop continues to the next chapter unless run with `--halt-on-error`.
