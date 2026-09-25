# FAQ

⬅ [Case Study Lab](07-case-study-lab.md) · 🏠 [README](README.md) · [Calculator Toolkit](09-calculator-toolkit.md) ➡

Thirty questions learners actually ask, grouped by level. Each answer starts with the short version.

---

## Level 0 · What a loop is

**❓ FAQ-1 · Is loop engineering new, or just a new name for agents?**
The name is new (it spread in June 2026); the ideas are older. Agents that act, check, and try again existed before, and engineers have built feedback loops for centuries. What's new is the focus: instead of prompting an agent turn by turn, you design the system that prompts it for you, with a trigger, a checker, state, and stop rules. Naming that practice made it easier to teach and compare. See [Level 0](00-level-0-zero.md) and [`12-sources.md`](12-sources.md).

**❓ FAQ-2 · Do I need to code to use loops?**
No. You can run your first loops by hand in a chat (the Hand Loop), with Claude Code's `/goal` and `/loop` commands, or with a routine, none of which needs code. The kit's `loop.sh` is short and explained line by line in Level 4, and you can run its dry run without changing a character. Coding helps most with checkers: a small script is often the best check you can have.

**❓ FAQ-3 · How is a loop different from a prompt chain or a workflow?**
A chain runs fixed steps once, in order; a loop repeats until a check says "done" or a stop rule fires. In a chain, step 3 always follows step 2. In a loop, what happens next depends on what the checker saw: go again, retry, escalate, or stop. Many real systems mix the two, such as a chain whose middle step is a loop.

**❓ FAQ-4 · Will a loop make Claude smarter?**
No. It gives Claude more tries and better feedback, not more knowledge. If Claude doesn't know a fact, repeating the question won't teach it; a good checker will only catch the wrong answers faster. That's why loops shine on work with a checkable result, like passing tests or exact quotes, and why the checker matters more than the prompt.

**❓ FAQ-5 · Is this the same as control-loop engineering in factories?**
No, but they're cousins. Industrial control-loop engineering (instrument loops, PID tuning) keeps a physical process at a set point, like a thermostat does. AI loop engineering applies the same feedback idea to agents: act, measure, correct. The vocabulary overlaps, but the tools, risks, and skills are different. This guide covers only AI agents.

---

## Level 1 · Designing a loop

**❓ FAQ-6 · What's the smallest useful first loop?**
One that repeats, has a checkable finish line, and can't hurt anything. Good examples: fixing broken links in a docs folder on a branch, reformatting files until a linter passes, or checking that every event page has a date, time, and place. Run it through the five loop-worthiness questions (FIG-1.2); five yeses make a great first loop.

**❓ FAQ-7 · How do I write a good "done" condition?**
Describe the finished state as facts a script could check, plus anything that must not change. "All tests in `tests/auth` pass and lint is clean" is good; adding "and no file under `tests/` changed" makes it better. Avoid chores ("fix the code") and feelings ("make it great"). If a stranger couldn't grade it without asking you, rewrite it (BP-1.1).

**❓ FAQ-8 · Which trigger should I start with?**
By hand. Start each run yourself until you trust the loop, then move to a goal (`/goal`) for longer sessions, and only later to a schedule or an event. Each step away from "by hand" means you watch less, so the checker and limits must be stronger first (FIG-1.3).

---

## Level 2 · Checking the work

**❓ FAQ-9 · Can the same model check its own work?**
Not in the same conversation, as the same "maker". An agent grading its own work tends to see what it meant to do. A separate check works much better: a script, or a second agent with fresh context and its own rubric (ideally a different model). Even Claude Code's `/goal` hands completion checks to a separate evaluator model for this reason (⚠VERIFY). See BP-2.1.

**❓ FAQ-10 · What if my task has no automatic test?**
Build the strictest check you can, and stack it. Look for a borrowed deterministic check first: a word count, a required heading, an exact match against a source (HCK-1.1, TRK-2.1). For what remains, use a model judge with an anchored rubric, calibrated on samples you graded yourself. Keep a person on a sample of passes. If nothing can be checked at all, the task may not be loop-worthy yet.

**❓ FAQ-11 · How many samples do I need to calibrate a judge?**
Ten good and ten bad is enough to start, and it gives a rough estimate. That tells you whether the judge is roughly trustworthy (CALC-1). For decisions that matter, use more (40 + 40 gives much steadier numbers), and re-calibrate whenever you change the rubric or the model underneath changes.

**❓ FAQ-12 · Why did my loop pass when the work was wrong?**
Usually one of three reasons: the maker graded itself, the checker could be gamed, or the checker didn't cover what went wrong. Check the diff for skipped tests or special cases (AVD-2.2), confirm that the checker is separate (AVD-2.1), and look at what the check doesn't test. Then measure your false-pass rate with spot checks (BP-5.3).

---

## Level 3 · Stop rules and state

**❓ FAQ-13 · How many iterations should I allow?**
Use CALC-2: estimate the chance one try succeeds (p), pick how sure you want to be (C), and compute the tries needed. For p = 0.5 and 95% confidence, that's 5. If the answer is above 15, the loop needs a better checker or smaller steps, not a bigger cap. Always pair the cap with a STUCK rule and a time limit.

**❓ FAQ-14 · Fresh context every run, or one long session?**
Fresh context with memory in files, for anything longer than one sitting. Long sessions fill up and get compacted, and early decisions blur. A fresh agent that reads `progress.md` and the last commits starts clean and still knows where things stand. For short loops of a few turns, one session is fine (TRK-3.1).

**❓ FAQ-15 · What do I do when the loop keeps failing the same way?**
Let it stop. That's what the STUCK rule is for. Then read the escalation note: the same failure three times usually means a wrong requirement, a missing permission or setting, or a checker message that doesn't say enough. Fix the cause (sometimes a decision only you can make) rather than raising the cap. Feeding the last three attempts into the prompt can also help (HCK-5.1).

**❓ FAQ-16 · How do I stop a loop right now?**
Use the stop file, Ctrl+C, or the tool's own control. With the kit's script, run `touch .loop-stop` in the loop's folder (it stops before the next iteration), or press Ctrl+C. In Claude Code, `/goal clear` removes an active goal, and Esc stops a self-paced `/loop` that's waiting (⚠VERIFY). Know your off switch before the first run.

---

## Level 4 · Building and running loops

**❓ FAQ-17 · What's the difference between `/goal`, `/loop`, and routines in Claude Code?**
They differ in what starts the next turn (⚠VERIFY, as of September 2026). `/goal` keeps working turn after turn until a separate model judges your condition met or impossible. `/loop` re-runs a prompt on an interval, fixed or self-paced, while your session is open; recurring tasks expire after seven days. Routines are saved automations that run in Anthropic's cloud on a schedule, an API call, or a GitHub event, without your machine. See the table in [Level 4](04-level-4-author.md).

**❓ FAQ-18 · What is the Ralph Wiggum loop, and should I use it?**
It's a shell loop that feeds the same prompt file to a fresh agent until the work is done, credited to Geoffrey Huntley ("Ralph is a Bash loop"). It's a great pattern: fresh context, memory in files, tests as backpressure. The naive version has no cap, though, and Anthropic's Ralph plugin defaults to unlimited iterations (⚠VERIFY). Use it with every stop family, like the kit's `loop.sh`.

**❓ FAQ-19 · How do I keep a loop from running up a bill?**
Set a ceiling before the first run. Compute the ceiling per run and per month with CALC-3, using current prices. Enforce it with an iteration cap, a time cap, and a STUCK rule, and set spend alerts at 50% and 80% of the monthly ceiling (TIP-6.3). With `claude -p`, JSON output includes an estimated cost you can log (⚠VERIFY).

**❓ FAQ-20 · Is it safe to let a loop run overnight?**
Yes, at rung 3 with guard rails; not at rung 4 on day one. Safe overnight means its own branch or worktree, all five stop families, a known ceiling, protected checker files, least-privilege permissions, and your review of the log and diff in the morning before anything merges. Money, health, legal, and production work never runs unattended above rung 3.

**❓ FAQ-21 · Do loops work on a Claude subscription, or only with an API key?**
Both, depending on the feature (⚠VERIFY; plans change). In-session features like `/goal` and `/loop` run under your plan's usage. Claude Code's documentation says that `--bare` scripted runs use an API key instead of your subscription login. Either way, tokens measure how much a loop consumes, so CALC-3 still applies: as money on the API, or as usage on a plan.

**❓ FAQ-22 · Can a loop read my email or the web safely?**
Only if it can't act on what it reads. Outside text can contain instructions meant to hijack the agent (prompt injection). Split the work: a reader loop with no write permissions summarizes into a file, and a separate maker loop works from that file on a branch, at rung 3. Fence outside text as data in the prompt (TRK-4.2, AVD-4.3).

---

## Level 5 · Observing and improving

**❓ FAQ-23 · How do I know my loop is getting better, not just busier?**
Measure it on a fixed golden set, one change at a time. Track success rate, iterations per success, cost per success, and the false-pass rate from spot checks. A change that raises activity but not those numbers is busyness. Keep a changelog with before-and-after numbers for every version (BP-5.2, EX-5.2).

**❓ FAQ-24 · What should I log?**
One row per iteration, always in the same columns: iteration, time, action, check result, stop reason, tokens in and out, lines changed, and a short note. The kit's `loop.sh` writes exactly these, and the workbook's Run Log sheet computes the summary numbers from them (BP-5.1).

**❓ FAQ-25 · My loop worked for weeks and then got worse. Why?**
Something underneath changed: the model, the data, the tools, or the task itself. Common causes are a model update, a changed dependency, a file your loop relies on, or a drifting rubric. Re-run your golden set to confirm the drop, replay a recent failure with one change (TRK-5.2), and re-calibrate the checker if the model changed.

**❓ FAQ-26 · What's a good Loop Scorecard score?**
75 or more before it runs unattended; 90 or more before rung 4. Below 60, don't run it unattended; 60–74 means run it while you watch. The fastest gains are usually in the first four criteria (goal, checker, stop rules, safety), where each point is worth 3 (CALC-4).

---

## Level 6 · Loop systems

**❓ FAQ-27 · Can a loop improve its own prompt?**
Yes, as a proposal tested on a locked golden set and approved by you. It must never change its own checker or its golden set; if it can, it will "improve" by making the test easier. Keep checker changes human, versioned, and re-calibrated (BP-6.2, EX-6.1).

**❓ FAQ-28 · When should I use more than one agent?**
When one agent needs a checker a script can't provide, or when a big job splits into independent pieces. A maker/checker pair suits tone, design, and teaching quality. An orchestrator with workers in separate worktrees suits large parallel jobs. For a single tricky bug, one agent plus a good test is better (FIG-6.2).

**❓ FAQ-29 · How many loops can one person manage?**
As many as your registry and review time allow, which is usually fewer than you think. Every loop needs an owner, a review date, a ceiling, and someone reading its escalations. A ten-minute monthly review per handful of loops is a healthy pace. If escalations go unread, you have too many loops (TIP-6.2, AVD-6.2).

**❓ FAQ-30 · When should I retire a loop?**
When its job is done, its numbers slip, or nobody reads its output. Set a review date when you create it (BP-6.3), and at each review decide to renew, fix, or retire it. A retired loop's spec and changelog are worth keeping: they're the fastest start for the next similar loop.

⬅ [Case Study Lab](07-case-study-lab.md) · 🏠 [README](README.md) · [Calculator Toolkit](09-calculator-toolkit.md) ➡
