# Level 3 · ENGINEER: Stop rules, state, and isolation

⬅ [Level 2](02-level-2-apprentice.md) · 🏠 [README](README.md) · [Level 4](04-level-4-author.md) ➡

**You'll be able to:**
- give every loop five ways to stop: DONE, CAP, STUCK, DANGER, and HUMAN;
- write an escalation note a person can act on in two minutes;
- keep a loop's memory in files, so each run can start fresh without forgetting;
- set an iteration cap from numbers with CALC-2, and keep each loop in its own workspace.

---

## The Lesson

### A loop is defined by how it stops

A loop that knows only how to succeed will keep trying when success is impossible, at your expense, while you sleep. Every loop in this guide has five stop families: one success exit and four failure exits.

![FIG-3.1: A state diagram. In the middle, a running state with a "not yet, next turn" arrow looping back to itself. Five exits lead out: DONE when the checker passes, exit code 0; CAP when iterations, spend, or time run out, exit code 2; STUCK when the same failure repeats, exit code 3; HUMAN when the stop file appears or a checkpoint is due, exit code 4; and DANGER when a risky permission, a destructive action, or a change to a protected file is detected, exit code 5.](assets/fig-3-1-stop-rules.svg)

**FIG-3.1 · The five stop families.** *What to notice:* four of the five exits are failures, and that's normal. A loop earns trust by stopping cleanly when it can't win, not by always winning. The exit codes match the kit's [`loop.sh`](kit/loop.sh).

| Family | Stops when | Example rule |
|---|---|---|
| **DONE** | The checker passes, with evidence | `check.sh` exits 0 |
| **CAP** | A limit runs out: iterations, tokens or money, or time | At most 5 iterations or 20 minutes |
| **STUCK** | No progress: the same failure N times, an empty diff, repeated output | The same failure 3 times in a row |
| **DANGER** | Something risky: a permission change, a destructive or irreversible action, a protected file edited | Any change under `tests/` |
| **HUMAN** | A person says stop, or a checkpoint is due | The file `.loop-stop` exists |

The tools you'll use have some of these built in, which is a good sign that the designers thought the same way (⚠VERIFY; these details change):
- Claude Code's `/goal` stops the loop if Claude keeps answering the evaluator without making progress (no tool use for several turns in a row), and its documentation suggests adding a turn or time clause to the condition, such as "or stop after 20 turns".
- A Claude Code Stop hook that keeps sending Claude back to work is overridden after it blocks **eight** times in a row without progress.
- Recurring `/loop` tasks expire after **seven days**, which, in the documentation's words, "bounds how long a forgotten loop can run."
- The Ralph loop plugin's `--max-iterations` defaults to *unlimited*, and its README warns you to always set it.

That last point is the lesson of this level: **never trust a default to cap your loop.** Write your own.

### Escalation: what the loop hands you

When a loop stops without success, it should leave a note a person can act on in two minutes. That note is the **escalation package**:

1. **What it was trying to do** (the goal, one line).
2. **Why it stopped** (the stop family and the rule that fired).
3. **What it tried** (one line per attempt).
4. **The evidence** (the last checker message, the last diff).
5. **Its best guess** at what's wrong, marked as a guess.

EX-3.2 shows a useless note and a useful one.

### State: amnesia with good notes

An AI agent's working memory is its **context window**: everything in the current conversation. Long loops break that memory in two ways. The window fills up and gets summarized ("compacted"), which blurs early details, and a new session starts with nothing at all.

The fix is to keep the loop's memory **in files**, not in the conversation:

![FIG-3.3: Three runs side by side. Each run starts with a fresh context, reads the same PROMPT.md plus the latest progress.md and git history, finishes one item, then writes progress.md and a commit. Underneath, a band of files on disk persists across runs: PROMPT.md stays the same, progress.md is updated, the git history grows, and the run log grows. A side note says one long session instead fills up, gets compacted, and blurs early details.](assets/fig-3-3-fresh-context-state.svg)

**FIG-3.3 · Fresh context, memory in files.** *What to notice:* the prompt never changes between runs, but the files do. Each run starts from zero and still knows exactly where things stand.

- **The prompt file** (`PROMPT.md`) stays the same every run: the goal, the rules, where to look first.
- **The progress file** (`progress.md`) says what's done, what's next, what's blocked, and what was decided.
- **Git history** records every change, with a message, and lets you undo any of them.
- **The run log** records every iteration in the same columns (Level 5).

This is the heart of the "Ralph" pattern you'll build in Level 4: the same prompt, fed to a fresh agent each time, with the files carrying the memory. A new session can pick up exactly where the last one stopped, which is also how the build of this guide resumes if it's interrupted.

### Isolation: one loop, one workspace

Two loops editing the same folder will overwrite each other's work, and a loop editing your main branch can break what everyone else uses. Give each loop its own workspace:

- **A branch**, so its changes sit apart until you approve them (autonomy rung 3).
- **A git worktree**, which is a second working folder attached to the same repository. Each loop gets its own folder on its own branch, so parallel loops never touch each other's files (TRK-3.2).
- **A container or a disposable virtual machine**, for any loop that runs with broad permissions (Level 4).

---

## 🧪 Examples

**EX-3.1 · A loop with one exit vs a loop with five** *(layer: Loop)*
- ❌ **Before:**
  ```text
  LIMITS: keep going until the tests pass
  ```
- ✅ **After:**
  ```text
  LIMITS: DONE    check.sh exits 0
          CAP     5 iterations · 20 minutes · (ceiling from CALC-3)
          STUCK   same failure message 3 times in a row
          DANGER  any change under tests/ or to check.sh
          HUMAN   .loop-stop exists
  ```
- **What changed and why:** the "before" loop has no way to give up. If the tests can't pass (a wrong requirement, a missing library), it runs until someone notices the bill.

**EX-3.2 · A useless escalation note vs a useful one** *(layer: Prompt; this is what the loop writes for you)*
- ❌ **Before:** `Loop stopped. Something went wrong.`
- ✅ **After:**
  ```text
  STOPPED: STUCK (same failure 3×) · goal: all tests in tests/ pass
  Tried: 1) rounding in refund() 2) Decimal instead of float 3) rounding at display time
  Last checker message: test_refund_rounding expected 10.01, got 10.00
  Last diff: billing/refunds.py (+6 −2) on branch loop/fix-tests
  Best guess (unverified): the test expects banker's rounding; the spec says round-half-up. Needs a human decision.
  ```
- **What changed and why:** you can see in one glance what happened and what decision is yours. The loop even spotted that the blocker is a requirements question, not a code bug.

---

## ✅ Best Practices

**BP-3.1 · Give every loop all five stop families**
- **The practice:** write a rule for DONE, CAP, STUCK, DANGER, and HUMAN in the LIMITS box before the first run.
- **Why it works:** each family catches a different way loops fail: impossible goals (CAP), repeated failure (STUCK), risky actions (DANGER), and plain human judgment (HUMAN).
- **How to check you did it:** for each family, you can name the exact condition and what the loop does when it fires.

**BP-3.2 · Keep state in files, not in the model's memory**
- **The practice:** at the end of every turn, the loop writes what it did and what's next to `progress.md`, commits its change, and appends a run-log row.
- **Why it works:** files survive a full context window, a crash, and a new session. Memory in the conversation doesn't.
- **How to check you did it:** kill the session mid-run, start a fresh one with the same prompt, and see whether it picks up the right next item.

**BP-3.3 · One loop, one workspace**
- **The practice:** each loop gets its own branch (and, for parallel loops, its own worktree). Nothing lands on the main branch without approval.
- **Why it works:** isolation turns every mistake into something you can throw away, and keeps parallel loops from editing the same files.
- **How to check you did it:** `git status` on your main branch is clean while the loop runs.

---

## 💡 Tips

**TIP-3.1 · Use a stop file as the universal off switch.** The loop checks for it at the start of every iteration.
```bash
[ -f .loop-stop ] && { echo "HUMAN: stop file found"; exit 4; }
```
To stop the loop from another window: `touch .loop-stop`.

**TIP-3.2 · Detect STUCK by comparing failure output.** Fingerprint the checker's failure message; if the same fingerprint appears three times in a row, stop.
```bash
fp=$(printf '%s' "$check_output" | cksum)   # same message → same fingerprint
```

**TIP-3.3 · End every run by writing the progress file,** even when the run fails.
```text
## {{DATE}} · iteration {{N}} · result: NOT YET
Did: rounded refund() to cents · Next: check display rounding · Blocked: none
```

---

## 🎯 Tricks

**TRK-3.1 · Amnesia with notes: a fresh context every run**
- **When to use it:** any loop longer than one sitting, or one that will run many iterations.
- **How:** start each iteration as a brand-new agent session. Its first instruction is "read `progress.md` and the last few commits, then do the next unchecked item."
- **What it buys you:** no context rot (the slow loss of quality as a long conversation fills up), no stale assumptions from ten turns ago, and a loop that can resume after any crash.

**TRK-3.2 · A worktree per loop for parallel runs**
- **When to use it:** when two or more loops work on the same repository at the same time.
- **How:** give each loop its own worktree on its own branch.
  ```bash
  git worktree add ../myapp-loop-links -b loop/docs-links
  ```
- **What it buys you:** loops that can't overwrite each other, and a clean place to review each loop's changes before you merge them.

---

## 🛠 Hacks

**HCK-3.1 · Use git commits as the loop's memory and undo button**
- **The move:** have the loop commit after every successful turn, with a message in a fixed format. Its next run reads `git log`, and you can undo any single turn.
  ```bash
  git commit -am "loop(docs-links) iter 3: fix 2 links in lessons/week2.md [check: 1 broken left]"
  git log --oneline -5      # the next run's first read
  ```
- **The trade-off:** you get a noisy history of many tiny commits. Squash them when you merge the branch. It backfires if the loop commits failing states without saying so, so put the checker result in every message.

---

## ⛔ Things to Avoid

**AVD-3.1 · The loop with no failure exit**
- **Symptom:** you come back in the morning to hundreds of iterations and a large bill, with the same error in every run.
- **Cause:** only DONE was defined, and the goal was impossible that night.
- **Fix:** add CAP and STUCK before anything else (BP-3.1).
  - ❌ `/ralph-loop "fix the build"` → ✅ `/ralph-loop "fix the build" --max-iterations 5`, plus a STUCK rule in the prompt (⚠VERIFY the flags)

**AVD-3.2 · State that lives only in the conversation**
- **Symptom:** after the session restarts, the loop redoes finished work, or undoes a decision you made yesterday.
- **Cause:** the only record of progress was in a context window that's gone.
- **Fix:** progress file, commits, and run log, written every turn (BP-3.2).
  - ❌ "Remember that we decided to keep round-half-up." → ✅ `progress.md → Decisions: rounding = round-half-up (you, Sep 12)`

**AVD-3.3 · Two loops in one folder**
- **Symptom:** files flip back and forth between two versions; each loop's checker fails because of the other loop's edits.
- **Cause:** two loops share one working folder.
- **Fix:** one worktree and one branch per loop (TRK-3.2).
  - ❌ Both loops run in `~/myapp` → ✅ `~/myapp-loop-links` and `~/myapp-loop-tests`, each on its own branch

---

## 🧮 Calculator

### CALC-2 · TRIES-TO-SUCCESS

**Purpose:** how many tries should the cap allow?

**Inputs**

| Symbol | Meaning | Allowed range | Default |
|---|---|---|---|
| p | Chance a single try succeeds | above 0, below 1 | Estimate it from a few runs (for example, 2 successes in 5 runs → 0.4) |
| C | How sure you want to be that the loop finishes within the cap | above 0, below 1 | 0.90 for routine work, 0.95 or more when a failed run is expensive |
| n | Tries allowed (the cap) | 1 and up | The result below |

**Formulas**
- **Chance of success within n tries = 1 − (1 − p)ⁿ**
- **Tries needed = ⌈ln(1 − C) ÷ ln(1 − p)⌉**, where the ⌈ ⌉ brackets mean round up to the next whole number, and ln is the natural log (`LN` in spreadsheets)
- **Average tries to the first success = 1 ÷ p**
- For the curious, one line: with a cap of N, the average number of tries actually used is (1 − (1 − p)ᴺ) ÷ p, which is 1.94 for p = 0.5 and N = 5.

**Assumptions (each adjustable)**
- Every try is independent and has the same chance p. Loops with good feedback often do *better*, because each try learns from the last. Loops with a weak checker or a filling context can do worse.
- p comes from a small sample, so treat the answer as a starting cap and correct it from the run log (Level 5).

**Worked examples**
- **p = 0.5, C = 0.95:** ln(0.05) ÷ ln(0.5) = −2.996 ÷ −0.693 = 4.32 → round up → **5 tries**. Check: 1 − 0.5⁵ = 1 − 0.03125 = **0.969**. With 4 tries, 1 − 0.0625 = 0.9375, which falls short of 0.95. Average tries = 1 ÷ 0.5 = **2**.
- **p = 0.2, C = 0.90:** ln(0.10) ÷ ln(0.8) = −2.303 ÷ −0.223 = 10.32 → round up → **11 tries**. Check: 1 − 0.8¹¹ = 1 − 0.086 = **0.914**. With 10 tries, 1 − 0.107 = 0.893, which falls short. Average tries = 1 ÷ 0.2 = **5**.

![FIG-3.2: A line chart of the chance of success within n tries, for n from 1 to 15. Three curves: p = 0.8 reaches over 99 percent within 3 tries; p = 0.5 reaches 96.9 percent at 5 tries; p = 0.2 climbs slowly and reaches 91.4 percent at 11 tries. Dashed lines mark 90 and 95 percent.](assets/fig-3-2-tries-to-success.svg)

**FIG-3.2 · Chance of success within n tries** (CALC-2). *What to notice:* the low-p curve needs many tries to reach the same confidence. If your p is low, a better checker or a smaller step usually beats a bigger cap.

**Reading the result (bands are adjustable)**

| Tries needed | What it means |
|---|---|
| **5 or fewer** | Comfortable. Use it as your CAP. |
| **6–15** | Workable, but set a budget ceiling too (CALC-3, Level 4). |
| **More than 15** | The loop needs a better checker or smaller steps, not more tries. |

**Blank worksheet**
```text
CALC-2 · TRIES-TO-SUCCESS
p  (chance one try succeeds)          = ______
C  (confidence you want)              = ______
ln(1 − C)                             = ______
ln(1 − p)                             = ______
ratio = ln(1 − C) ÷ ln(1 − p)         = ______
Tries needed (round the ratio up)     = ______   → band: ______
Check: 1 − (1 − p)^tries              = ______   (should be ≥ C)
Average tries to first success = 1÷p  = ______
```

**Spreadsheet formulas** (Google Sheets and Excel), with p in B2, C in B3, and a cap n in B4:
```text
Tries needed:              =ROUNDUP(LN(1-B3)/LN(1-B2)-1E-9,0)
Chance of success within n: =1-(1-B2)^B4
Average tries:             =1/B2
```
The tiny `-1E-9` guards against rounding error: when the ratio is exactly a whole number (p = 0.5 and C = 0.75 gives exactly 2), a computer can store it as 2.0000000000000004, and rounding up would wrongly give 3.

**Workbook sheet:** `CALC-2 Tries` in [`workbook/loop-engineering-workbook.xlsx`](workbook/loop-engineering-workbook.xlsx), with a table of n = 1 to 20.

---

## 🗣 Council Debate

*Fresh context every run, or one long session?*

> **WHISPERER:** One long session keeps everything: the reasoning, the dead ends, the subtle decisions. A fresh agent has to rediscover them.
> **SMITH:** And one long session fills up, gets compacted, and quietly forgets the decision from turn 4. I've watched loops undo their own fixes that way.
> **WHISPERER:** Only if nobody wrote the decision down.
> **SMITH:** Exactly: so write it down, and then the fresh agent knows it too.
> **GOVERNOR:** Fresh runs are also easier to cap and kill. Each iteration is a separate process with a clean exit code.

**ORBIT's ruling:** fresh context with memory in files for anything longer than one sitting. One continuous session is fine for short loops whose whole history fits comfortably in the window, like a `/goal` run of a few turns.

---

## 🏋 Practice

Upgrade the Loop Spec you wrote in Level 1. (Layer: **Loop**.)

1. **LIMITS:** write one rule for each of the five families (EX-3.1).
2. **Estimate p:** run the task (by hand or with a simple prompt) 3–5 times and count successes. With 2 of 5, p = 0.4.
3. **Set the CAP with CALC-2:** choose C (0.90 is fine for practice) and compute the tries needed. For p = 0.4 and C = 0.90: ln(0.10) ÷ ln(0.6) = −2.303 ÷ −0.511 = 4.51, so round up to **5 tries**.
4. **STATE:** decide which files hold the loop's memory, and copy [`kit/progress.md`](kit/progress.md) as your template.
5. **ESCALATION:** write the five-part escalation note (EX-3.2) the loop should leave you.
6. **Isolation:** name the branch (and worktree, if you'll run loops in parallel).

**Done when:** your spec's LIMITS box has all five families, the CAP came from CALC-2, and a fresh agent could resume from your STATE files alone.

---

## ✔ Level-Up Check

1. **Name the five stop families, and say which is the success exit.**
   *Answer:* DONE (success), CAP, STUCK, DANGER, HUMAN.
2. **What goes into an escalation note?**
   *Answer:* the goal, why it stopped, what it tried, the evidence (last checker message and diff), and its best guess, marked as a guess.
3. **Why do long loops keep their memory in files?**
   *Answer:* the context window fills up and gets compacted, and new sessions start empty. Files survive both (BP-3.2).
4. **p = 0.5, and you want 95% confidence. What cap does CALC-2 give?**
   *Answer:* ln(0.05) ÷ ln(0.5) = 4.32, so round up to 5 tries (chance of success 96.9%).
5. **Two loops keep undoing each other's edits. What's the fix?**
   *Answer:* one workspace per loop: a separate worktree on its own branch (TRK-3.2).

⬅ [Level 2](02-level-2-apprentice.md) · 🏠 [README](README.md) · [Level 4](04-level-4-author.md) ➡
