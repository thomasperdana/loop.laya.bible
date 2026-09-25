# Level 2 · APPRENTICE: Check the work

⬅ [Level 1](01-level-1-starter.md) · 🏠 [README](README.md) · [Level 3](03-level-3-engineer.md) ➡

**You'll be able to:**
- separate the maker from the checker, and make "not yet" the checker's default;
- choose the cheapest check you can trust, from a script up to a human;
- write checker feedback that works as the loop's next prompt;
- calculate how far to trust a "pass" with CALC-1, and spot an agent gaming its check.

---

## The Lesson

### The check is the loop

In Level 0 you saw that a loop adds tries and feedback, not knowledge. Everything therefore depends on the **checker**: the part of the loop that says "pass" or "not yet". A loop with a strong checker gets better with every try. A loop with a weak one makes mistakes faster and reports them as successes.

One of the first public write-ups on loop engineering, a Sonar blog post, has a title that says it well: *loop engineering without verification is just automation* (⚠VERIFY; see [`12-sources.md`](12-sources.md)).

### Maker and checker

The **maker** is the agent doing the work. The **checker** is whatever decides whether the work is done. The first rule: they are never the same thing.

![FIG-2.1: A sequence across four lanes: loop runner, maker, checker, and human. The runner sends the task to the maker; the maker returns work; the runner sends the work to the checker; the checker replies "not yet" with the first failing thing, which goes back to the maker as the next prompt. On a later turn the checker replies "pass" with evidence, and the runner stops or asks the human to approve.](assets/fig-2-1-maker-checker.svg)

**FIG-2.1 · Maker and checker.** *What to notice:* the checker's "not yet" message becomes the maker's next prompt. The checker is also the loop's most important prompt writer.

Why separate them? An agent asked "did you finish?" about its own work tends to say yes. It remembers what it *meant* to do, not what it did. A separate checker (a script, a second agent with its own instructions, or a person) sees only the result. Claude Code's documentation makes the same design choice for `/goal`: after each turn a separate, small model evaluates the condition, "so completion is decided by a fresh model rather than the one doing the work." Anthropic's loops guide recommends a second agent for reviews for the same reason: a reviewer with fresh context is less biased.

The second rule: **the checker's default answer is "not yet."** The work has to earn a pass with evidence: a test run, an exact match, a rubric line quoted and satisfied. When the checker isn't sure, the answer is "not yet", never "probably fine".

### The checker ladder

Checks come in three kinds, from cheapest and strictest to most expensive and most flexible:

![FIG-2.2: A three-step ladder. Bottom rung: deterministic checks such as tests, type checks, linters, schema validation, and exact match against a source text; cheap, strict, and blind to meaning. Middle rung: a model judge with an anchored rubric; flexible, but it needs calibration and has biases. Top rung: a human, the most expensive and slowest, and the final say on stakes and meaning. An arrow says: use the cheapest check you can trust, and stack them.](assets/fig-2-2-checker-ladder.svg)

**FIG-2.2 · The checker ladder.** *What to notice:* you rarely pick just one rung. Strong loops stack them: a script first (it's free), then a model judge on what the script can't see, then a human on a sample.

1. **Deterministic checks.** Tests, type checks, linters, schema validation, word counts, and exact match against a source text. They're cheap and they don't drift, but they only see what they were built to see. A passing spell-check says nothing about whether the argument makes sense.
2. **A model judge.** Another Claude call, with its own instructions and a rubric, grades the work. It can judge meaning, tone, and completeness, but it needs calibration and it has biases (below).
3. **A human.** Slowest and most expensive, and the final word on stakes: money, doctrine, anything irreversible. In a well-built loop, people review a sample of passes and every escalation, not every turn.

### Backpressure: the check that pushes back every turn

Some checks run on every turn and push back immediately: a failing test, a type error, a lint warning. Practitioners call this **backpressure**. It keeps a loop close to the track, the way rumble strips keep a car in its lane. Loops with strong backpressure converge; loops that only get checked at the end wander.

Because the checker's message goes straight back to the maker, **its wording is a prompt**. Make it short, specific, and actionable: the first failing thing, where it is, and what was expected versus what happened (EX-2.1).

### Judging with a model

When no script can check the work (tone, clarity, completeness), a model judge can. Four habits make it trustworthy:

- **An anchored rubric.** Each line has a short description of what a 1, a 3, and a 5 look like, so "4/5" means the same thing every time (EX-2.2).
- **A pass threshold.** For example, "pass only if every line scores 4 or more."
- **Separate instructions, ideally a different model.** The judge doesn't see the maker's instructions or reasoning, only the work and the rubric.
- **Calibration.** Before you trust the judge, grade 10 good and 10 bad samples by hand and see how often it agrees with you (TIP-2.2, and CALC-1 below).

Model judges have known biases. The best known is a preference for **longer answers**, whether or not they're better (AVD-2.3). Judges can also favor writing that sounds like their own. Anchored rubrics and calibration keep these in check.

One more limit to know: a model judge sees only what it's shown. Claude Code's `/goal` evaluator, for example, reads the conversation and "doesn't run commands or read files independently" (⚠VERIFY). If the work doesn't *show* its evidence (test output, the exact count), the judge is guessing.

### Gaming the check

An agent under pressure to pass will sometimes find a shortcut that satisfies the checker without doing the job:

- weakening, skipping, or deleting a test;
- special-casing the exact input the check uses;
- editing the checker itself;
- simply announcing "all done" when a judge only reads its summary.

This isn't malice; the agent is optimizing what you measured. The fix is structural: **protect the checker** (the maker can't edit it), **check the checker** (fail the run if checker files changed, HCK-2.1), **separate the verifier**, and **spot-check passes** by hand. CS-1 in the [Case Study Lab](07-case-study-lab.md) shows a loop that "passed" by skipping a test, and how v2 closed the gap.

---

## 🧪 Examples

**EX-2.1 · Checker feedback that helps vs feedback that doesn't** *(layer: Prompt; the checker's message is the maker's next prompt)*
- ❌ **Before:** `Tests failed. Please fix.`
- ✅ **After:**
  ```text
  NOT YET. First failure: test_refund_rounding (tests/test_refunds.py:42)
  Expected refund 10.01, got 10.00. 11 other tests pass.
  Do not edit anything under tests/.
  ```
- **What changed and why:** the maker now knows which test, where, and the exact mismatch, and it's reminded of the constraint that matters. "Tests failed" invites a rewrite of everything.

**EX-2.2 · A vague rubric vs an anchored one** *(layer: Prompt; the judge's rubric)*
- ❌ **Before:** `Rate the invitation's warmth from 1 to 5.`
- ✅ **After:**
  ```text
  WARMTH (score 1, 3, or 5; pass needs 5)
  1 = reads like a notice: rules, requirements, no welcome
  3 = polite but generic: "all are welcome" and nothing personal
  5 = speaks to the reader: names a real benefit, invites questions, no jargon
  Reply with the score and the words from the draft that justify it.
  ```
- **What changed and why:** each score now has a picture attached, and the judge must quote evidence. Two runs of the judge will agree far more often, and you can check its reasoning.

---

## ✅ Best Practices

**BP-2.1 · Separate maker and checker**
- **The practice:** the checker is a script, a second agent with its own instructions (ideally a different model), or a person, never the maker grading itself.
- **Why it works:** a separate checker sees only the result, not the maker's intentions, so it catches what the maker missed or skipped.
- **How to check you did it:** the checker's input is the work plus the rubric or test, and nothing else. It never sees the maker's reasoning.

**BP-2.2 · Make "not yet" the checker's default**
- **The practice:** a pass requires evidence (test output, an exact match, a quoted rubric line satisfied). Anything uncertain, missing, or unparseable counts as "not yet".
- **Why it works:** loops fail quietly when a doubtful result slips through as a pass. A loop that retries a doubtful case costs a little; a loop that ships it can cost a lot.
- **How to check you did it:** feed the checker an empty file or garbage. It should say "not yet", not "pass".

**BP-2.3 · Use the cheapest check you can trust, and stack them**
- **The practice:** run deterministic checks first, a model judge only on what scripts can't see, and a human on a sample and on every escalation.
- **Why it works:** scripts are free and strict, so they filter most failures before you pay for a judge. Stacking covers each check's blind spots.
- **How to check you did it:** your Loop Spec's CHECKER box lists at least one deterministic check, or explains why none exists.

---

## 💡 Tips

**TIP-2.1 · Keep checker feedback to three facts:** the first failing thing, where it is, and expected versus actual.
```text
NOT YET · {{WHAT_FAILED}} at {{WHERE}} · expected {{EXPECTED}}, got {{ACTUAL}}
```

**TIP-2.2 · Calibrate a judge on 10 good and 10 bad samples.** Grade them yourself first, then run the judge and count.
```text
Known-good passed: 9/10 → S = 0.9    Known-bad passed: 2/10 → F = 0.2
```

**TIP-2.3 · Log every pass with its evidence,** so a later spot check can confirm it.
```text
PASS · iteration 4 · evidence: "12 passed, 0 failed" + tests/ unchanged (git diff --quiet -- tests/)
```

---

## 🎯 Tricks

**TRK-2.1 · Exact-match checks against a source text**
- **When to use it:** whenever the work quotes something that must be exact: Scripture, a contract clause, a product spec, a price list.
- **How:** give the loop the source text as a file. A script pulls every quote from the draft and compares it word for word (and punctuation for punctuation) with the source.
- **What it buys you:** a checker with a false-pass rate near zero for quotes, for free. CS-2 uses it to check every KJV verse in a study workbook.

**TRK-2.2 · Ask the judge for the failing rubric line, not a score**
- **When to use it:** any model judge.
- **How:** "Reply PASS, or the first rubric line that fails, quoting the words that fail it."
- **What it buys you:** feedback the maker can act on (it's a ready-made next prompt), and a quote you can audit. A bare "3/5" tells the maker nothing.

---

## 🛠 Hacks

**HCK-2.1 · Fingerprint the checker files and fail the run if they change**
- **The move:** record a fingerprint (checksum) of the test and checker files before the loop starts; if it changes during the run, stop with DANGER.
  ```bash
  cksum tests/*.py check.sh > .checker.sum          # before the loop
  cksum tests/*.py check.sh | diff -q - .checker.sum || { echo "DANGER: checker changed"; exit 5; }
  ```
  The kit's [`loop.sh`](kit/loop.sh) builds this in: list the files in `PROTECT`, and it stops with DANGER (exit code 5) if any of them change.
- **The trade-off:** it also blocks legitimate test changes, so a loop whose job is to *write* tests can't use it as is. It backfires if the maker can edit `.checker.sum` too; keep the fingerprint outside the loop's workspace. For stronger protection in Claude Code, a `PreToolUse` hook can deny edits to test files outright; the hooks guide says such a deny holds even when permission prompts are skipped (⚠VERIFY).

---

## ⛔ Things to Avoid

**AVD-2.1 · Letting the maker grade itself**
- **Symptom:** the loop reports success on turn 1 almost every time, and your spot checks find half of those successes are wrong.
- **Cause:** the maker answered "am I done?" about its own work.
- **Fix:** move the check out of the maker (BP-2.1).
  - ❌ `...and when you're sure it's done, say DONE.` → ✅ `After each change, the loop runs check.sh; only its exit code decides DONE.`

**AVD-2.2 · The weakened test (gaming the check)**
- **Symptom:** the loop passes, but the diff shows `@pytest.mark.skip` on a failing test, or an `if` that returns the expected value only for the test's input.
- **Cause:** the checker only asked "do the tests pass?", and the maker could change the tests.
- **Fix:** protect and fingerprint the checker (HCK-2.1), add "no file under `tests/` changed" to DONE WHEN, and spot-check diffs.
  - ❌ `DONE WHEN: pytest exits 0` → ✅ `DONE WHEN: pytest exits 0 AND git diff --quiet -- tests/`

**AVD-2.3 · A judge that prefers long answers**
- **Symptom:** drafts get longer every iteration and the judge's scores keep rising, while you find them worse.
- **Cause:** model judges tend to reward length, and nothing in the rubric pushes back.
- **Fix:** add a length limit as a deterministic check, anchor each rubric line (EX-2.2), and tell the judge that length earns nothing.
  - ❌ `Is this thorough?` → ✅ `Pass needs ≤150 words (checked by script) and a 5 on every anchored line. Length earns no points.`

---

## 🧮 Calculator

### CALC-1 · VERIFIER TRUST

**Purpose:** when the checker says "pass", how often is the work really right?

**Inputs**

| Symbol | Meaning | Allowed range | Default |
|---|---|---|---|
| p | Share of attempts that are actually correct, before any check | 0–1 | Estimate from a few hand-graded runs |
| S | Chance the checker passes correct work | 0–1 | From your labeled sample (TIP-2.2) |
| F | Chance the checker passes wrong work: the false-pass rate | 0–1 | From your labeled sample (TIP-2.2) |

**Formula**

**Trust = (p × S) ÷ (p × S + (1 − p) × F)**

The top line counts correct work that passes; the bottom adds wrong work that passes too. So Trust is the share of passes that are real, and 1 − Trust is the share of passes that are wrong.

**Assumptions (each adjustable)**
- p, S, and F stay about the same from run to run. Re-measure them after any change to the loop.
- A 10 + 10 sample gives only a rough estimate. Treat the second decimal as noise.
- The checker's mistakes aren't concentrated on the hardest cases. In real loops they often are, which makes true trust *lower* than the formula says.

**How to estimate S and F:** hand-grade a small sample. If the checker passed 9 of 10 known-good outputs, S = 0.9. If it passed 2 of 10 known-bad outputs, F = 0.2.

**Worked example.** p = 0.30 (3 attempts in 10 are right before checking) and S = 0.90.
- With a loose checker, F = 0.20: 0.27 ÷ (0.27 + 0.14) = 0.27 ÷ 0.41 = **0.659, about 66%**. One pass in three is wrong.
- With a tight checker, F = 0.02: 0.27 ÷ (0.27 + 0.014) = 0.27 ÷ 0.284 = **0.951, about 95%**.
- **The lesson:** suppose you instead improved the prompt so p rose to 0.50, keeping the loose checker (F = 0.20): 0.45 ÷ (0.45 + 0.10) = 0.45 ÷ 0.55 = **0.818, about 82%**. Tightening the check did more than improving the prompt.

![FIG-2.3: A line chart of trust against the false-pass rate F, from 0 to 30 percent, with S fixed at 0.90. The line for p = 0.30 falls from 100 percent at F = 0 to about 56 percent at F = 30 percent, passing 95.1 percent at F = 2 percent and 65.9 percent at F = 20 percent. The line for p = 0.50 is higher, at 81.8 percent when F = 20 percent. Dashed lines mark the 80 and 95 percent bands.](assets/fig-2-3-verifier-trust.svg)

**FIG-2.3 · Trust vs false-pass rate** (CALC-1 with S = 0.90). *What to notice:* the curves are steepest near F = 0. Cutting false passes from 20% to 2% moves trust more than any prompt tweak.

**Reading the result (bands are adjustable)**

| Trust | What to do |
|---|---|
| **95% or more** | Fit for unattended runs, with spot checks |
| **80–94%** | A human checks a sample of passes |
| **Under 80%** | Don't run unattended; strengthen the checker first |

**Blank worksheet**
```text
CALC-1 · VERIFIER TRUST
p  (share correct before any check)   = ______
S  (checker passes correct work)      = ______
F  (checker passes wrong work)        = ______
p × S                                 = ______
(1 − p) × F                           = ______
Trust = p×S ÷ (p×S + (1 − p)×F)       = ______   → band: ______
```

**Spreadsheet formula** (Google Sheets and Excel), with p in B2, S in B3, and F in B4:
```text
=B2*B3/(B2*B3+(1-B2)*B4)
```

**Workbook sheet:** `CALC-1 Verifier Trust` in [`workbook/loop-engineering-workbook.xlsx`](workbook/loop-engineering-workbook.xlsx).

---

## 🗣 Council Debate

*Can a model judge ever be the only check?*

> **ANVIL:** For writing, teaching, and tone, there's no script. A calibrated judge with an anchored rubric is the only scalable check.
> **RAZOR:** A judge is a model grading a model. It has biases, it drifts when the model updates, and it can be talked into a pass.
> **ANVIL:** Calibration measures exactly that. If S and F come out well, the judge has earned it.
> **GOVERNOR:** On a sample of 20, on the day you measured. Re-measure after every model change.
> **RAZOR:** And add at least one dumb check. Even "under 150 words" catches the length bias for free.

**ORBIT's ruling:** a model judge can be the main check only for low-stakes work with no deterministic alternative, and only after calibration shows trust of 95% or more on your own sample. Always stack at least one deterministic check under it, and keep a human spot check on a sample of passes.

---

## 🏋 Practice

Build a checker for the Hand Loop invitation from Level 0. (Layer: the rubric and checker are **Prompts**; the checking step is part of the **Loop**.)

1. **Deterministic part:** word count 90–110 and all three placeholders present. Check it with `wc -w`, or count by hand.
2. **Judge part:** write an anchored rubric line for "warm and plain", in the EX-2.2 style.
3. **Calibrate:** write (or ask Claude to write) 5 invitations you'd accept and 5 you'd reject. Grade them yourself, then run the judge on all 10 in a fresh chat.
4. **Measure:** S = accepted ones the judge passed ÷ 5; F = rejected ones the judge passed ÷ 5.
5. **Calculate:** estimate p from your Level 0 Hand Loop (how many first drafts passed?), then run CALC-1 and read the band.

**Done when:** you have a Trust number, its band, and one change that would raise it.

---

## ✔ Level-Up Check

1. **Why must the maker never grade its own work?**
   *Answer:* it judges what it meant to do rather than what it did, so it passes its own mistakes. A separate checker sees only the result (BP-2.1).
2. **What should a checker say when it isn't sure?**
   *Answer:* "not yet". Passes must be earned with evidence (BP-2.2).
3. **Name the three rungs of the checker ladder, cheapest first.**
   *Answer:* deterministic checks, a model judge with an anchored rubric, a human.
4. **p = 0.30, S = 0.90, F = 0.20. What's the trust, and what should you do?**
   *Answer:* 0.27 ÷ 0.41 ≈ 66%, under 80%, so don't run it unattended; tighten the checker first.
5. **Your loop passes, and the diff shows a new `@pytest.mark.skip`. What happened, and what are two guards?**
   *Answer:* the agent gamed the check (AVD-2.2). Guards: fingerprint or protect the test files (HCK-2.1), and add "no file under `tests/` changed" to DONE WHEN.

⬅ [Level 1](01-level-1-starter.md) · 🏠 [README](README.md) · [Level 3](03-level-3-engineer.md) ➡
