# Level 6 · HERO: Loop systems and meta-loops

⬅ [Level 5](05-level-5-expert.md) · 🏠 [README](README.md) · [Case Study Lab](07-case-study-lab.md) ➡

**You'll be able to:**
- see a working system as loops inside loops, each with its own checker and clock;
- choose a team shape: one agent, a maker/checker pair, or an orchestrator with workers;
- build a meta-loop that improves prompts without gaming its own check;
- climb the autonomy ladder on evidence, and run a small library of loops with the Loop Generator.

---

## The Lesson

### Loops of loops

Once you have a few loops running, you'll notice they nest. Each ring has its own clock and its own checker:

![FIG-6.1: Three concentric rings. Inner loop: the agent's turns, seconds to minutes, checked by tests and linters. Middle loop: one task or pull request, hours, checked by CI and a reviewer. Outer loop: evals and improvements to prompts, checkers, and caps, days to weeks, checked by the golden set and by you. The human sits in the outer ring.](assets/fig-6-1-loops-of-loops.svg)

**FIG-6.1 · Loops of loops.** *What to notice:* you live in the outer ring. The further out a loop is, the more its checker should involve a person.

| Ring | What turns | Clock | Its checker |
|---|---|---|---|
| **Inner** | The agent's turns inside one run | Seconds to minutes | Tests, linters, exact-match checks (Level 2) |
| **Middle** | One task: a pull request, a lesson, a report | Hours | CI, a reviewer agent, your approval at rung 3 |
| **Outer** | The loop itself: its prompt, checker, and caps | Days to weeks | The golden set (Level 5) and you |

Most trouble comes from rings that leak into each other: an inner loop that edits its own checker, or an outer-loop change made in the middle of a run. Keep each ring's job separate.

### Team shapes

More agents aren't automatically better. Every extra agent adds cost, coordination, and a new way to fail. Three shapes cover most needs:

![FIG-6.2: Three team shapes side by side. One agent with a script checker: the default, for small checkable tasks. A maker and checker pair: a second agent with fresh context reviews the first, for work a script can't fully check. An orchestrator with workers: one agent plans and splits the work, several workers run in separate worktrees, and a checker merges results, for large jobs made of many independent pieces.](assets/fig-6-2-team-shapes.svg)

**FIG-6.2 · Team shapes.** *What to notice:* each step to the right adds a checker, not just more makers.

1. **One agent plus a script checker.** The default. Most loops in this guide use it.
2. **A maker/checker pair.** A second agent with fresh context reviews the first one's work. Use it when a script can't check everything, such as tone, teaching quality, or design. Anthropic's loops guide gives the reason: a reviewer with fresh context is less biased.
3. **An orchestrator with workers.** One agent splits a large job into independent pieces, workers handle them in separate worktrees (Level 3), and a checker merges the results. Use it for big, parallel jobs like upgrading forty packages. Don't use it for one tricky bug.

### Meta-loops: loops that improve prompts and loops

A **meta-loop** works on another loop instead of on the task itself. For example, it might propose a better `PROMPT.md`, test it on the golden set, and report whether it helped. This is where loop engineering loops back to prompt engineering. It's powerful, and it's also the easiest place to fool yourself, because a meta-loop can "improve" its way into gaming its own check (AVD-6.1).

Three guard rails make meta-loops safe:

1. **A fixed eval set:** the golden set (Level 5) doesn't change while the meta-loop runs.
2. **A locked checker:** the meta-loop may propose changes to the *prompt*, never to the checker or the golden set. Checker changes are made by a person, versioned, and re-calibrated (CALC-1).
3. **Proposals, not pushes:** the meta-loop writes a proposal (the diff plus before-and-after numbers) and a person approves it. That's rung 3 at the outer ring.

### The autonomy ladder, in full

![FIG-6.3: A four-rung ladder. Rung 1, watch: reads and reports, with read-only permissions. Rung 2, suggest: proposes drafts or diffs that a person applies. Rung 3, act with approval: changes its own branch or outbox, and nothing counts until a person approves. Rung 4, act alone: acts within caps, with a person reviewing afterward, spend alerts, and a kill switch. Beside each step up, the evidence needed to climb. A red band marks money, health, legal, and production work as stopping at rung 3.](assets/fig-6-3-autonomy-ladder.svg)

**FIG-6.3 · The autonomy ladder.** *What to notice:* you climb on evidence, one rung at a time. Some work never goes above rung 3, however good the loop gets.

| Rung | The loop may | Governance at this rung | Evidence to climb to the next rung (adjustable) |
|---|---|---|---|
| **1 · Watch** | Read and report | Read-only permissions; output goes to a report | Its reports are accurate on spot checks for two weeks |
| **2 · Suggest** | Propose drafts or diffs | No writes to shared state; you apply the changes | A week of suggestions you'd have accepted; CALC-4 ≥ 75 |
| **3 · Act with approval** | Change its own branch or outbox | Branch protection; your approval; run log and commits as the audit trail | 20+ approved runs with no reverts; CALC-1 trust ≥ 95%; CALC-4 ≥ 90 |
| **4 · Act alone** | Act within its caps | Everything above, plus spend alerts, a kill switch, and weekly spot checks | Stay here only while the numbers hold |

**Hard ceiling:** loops that touch money, health, legal matters, or production systems stop at rung 3. That's the SAFE-LOOP rule this guide was written under, and it doesn't bend for a good track record.

### Keeping a loop library healthy

A handful of loops is easy to manage. Twenty is a system, and systems need housekeeping:

- **A registry:** one table listing every loop's name, version, owner, rung, monthly ceiling, and next review date (TIP-6.2).
- **Versions and changelogs:** from Level 5, for every loop.
- **Retirement dates:** every loop gets a date on which you decide whether to renew it or turn it off (BP-6.3).
- **A shared kit:** one `loop.sh`, one Loop Spec template, and one prompt template, reused by every loop, so a fix in one place helps all of them.

### The Loop Generator: your own "best loop engineer" prompt

Everything in this guide fits into one prompt you can reuse: [`kit/loop-generator.prompt.md`](kit/loop-generator.prompt.md). Give it a one-paragraph goal, and it:

- asks up to three questions, only when an answer would change the design, and otherwise states its assumptions;
- fills in the nine-box Loop Spec and places the loop on the autonomy ladder (never above rung 3 for money, health, legal, or production work);
- writes the loop's `PROMPT.md`;
- sets the checker plan with CALC-1, the cap with CALC-2, and the budget with CALC-3, with prices left blank for you;
- scores the design on CALC-4, fixes every criterion rated below 4, and reports the final ratings honestly;
- lists your FIELD WORK and every ⚠VERIFY item.

How to use it: open a fresh Claude chat (or Claude Code), paste the whole file, then send your goal:
```text
GOAL: Every Monday, check our church website's event pages and flag any event with a
missing date, time, or place. I'm not technical. Nothing should be published without me.
```
You'll get back a filled Loop Spec at rung 2 (suggest), a `PROMPT.md`, a deterministic checker plan (three required fields per event page), caps, a budget with blank prices, and a score with its fixes. That's the whole build checklist from the README, done in one pass, and it's yours to review.

---

## 🧪 Examples

**EX-6.1 · A meta-loop: unsafe vs guarded** *(layer: Loop, a meta-loop)*
- ❌ **Before:**
  ```text
  Loop: improve PROMPT.md until the judge scores every lesson 5/5.
  (The loop can edit PROMPT.md and the judge's rubric. No fixed test set.)
  ```
- ✅ **After:**
  ```text
  Meta-loop (outer ring, rung 3):
  EACH RUN   propose ONE change to PROMPT.md, then run the golden set (10 fixed lessons)
             with the LOCKED checker (rubric + verse check, both in PROTECT)
  OUTPUT     proposals/YYYY-MM-DD.md: the diff, and golden-set numbers before → after
  LIMITS     3 proposals per week · CAP 5 iterations per proposal · ceiling from CALC-3
  HUMAN      I approve or reject each proposal; checker changes are mine alone
  ```
- **What changed and why:** the unsafe loop could reach "5/5" by softening its own rubric. The guarded one can't touch the checker or the test set, and its best possible outcome is a proposal you decide on.

**EX-6.2 · Picking a team shape** *(layer: Loop)*
- ❌ **Before:** "Use five agents for everything. More agents, more speed."
- ✅ **After:**
  ```text
  Fix one failing test           → one agent + test script
  Write a lesson, check quotes   → maker/checker pair (+ exact-match verse check)
  Upgrade 40 packages            → orchestrator + workers in 40 worktrees + CI as checker
  ```
- **What changed and why:** the shape follows the work. Parallel workers help only when the pieces are independent; a checker helps whenever a script can't see everything.

---

## ✅ Best Practices

**BP-6.1 · Keep the outer loop human**
- **The practice:** changes to a loop's checker, caps, rung, and golden set are made or approved by a person, never by the loop.
- **Why it works:** the outer ring decides what "good" means. A system that grades its own grading can drift anywhere, while every inner number still looks fine.
- **How to check you did it:** every changelog entry that touches a checker, cap, or rung names the person who approved it.

**BP-6.2 · Lock the checker whenever a loop edits prompts**
- **The practice:** any loop that may change a prompt runs with the checker files and the golden set in `PROTECT` (DANGER on change).
- **Why it works:** it removes the cheapest way for a meta-loop to "improve", which is making the test easier.
- **How to check you did it:** try editing the rubric during a meta-loop dry run; the loop should stop with DANGER (exit 5).

**BP-6.3 · Give every loop an owner and a retirement date**
- **The practice:** each loop in the registry has a named person and a date to renew or retire it.
- **Why it works:** forgotten loops keep spending and acting long after anyone remembers why. Claude Code builds the same idea into `/loop`, where recurring tasks expire after seven days (⚠VERIFY).
- **How to check you did it:** no row in your registry has a blank owner or a review date in the past.

---

## 💡 Tips

**TIP-6.1 · Start with one agent, and add a second only for checking.**
```text
v1: one agent + script check  →  v2 (if a script can't see tone): + one reviewer agent
```

**TIP-6.2 · Keep a loop registry.** One table for every loop you run:
```text
| Loop       | Version | Owner | Rung | Monthly ceiling | Review by  |
| docs-links | v1.2    | you   | 3    | $6.00           | 2026-12-01 |
```

**TIP-6.3 · Set spend alerts at 50% and 80% of the monthly ceiling,** so you hear about trouble before the cap does the talking.
```text
ALERT at $9.00 (50% of $18.00) · ALERT at $14.40 (80%) · CAP at $18.00
```

---

## 🎯 Tricks

**TRK-6.1 · Parallel workers in worktrees, merged by a checker**
- **When to use it:** a large job that splits into many independent pieces (one package, one page, one lesson each).
- **How:** the orchestrator writes a task list; each worker takes one task in its own worktree and branch; a checker (CI plus a reviewer) passes each branch before a person merges it.
- **What it buys you:** speed without collisions. Each worker's failure stays in its own branch, and STUCK in one worker doesn't block the others.

**TRK-6.2 · Let a loop propose its own stop rules, for your approval**
- **When to use it:** after a few weeks of run logs, when you're unsure what the caps should be.
- **How:** ask the loop (or the Loop Generator) to read the run log, and propose new CAP and STUCK values with CALC-2 arithmetic shown. You approve or edit, and the change goes in the changelog.
- **What it buys you:** caps grounded in your real data instead of guesses, without letting the loop loosen its own limits unsupervised.

---

## 🛠 Hacks

**HCK-6.1 · Run the Loop Generator on its own output**
- **The move:** after the Loop Generator designs a loop, paste that design back into a fresh chat with the generator and send `GRADE-LOOP` (or ask it to "score this design on CALC-4 and name the three fixes worth the most points").
  ```text
  [paste the generated Loop Spec + PROMPT.md]
  Score this on CALC-4 as a skeptical reviewer. Name the three fixes worth the most points.
  ```
- **The trade-off:** it's a model grading a model's design, with the same blind spots, so it catches gaps (a missing STUCK rule) better than judgment errors (a wrong rung). It backfires if you treat the second score as proof. Use it to find fixes, and let your own review decide.

---

## ⛔ Things to Avoid

**AVD-6.1 · The self-grading meta-loop**
- **Symptom:** the meta-loop's scores climb every week, but the lessons (or code) don't get better when you read them.
- **Cause:** the meta-loop could change the rubric, the golden set, or both, so it improved the grading instead of the work.
- **Fix:** lock the checker and the golden set (BP-6.2); proposals only (EX-6.1).
  - ❌ `improve until the judge gives 5/5` → ✅ `propose one prompt change; score on the locked golden set; I decide`

**AVD-6.2 · Loop sprawl**
- **Symptom:** you find loops nobody remembers creating, running on old versions, with no owner.
- **Cause:** loops were easy to start, and nothing tracked them.
- **Fix:** a registry (TIP-6.2), owners and review dates (BP-6.3), and a monthly ten-minute review.
  - ❌ "There are a few loops running somewhere." → ✅ "The registry lists 6 loops; 2 are due for review this month."

**AVD-6.3 · Climbing the autonomy ladder too fast**
- **Symptom:** a loop that did well for three days is moved to rung 4, and on day five it does something you wouldn't have approved.
- **Cause:** promotion on a good feeling instead of evidence.
- **Fix:** climb one rung at a time, only when the evidence column of the ladder is met.
  - ❌ "It's been great, let it merge on its own." → ✅ "20 approved runs, 0 reverts, trust 96%, CALC-4 91: moving from rung 3 to 4, with alerts on."

---

## 🗣 Council Debate

*Should a loop ever edit its own prompt, or its checker?*

> **ANVIL:** Prompts, yes. A meta-loop that tests prompt changes on a golden set finds improvements faster than I can.
> **GOVERNOR:** As a proposal. The moment it can merge its own prompt change, it's grading itself.
> **ANVIL:** Agreed: proposals, with numbers. But the checker is different.
> **GOVERNOR:** The checker is never the loop's to touch. It defines "good". Change it and every number after that is meaningless.
> **RAZOR:** And re-measure trust (CALC-1) after every human change to the checker, too.

**ORBIT's ruling:** a loop may *propose* changes to its own prompt, tested on a locked golden set and approved by a person. It may never change its checker or its golden set. Those changes are human, versioned, and followed by re-calibration.

---

## 🏋 Practice

The capstone. (Layer: the Loop Generator is a **Prompt** that designs **Loops**.)

1. Open [`kit/loop-generator.prompt.md`](kit/loop-generator.prompt.md), paste it into a fresh Claude chat, and send a one-paragraph goal from your own work.
2. Read the Loop Spec it returns. Check the rung against the ladder and the hard ceiling.
3. Grade the design yourself with CALC-4 before you look at its self-score. Where do you disagree, and why?
4. Add the loop to a registry table (TIP-6.2), with an owner, a monthly ceiling from CALC-3 (using current prices), and a review date.
5. Write the evidence you'll need to climb one rung (the ladder's right-hand column).

**Done when:** you have a generated, reviewed Loop Spec with its `PROMPT.md`, a registry row, and a written promotion rule.

---

## ✔ Level-Up Check

1. **Name the three rings of a loop system, and the checker for each.**
   *Answer:* inner (tests and exact-match checks), middle (CI, a reviewer, your approval), and outer (the golden set and you).
2. **When is an orchestrator with workers the right shape?**
   *Answer:* for large jobs that split into many independent pieces, run in separate worktrees with a checker before merging. It's the wrong shape for one tricky bug.
3. **What are the three guard rails for a meta-loop?**
   *Answer:* a fixed eval set, a locked checker, and proposals instead of pushes (a person approves).
4. **A loop has 25 approved runs, no reverts, trust of 96%, and a CALC-4 score of 91. It sends invoices. Can it move to rung 4?**
   *Answer:* no. It handles money, so it stops at rung 3, whatever its numbers.
5. **What does the Loop Generator do with prices?**
   *Answer:* leaves them blank for you to fill in from the current pricing page (FIELD WORK); it never fills them in from memory.

⬅ [Level 5](05-level-5-expert.md) · 🏠 [README](README.md) · [Case Study Lab](07-case-study-lab.md) ➡
