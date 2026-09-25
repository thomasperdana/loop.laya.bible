# Level 5 · EXPERT: Observe, debug, and improve

⬅ [Level 4](04-level-4-author.md) · 🏠 [README](README.md) · [Level 6](06-level-6-hero.md) ➡

**You'll be able to:**
- keep a run log you can actually debug from, and compute the five numbers that matter;
- diagnose the nine common loop failures from their symptoms;
- improve a loop safely: one change at a time, measured on a fixed task set, with a version number;
- score any loop on the Loop Scorecard (CALC-4) and name the fixes worth the most points.

---

## The Lesson

### A loop you can't see is a loop you can't trust

Once a loop runs without you, its **run log** is how you find out what it did. Log every iteration in the same columns. The kit's `loop.sh` and the workbook's Run Log sheet share these:

| Column | What it records | Why you'll want it |
|---|---|---|
| `iteration` | 1, 2, 3… | Where in the run it happened |
| `started_at` | Time, in UTC | Spotting slow or overlapping runs |
| `action` | What the maker did (`agent`, `mock-agent`, `none`) | Separating real turns from skipped ones |
| `check_result` | `pass`, `fail`, or `skipped` | The checker's verdict |
| `stop_reason` | `DONE`, `CAP`, `STUCK`, `HUMAN`, `DANGER`, or blank | Why the run ended, on its last row |
| `tokens_in`, `tokens_out` | Tokens used, if your agent reports them | Cost (CALC-3) |
| `diff_lines` | Lines changed this iteration | Spotting runaway or empty changes |
| `note` | The last line of the checker's message | Debugging without rerunning |

### The five numbers that matter

From a week of logs, compute:

1. **Success rate** = runs that ended DONE ÷ all runs.
2. **Iterations per success** = total iterations ÷ successful runs.
3. **Cost per success** = total cost ÷ successful runs (TIP-5.2).
4. **Human interventions per run** = escalations plus manual stops ÷ runs.
5. **False-pass rate** = passes that failed your spot check ÷ passes you spot-checked (BP-5.3). This is F from CALC-1, measured for real.

The Run Log sheet computes the first three for you.

### Nine ways loops fail

Every loop failure shows up as a symptom in the log first. Learn to read them:

![FIG-5.1: Nine failure modes, each with a small sketch and its symptom. Runaway: cost keeps climbing. Thrashing: fixing A breaks B and back again. Drift: it solves a neighboring problem. Gaming the check: passes with weakened tests. Premature done: says done, but spot checks fail. Context rot: quality fades as a session grows. Stale state: redoes finished work. Silent failure: all green, but nothing ran. Pile-up: scheduled runs overlap.](assets/fig-5-1-failure-modes.svg)

**FIG-5.1 · Failure-mode gallery.** *What to notice:* none of these is solved by a better prompt alone. Each needs a structural fix: a cap, a check, a file, a lock.

| Failure | Symptom in the log | Likely cause | Fix |
|---|---|---|---|
| **Runaway** | Iterations and cost keep climbing | No CAP or STUCK rule | All five stop families (BP-3.1) and a ceiling (CALC-3) |
| **Thrashing** | Fixing A breaks B, then fixing B breaks A | Turns too big; the check reports one failure at a time | Smaller turns (BP-4.1); run the whole check every turn; record decisions (AVD-5.1) |
| **Drift** | The loop solves a neighboring problem | The goal is vague, or the agent restated it | Goal word for word in `PROMPT.md`; DONE WHEN checked every turn (BP-1.1) |
| **Gaming the check** | Passes arrive with weakened tests or special cases | The maker can touch the checker | `PROTECT` and DANGER (HCK-2.1); a separate verifier (AVD-2.2) |
| **Premature "done"** | "DONE", but spot checks fail | The maker declared success; the judge only read a summary | The checker decides, with evidence (BP-2.2, AVD-5.2) |
| **Context rot** | Quality fades as a long session goes on | The window fills up and gets compacted | Fresh context each run, memory in files (TRK-3.1) |
| **Stale state** | It redoes finished work or reverses a decision | The progress file wasn't written, or wasn't read | Read first, write last, every turn (TIP-3.3) |
| **Silent failure** | The dashboard is green, but nothing ran | The loop crashed before logging, or logs nowhere | Log every iteration; alert when a day has no rows (AVD-5.3) |
| **Pile-up** | Scheduled runs overlap and undo each other | The next run starts before the last one ends | A lock file; an interval longer than the worst-case run; one workspace per loop |

### Evals: the outer loop that improves your loop

Improving a loop is itself a loop, one level up. An **eval** (short for evaluation) is a fixed set of test tasks you run every time you change something, so you can compare versions fairly.

![FIG-5.2: A cycle of four steps: change one thing (the prompt, the checker, the cap, or the model); run the golden set of about ten fixed tasks; compare success rate, iterations per success, cost per success, and false passes against the last version; then keep it, with a version bump and changelog line, or revert it. An arrow returns to the first step.](assets/fig-5-2-eval-loop.svg)

**FIG-5.2 · The eval loop.** *What to notice:* "revert" is a normal, healthy outcome. Most changes don't help, and the eval is how you find out without shipping them.

1. **Build a golden set:** about ten real tasks the loop should handle, with known right answers (TRK-5.1).
2. **Change one thing:** the prompt, the checker, a cap, or the model underneath.
3. **Run the whole golden set** and record the five numbers.
4. **Compare with the last version.** Keep the change only if it helped without hurting anything else.
5. **Version it:** bump the number (v1.0 → v1.1) and write one changelog line (EX-5.2).

When the model underneath changes (a new Claude release, for example), rerun the golden set before you trust the loop again. Your loop's behavior is only as stable as the model's.

---

## 🧪 Examples

**EX-5.1 · A run log you can't use vs one you can** *(layer: Loop)*
- ❌ **Before:** a terminal that scrolled away, and a final line: `Done!`
- ✅ **After:**
  ```text
  iteration,started_at,action,check_result,stop_reason,tokens_in,tokens_out,diff_lines,note
  1,2026-09-20T02:00:04Z,agent,fail,,21044,1893,14,"FAIL: test_refund_rounding expected 10.01, got 10.00"
  2,2026-09-20T02:03:11Z,agent,fail,,22318,2210,9,"FAIL: test_tax_totals expected 3.15, got 3.14"
  3,2026-09-20T02:06:40Z,agent,pass,DONE,22901,1650,6,"12 passed, 0 failed"
  ```
- **What changed and why:** you can see that the loop fixed two different tests in three turns, what each turn cost in tokens, and that no turn made a huge change. "Done!" tells you none of that.

**EX-5.2 · A changelog entry, v1.0 → v1.1** *(layer: Loop)*
- ❌ **Before:** the checker was edited in place, with no record, and nobody knows why the loop behaves differently.
- ✅ **After:**
  ```text
  ## v1.1 · 2026-09-20
  Changed:    CHECKER now fails if any file under tests/ changes (was: pytest only)
  Why:        spot check found 2 of 10 passes had a skipped test (false-pass rate 20%)
  Golden set: success 8/10 → 8/10 · iterations per success 2.4 → 2.6 · false passes 2 → 0
  Decision:   keep
  ```
- **What changed and why:** the entry records one change, its reason, the before-and-after numbers, and the decision. Six months from now, you'll know why the checker looks the way it does.

---

## ✅ Best Practices

**BP-5.1 · Log every iteration in the same columns**
- **The practice:** one CSV row per iteration with fixed columns (the table above), including skipped and failed ones.
- **Why it works:** a consistent log turns debugging into reading, and lets you compute the five numbers with a spreadsheet instead of guessing.
- **How to check you did it:** paste a week of logs into the workbook's Run Log sheet, and the summary cells fill in without edits.

**BP-5.2 · Change one thing at a time, measured on a fixed task set**
- **The practice:** each version of the loop differs from the last in one way, and both versions run the same golden set (TRK-5.1).
- **Why it works:** if you change the prompt and the checker together and results improve, you can't tell which change helped, or whether one of them hurt.
- **How to check you did it:** every changelog entry names exactly one change and shows golden-set numbers for before and after.

**BP-5.3 · Spot-check passes to measure the false-pass rate**
- **The practice:** every week, check a random sample of passes by hand (for example 10), and count how many were really wrong.
- **Why it works:** it's the only way to measure F in real use, and F is the number that decides how far you can trust the loop (CALC-1).
- **How to check you did it:** your notes show a date, a sample size, and a count, such as "Sep 20: 10 checked, 0 wrong".

---

## 💡 Tips

**TIP-5.1 · Read the log backwards from the stop reason.** Start at the last row, then read up until the notes change.
```bash
tail -n 5 loop-log.csv     # last five iterations: stop reason first, then what led to it
```

**TIP-5.2 · Track cost per success, not cost per run.** Failed runs cost money too. Using the invented $0.12 per iteration from Level 4: 10 runs, 7 successes, 31 iterations → total $3.72.
```text
cost per run = $3.72 ÷ 10 = $0.37   ·   cost per success = $3.72 ÷ 7 = $0.53
```

**TIP-5.3 · Keep a failure-mode tally.** Each time a run fails, add one mark to the matching row of FIG-5.1.
```text
Sep: STUCK ||||  · gaming |  · stale state ||  → fix STUCK first
```

---

## 🎯 Tricks

**TRK-5.1 · The golden set: ten fixed tasks for every change**
- **When to use it:** before you change a loop that already works.
- **How:** save about ten real past tasks (for example, ten failing-test situations from your history) with their known right outcomes. Every candidate change runs all ten.
- **What it buys you:** an apples-to-apples comparison. Without it, a change that "seemed better" on today's task can quietly break tomorrow's.

**TRK-5.2 · Replay a failed run with one change**
- **When to use it:** after a failure you don't understand.
- **How:** reset the workspace to the commit where the failed run started (`git switch -c replay <commit>`), change one thing (the prompt, the checker message, the cap), and run it again.
- **What it buys you:** proof of what fixed it. A replay turns "I think it was the prompt" into "the prompt change alone took it from STUCK to DONE."

---

## 🛠 Hacks

**HCK-5.1 · Feed the last three attempts into the next prompt**
- **The move:** have the loop include its own recent history in the next run's context, so a fresh agent doesn't repeat a failed idea.
  ```text
  PREVIOUS ATTEMPTS (from progress.md, most recent last):
  1) rounded in refund()  → FAIL same test
  2) switched to Decimal   → FAIL same test
  Do not repeat these. Try something different, or report STUCK with your best guess.
  ```
- **The trade-off:** more context per run means more tokens (CALC-3), and a long list of failures can nudge the agent into odd workarounds. Keep it to the last three attempts, and let the STUCK rule decide when to stop trying.

---

## ⛔ Things to Avoid

**AVD-5.1 · Thrashing: fixing A breaks B**
- **Symptom:** the log alternates between two failures: iteration 3 fixes `test_a` and breaks `test_b`; iteration 4 does the reverse.
- **Cause:** each turn sees only the first failure, and the fixes conflict.
- **Fix:** run the whole check each turn and show every failure, keep turns small, and record in `progress.md` any constraint a fix must respect.
  - ❌ checker message: first failure only → ✅ `2 failing: test_a (expected X), test_b (expected Y). Fix both, or explain the conflict.`

**AVD-5.2 · Premature "done"**
- **Symptom:** the loop reports DONE, and your spot check finds the work unfinished.
- **Cause:** the maker's own "I'm done" was accepted, or a judge graded a summary instead of the work.
- **Fix:** only the checker's evidence ends a run (BP-2.2). With `/goal`, word the condition so the transcript must show proof, such as "`npm test` exits 0 and its output is shown."
  - ❌ `End when you're confident it's complete.` → ✅ `DONE only when check.sh exits 0; paste its last 5 lines as evidence.`

**AVD-5.3 · Silent failure: the loop that stopped logging**
- **Symptom:** everything looks quiet for a week; then you discover the loop hasn't run since a password change.
- **Cause:** "no news" was read as "good news". A loop that crashes before it logs leaves no trace.
- **Fix:** log a row at the start of every run, and alert when a day passes without one.
  - ❌ no rows = fine → ✅ `if no row dated today by 9 a.m., notify me`

---

## 🧮 Calculator

### CALC-4 · LOOP SCORECARD /100

**Purpose:** how ready is this loop to run without you, and which fixes are worth the most?

**Inputs:** rate each criterion from 0 (missing) to 5 (what the right-hand column describes).

| # | Criterion | What a 5 looks like |
|---|---|---|
| 1 | Goal & done condition | An end state a machine can check, with a success exit and a failure exit |
| 2 | Checker | Separate from the maker, "not yet" by default, trust estimated with CALC-1 |
| 3 | Stop rules & budget | Caps on iterations, spend, and time; a STUCK rule; the ceiling known from CALC-2 and CALC-3 |
| 4 | Safety | An isolated workspace, least permissions, no destructive defaults, secrets kept out, prompt injection considered, a kill switch |
| 5 | State & memory | Kept in files outside the model; a fresh session can resume from them |
| 6 | Observability | A run log for every iteration, and the five numbers from this level |
| 7 | Human touchpoints | An escalation package, approval where the stakes need it, the autonomy rung stated |
| 8 | Reusability | A one-page Loop Spec, a version number, placeholders, easy to adapt |

**Formula:** **Score = 3 × (r1 + r2 + r3 + r4) + 2 × (r5 + r6 + r7 + r8)**. Criteria 1–4 are worth 15 points each and criteria 5–8 are worth 10 each, so a perfect loop scores 3 × 20 + 2 × 20 = 100. The first four weigh more because a loop that fails them can do damage; the last four make it easier to run and improve.

**Assumptions (each adjustable):** the weights (3 and 2) are a judgment call, not a law; ratings are honest estimates. Re-score after every version change.

**Worked example: CS-1's test-fixing loop, v1 against v2** (the full story is in the [Case Study Lab](07-case-study-lab.md)):

| # | Criterion | v1 | v2 | Why v2 is higher |
|---|---|---|---|---|
| 1 | Goal & done | 2 | 5 | End state plus "no file under `tests/` changes", with success and failure exits |
| 2 | Checker | 1 | 5 | Tests plus a fingerprint of `tests/`, and a separate reviewer; trust measured at 96% |
| 3 | Stop rules & budget | 0 | 5 | Cap of 5 from CALC-2, 20 minutes, STUCK after 3, ceiling from CALC-3 |
| 4 | Safety | 1 | 4 | A branch, an allowlist, `PROTECT`; not yet in a container |
| 5 | State & memory | 1 | 4 | `progress.md` plus commits; resume tested once |
| 6 | Observability | 1 | 4 | CSV run log; weekly numbers; no alerts yet |
| 7 | Human touchpoints | 1 | 4 | Rung 3: you merge; escalation note; no spot-check schedule yet |
| 8 | Reusability | 1 | 4 | Loop Spec v2.0 with a changelog |

- **v1:** 3 × (2 + 1 + 0 + 1) + 2 × (1 + 1 + 1 + 1) = 3 × 4 + 2 × 4 = 12 + 8 = **20 / 100, draft**
- **v2:** 3 × (5 + 5 + 5 + 4) + 2 × (4 + 4 + 4 + 4) = 3 × 19 + 2 × 16 = 57 + 32 = **89 / 100, strong**

**Worked example: the kit's own `loop.sh`, at its default settings.** An honest score for the plumbing alone, before you plug in a real goal and checker:
- Ratings: goal & done 2 (the default check is a mock), checker 2 (separate by design, but nothing measured), stop rules & budget 4 (four stop families built in, plus DANGER when you set `PROTECT`, but spend isn't tracked), safety 4 (dry run by default, stop file, no deletes or pushes, not sandboxed), state 3 (the script keeps a log, but `progress.md` is up to your prompt), observability 3 (token columns stay blank unless you fill them), human touchpoints 3 (a stop file, but no automatic escalation note), reusability 4.
- **Score:** 3 × (2 + 2 + 4 + 4) + 2 × (3 + 3 + 3 + 4) = 3 × 12 + 2 × 13 = 36 + 26 = **62 / 100, working**. That's the honest lesson: a script is plumbing. The loop becomes strong when you add a real DONE condition, a measured checker, and an escalation note.

![FIG-5.3: Paired horizontal bars for the eight criteria, v1 in orange with diagonal hatching and v2 in blue, each rated 0 to 5. v1 is low everywhere and zero on stop rules. v2 scores 5 on goal, checker, and stop rules, and 4 on the rest. Totals: v1 20 out of 100, v2 89 out of 100.](assets/fig-5-3-scorecard-v1-v2.svg)

**FIG-5.3 · CS-1 scorecard, v1 vs v2** (CALC-4). *What to notice:* the three biggest gains (checker, stop rules, goal) are all in the 15-point group. That's where most first loops are weakest.

**Reading the result**

| Score | Band | What to do |
|---|---|---|
| **0–59** | Draft | Don't run it unattended |
| **60–74** | Working | Run it while you watch |
| **75–89** | Strong | Unattended, with caps and spot checks |
| **90–100** | Hero-grade | Unattended; keep measuring |

Every rating below 4 names the fix that would raise it. The biggest gains are usually in criteria 1–4, where each point is worth 3.

**Blank worksheet**
```text
CALC-4 · LOOP SCORECARD                          rating 0–5    fix if below 4
1 Goal & done condition                          r1 = __       ______________
2 Checker                                        r2 = __       ______________
3 Stop rules & budget                            r3 = __       ______________
4 Safety                                         r4 = __       ______________
5 State & memory                                 r5 = __       ______________
6 Observability                                  r6 = __       ______________
7 Human touchpoints                              r7 = __       ______________
8 Reusability                                    r8 = __       ______________
Score = 3 × (r1+r2+r3+r4) + 2 × (r5+r6+r7+r8) = 3 × __ + 2 × __ = ____ / 100 → band: ______
```

**Spreadsheet formulas** (Google Sheets and Excel), with the eight ratings in B2:B9:
```text
Score: =3*SUM(B2:B5)+2*SUM(B6:B9)
Band:  =IF(B10>=90,"hero-grade",IF(B10>=75,"strong",IF(B10>=60,"working","draft")))     (B10 = score)
```

**Workbook sheet:** `CALC-4 Scorecard` in [`workbook/loop-engineering-workbook.xlsx`](workbook/loop-engineering-workbook.xlsx), with CS-1's v1 and v2 pre-filled.

---

## 🗣 Council Debate

*Is a loop that succeeds 90% of the time good enough?*

> **ABACUS:** 90% success, and a CALC-1 trust of 95% on the passes, is better than most people manage by hand.
> **GOVERNOR:** What happens in the other 10%? If those runs stop cleanly with an escalation note, fine. If they fail silently, 90% is a trap.
> **ABACUS:** Those are two different numbers. Success rate is how often it finishes; trust is how often a finish is real.
> **SMITH:** And a third: what the 10% costs. Ten percent of newsletter drafts is nothing. Ten percent of database changes is not.
> **RAZOR:** Then the answer is never just a percentage. It's a percentage plus how it fails.

**ORBIT's ruling:** 90% is good enough when the failures exit cleanly (CAP, STUCK, or DANGER, with an escalation note), the passes are trustworthy (CALC-1 ≥ 95%), and a failure is cheap. When any of those three is missing, fix that before chasing a higher success rate.

---

## 🏋 Practice

(Layer: **Loop**.)

1. Run the kit's dry-run demos from Level 4 a few times with different settings, and collect the `loop-log.csv` files.
2. Paste the rows into the workbook's **Run Log** sheet, and read the success rate, iterations per success, and cost per success it computes. (Token columns will be blank in a dry run, so cost stays blank too. That's expected.)
3. Score the loop you designed in Levels 1–4 with CALC-4. For every rating below 4, write the fix.
4. Pick the single fix worth the most points (a criterion from 1–4 if any are low), apply it, and write a v0.2 changelog entry in the EX-5.2 format.
5. Name three tasks from your own work that would make a good golden set for this loop.

**Done when:** you have a scored spec, one fix applied with a changelog line, and a golden set of three or more tasks.

---

## ✔ Level-Up Check

1. **Name the five numbers that matter, and which one is CALC-1's F measured for real.**
   *Answer:* success rate, iterations per success, cost per success, human interventions per run, and the false-pass rate. The false-pass rate is F.
2. **The log alternates between two failing tests. What's happening, and what's one fix?**
   *Answer:* thrashing (AVD-5.1). Show every failure each turn, keep turns small, and record constraints in `progress.md`.
3. **Why change only one thing per version?**
   *Answer:* so you can tell which change helped or hurt (BP-5.2).
4. **Ratings of 2, 1, 0, 1, 1, 1, 1, 1. What's the score and band?**
   *Answer:* 3 × 4 + 2 × 4 = 20 / 100, draft. Don't run it unattended.
5. **A loop has run quietly for a week with no errors. Why might that be bad news?**
   *Answer:* it might not have run at all: a silent failure (AVD-5.3). Check that each day has log rows.

⬅ [Level 4](04-level-4-author.md) · 🏠 [README](README.md) · [Level 6](06-level-6-hero.md) ➡
