# Level 0 · ZERO: What a loop is, and why prompting by hand runs out

⬅ [README](README.md) · 🏠 [README](README.md) · [Level 1](01-level-1-starter.md) ➡

**You'll be able to:**
- say what a loop is, and how it differs from a single prompt;
- name the three jobs you already do in every chat (prompt, judge, decide) and the six stages of a loop;
- place loop engineering after prompt, context, and harness engineering;
- run your first loop by hand and see exactly which parts a system could take over.

---

## The Lesson

### One prompt is one shot

A prompt is a single request: you ask, Claude answers, done. If the answer is wrong, nothing happens unless someone notices and asks again.

A **loop** is different. It's a small system that asks, checks the answer, and decides whether to ask again. You already trust loops like this every day:

- **A thermostat** reads the room, compares it with the number you set, and turns the heat on or off. Then it reads the room again.
- **Spell-check** marks a word, you fix it, it checks again, and the red line goes away.
- **A student with an answer key** works a problem, checks it, and redoes it until the answer matches.

Each one has the same parts: something that **acts**, something that **checks**, and a **rule for when to stop**.

### You have been the loop all along

Think about your last long chat with Claude. You asked for a draft. You read it and judged it ("too long", "wrong tone", "missing the date"). You decided whether to go again, and you typed the next prompt. Then you did it again.

In that chat, you did three jobs:

1. **Prompt:** write the next request.
2. **Judge:** decide whether the answer is good enough.
3. **Decide:** choose whether to go again, change direction, or stop.

![FIG-0.3: On the left, a person doing three jobs in a chat: write the next prompt, judge the answer, decide to go again or stop. On the right, a loop system doing the same jobs with a prompt file, a checker, and stop rules, while the person designs the system and handles escalations.](assets/fig-0-3-you-are-the-loop.svg)

**FIG-0.3 · You have been the loop.** In a chat, you do all three jobs by hand. Loop engineering hands them to a system you design. *What to notice:* you don't disappear. You move from doing every turn to designing the system and handling what it can't.

**Loop engineering** is designing the system that does those jobs for you. The working definition this guide uses:

> Loop engineering is designing the system that prompts an AI agent for you: what starts each run, the goal it works toward, the tools and context it gets, how its work gets checked, what it writes down between runs, and when it stops or calls a human.

An **agent** here means an AI model that can take actions (read files, run commands, edit documents), not just reply with text. Claude Code is an agent; so is Claude with tools in the Claude app.

### The core cycle

Every loop in this guide runs the same cycle:

![FIG-0.1: Six stages in a row: trigger, plan, act, observe, verify, decide. From decide, arrows lead back to plan to continue or retry, forward to stop when done, and up to a human to escalate. A state bar under all six stages shows that the loop writes down what happened after every turn.](assets/fig-0-1-core-cycle.svg)

**FIG-0.1 · The core cycle.** *What to notice:* "decide" has four exits, not one. A loop that can only "continue" is a loop that never stops.

| Stage | What happens | In a loop that fixes failing tests |
|---|---|---|
| **Trigger** | Something starts a run | You press go, a 2 a.m. schedule fires, or a new test fails |
| **Plan** | Pick the next small piece of work | "The next failing test is `test_refund_rounding`" |
| **Act** | Do it with tools | Edit the code |
| **Observe** | Collect what actually happened | Run the tests, read the output |
| **Verify** | A checker says "pass" or "not yet" | A separate check confirms the tests pass *and* no test file changed |
| **Decide** | Continue, retry, escalate, or stop | Stop: done. Or try again, or hand it to you |

Under all six sits **state**: what the loop writes down after every turn (a progress file, a log, a git commit) so the next turn, or the next run, knows what already happened.

### Where loop engineering came from

Loop engineering didn't replace the skills before it. It wraps them.

![FIG-0.2: Four nested boxes. The innermost is prompt engineering, the words of one request. Around it is context engineering, everything in the model's window for one request. Around that is harness engineering, the tools, permissions, and runtime around the model. The outermost is loop engineering, the repeating system that runs all of it.](assets/fig-0-2-four-layers.svg)

**FIG-0.2 · Four layers.** *What to notice:* each layer contains the one before it. Prompts still matter; they just live inside the loop now.

- **Prompt engineering** is choosing the words of one request.
- **Context engineering** is choosing everything in the model's window for one request: instructions, files, examples, history. The term spread in 2025.
- **Harness engineering** is the machinery around the model: which tools it can use, what it's allowed to do, where it runs.
- **Loop engineering** is the repeating system that runs all of it, turn after turn, without you typing each prompt.

**A short history (⚠VERIFY the names and dates before you quote them).** The name spread in June 2026. Peter Steinberger posted that you shouldn't be prompting coding agents anymore; you should be designing loops that prompt your agents. Addy Osmani named the practice in an essay called "Loop Engineering". Boris Cherny, who leads Claude Code at Anthropic, has been quoted saying loops he writes now do his prompting. On June 30, 2026, Anthropic published "Loop Engineering: Getting Started with Loops", which describes loops as "agents repeating cycles of work until a stop condition is met." By August, researchers were measuring how often loop building blocks show up in open-source projects. Sources are in [`12-sources.md`](12-sources.md).

The idea itself is old. Engineers have built feedback loops for centuries: the spinning-ball governor on steam engines, the thermostat, the cruise control in a car. Industrial "control-loop engineering" (instrument loops and PID tuning in factories) shares the name and the feedback idea, but it's a different field. This guide is about loops that prompt AI agents.

### What a loop can't do

A loop gives a model **more tries and better feedback**. It doesn't give the model knowledge it doesn't have. If Claude doesn't know a fact, running it fifty times won't teach it; a good check will only catch the wrong answers faster.

That's why the **check** is the most important part of any loop. A loop with a weak check makes mistakes faster, and it does so while you're not watching. Level 2 is all about checks.

### Loop, prompt, guide: three things to keep apart

| Layer | What it is | Example |
|---|---|---|
| **Loop** | The system: trigger, goal, tools, check, state, stop rules | "Every night, fix failing tests until they pass, at most 5 tries, then tell me" |
| **Prompt** | The words the loop hands its agent (or its checker) each run | The `PROMPT.md` file that loop reads every time |
| **Guide** | What you're reading | This folder |

When you design a loop, you write both: the loop (the system) and the prompt (its words). Beginners often write only the prompt and wonder why nothing stops.

---

## 🧪 Examples

**EX-0.1 · The same task, as a prompt and as a loop**
- ❌ **Before (a prompt):** "Write a product description for my coloring book." You read it, don't love it, type "make it better", and repeat until you're tired.
- ✅ **After (a loop, written as a spec):**
  ```text
  GOAL:      a product description for "Garden Friends" coloring book
  DONE WHEN: 120–150 words, names the age range and page count,
             and a separate checker rates every rubric line 4/5 or higher
  CHECKER:   a second chat with the rubric, which answers "pass" or the failing line
  LIMITS:    at most 4 rounds; then I pick the best draft myself
  ```
- **What changed and why:** the loop has a finish line a checker can see, a checker that isn't the writer, and a limit. "Make it better" has none of the three, so it never ends on its own.

**EX-0.2 · "Done" as a feeling vs "done" as a check**
- ❌ **Before:** "Keep improving the lesson plan until it's good."
- ✅ **After:** "Done when the lesson plan has an opening question, three discussion questions, and a closing prayer; takes 45 minutes or less at the stated timings; and every Scripture reference is written out as book, chapter, and verse."
- **What changed and why:** "good" lives in your head. The new version can be checked by someone else, or by a script, without asking you.

---

## ✅ Best Practices

**BP-0.1 · Name the three jobs before you automate any of them**
- **The practice:** for any task you want to loop, write one sentence each for *prompt* (what gets asked each round), *judge* (how an answer is graded), and *decide* (when to go again or stop).
- **Why it works:** you can only hand over a job you can describe. The sentence you can't write shows you which job still needs you.
- **How to check you did it:** three sentences on paper, and none of them says "use my judgment."

**BP-0.2 · Write the check before the first prompt**
- **The practice:** before you ask for a single draft, write down how you'll know it's right.
- **Why it works:** the check decides whether a loop converges. A strong prompt with a vague check drifts; a plain prompt with a sharp check gets there.
- **How to check you did it:** a stranger could read your check and grade a draft the same way you would.

**BP-0.3 · Run three rounds by hand first**
- **The practice:** before you automate anything, run the loop yourself for three rounds in a chat (the Hand Loop in the Practice section below).
- **Why it works:** you discover the real failure modes (vague rubric, answers that fix one thing and break another) for free, before a script repeats them fifty times.
- **How to check you did it:** a short journal of three rounds, with what you checked and what you asked for next.

---

## 💡 Tips

**TIP-0.1 · Keep a one-line loop journal.** After each round, write one line.
```text
R1 checked: word count 212 (fail). Asked: cut to 150, keep the date.
R2 checked: 148 words, date present, tone stiff (fail). Asked: warmer, same length.
```

**TIP-0.2 · Put the rubric in the first message,** so every round is judged against the same bar.
```text
Rubric (I'll grade every draft against this):
1. 90–110 words  2. includes {{DAY}}, {{TIME}}, {{PLACE}}  3. warm, no church jargon
```

**TIP-0.3 · Use a second chat as the judge.** Paste the rubric and the draft into a fresh chat and ask only for a verdict.
```text
Grade this draft against the rubric. Reply "PASS" or the first failing rubric line, quoting the failing words.
```

---

## 🎯 Tricks

**TRK-0.1 · Paste the check result as the next prompt**
- **When to use it:** whenever a round fails.
- **How:** instead of writing a new request, paste the judge's exact finding: "Rubric line 1 fails: 131 words. Fix only this."
- **What it buys you:** smaller, targeted fixes and fewer new mistakes. It's also exactly what an automated loop does, so you're practicing the real thing.

**TRK-0.2 · Ask for the smallest next change, not a rewrite**
- **When to use it:** when each round "improves" the draft but breaks something that was already right.
- **How:** "Change only the second paragraph. Keep everything else word for word."
- **What it buys you:** stable progress. Rewrites reset everything you already checked; small changes keep it.

---

## 🛠 Hacks

**HCK-0.1 · A kitchen timer as your first cap**
- **The move:** set a 15-minute timer before a hand loop. When it rings, stop, pick the best draft so far, and write one line about why the loop didn't finish.
  ```text
  Timer: 15 min. Best draft: R3. Didn't finish because rubric line 3 ("warm") has no clear test.
  ```
- **The trade-off:** a time cap is arbitrary; some tasks honestly need longer. It backfires if you treat it as a deadline for quality rather than a signal that the loop design needs work. Its job is to teach you that every loop needs a stop rule.

---

## ⛔ Things to Avoid

**AVD-0.1 · The endless polish loop**
- **Symptom:** round 12, each draft "slightly better", no end in sight.
- **Cause:** no done condition, so nothing can ever say "stop".
- **Fix:** write DONE WHEN before round 1.
  - ❌ "Keep improving it." → ✅ "Done when all three rubric lines pass, or after 4 rounds."

**AVD-0.2 · Judging by mood**
- **Symptom:** you accept round 3 because you're tired, and reject a better round 2 because you were fresh.
- **Cause:** no written rubric, so the bar moves with your energy.
- **Fix:** three rubric lines, written first (TIP-0.2), used every round.
  - ❌ "Looks fine." → ✅ "Line 1 pass (104 words), line 2 pass, line 3 fail (uses 'fellowship hour')."

**AVD-0.3 · Automating a task you've never done by hand**
- **Symptom:** a script runs 30 rounds overnight and produces 30 versions of the same mistake.
- **Cause:** you automated before you knew what "wrong" looks like for this task.
- **Fix:** three hand rounds first (BP-0.3); automate only the jobs you could describe.
  - ❌ "Run it overnight and see." → ✅ "Run it by hand three times, write the rubric the failures taught me, then automate."

---

## 🗣 Council Debate

*Should beginners run a loop by hand before automating anything?*

> **SHERPA:** Yes. The hand loop teaches the judging job, and judging is the part beginners skip.
> **SMITH:** Hand loops are slow and people quit. The kit's dry run shows the whole mechanism in two minutes.
> **SHERPA:** The dry run shows the mechanism, not the judgment. It passes because the mock says so.
> **GOVERNOR:** And someone who's never judged a round by hand won't notice when an automated checker is too lenient.
> **SMITH:** Then keep it short. Three rounds, not ten.

**ORBIT's ruling:** three hand rounds, time-boxed to 15 minutes, then the dry run in Level 4. The hand rounds teach you what a good check looks like, which no script can teach you.

---

## 🏋 Practice: The Hand Loop

Run this in a fresh Claude chat. It costs nothing but 15 minutes. (Layer: this is a **Loop** you run by hand; the text you paste is its **Prompt**.)

1. **Set the task and rubric.** Paste:
   ```text
   Write a 100-word invitation to a six-week small-group study on the Sermon on the Mount.
   Use {{DAY}}, {{TIME}}, and {{PLACE}} as placeholders.
   Rubric I'll grade against:
   1. 90–110 words  2. includes all three placeholders  3. warm and plain, no church jargon
   ```
2. **Judge in a second chat** (TIP-0.3). Paste the rubric and the draft; ask for "PASS" or the first failing line.
3. **Feed the finding back** (TRK-0.1): paste the judge's exact words into the first chat with "Fix only this."
4. **Repeat for three rounds**, keeping a one-line journal (TIP-0.1).
5. **Label your own jobs.** Next to each journal line, write P (you prompted), J (you judged), or D (you decided).

**What you should notice:** the judging (J) was the hard part, and rubric line 3 ("warm") was the fuzziest. That fuzziness is what Level 2 fixes.

---

## ✔ Level-Up Check

1. **What three jobs do you do when you are the loop?**
   *Answer:* prompt (write the next request), judge (grade the answer), and decide (go again, change course, or stop).
2. **Name the six stages of the core cycle. Where does state get written?**
   *Answer:* trigger, plan, act, observe, verify, decide. State is written down after every turn: a progress file, a log, or a commit.
3. **Why can't a loop make Claude know a fact it doesn't know?**
   *Answer:* a loop adds tries and feedback, not knowledge. A good check can reject wrong answers, but it can't supply the missing fact.
4. **How is loop engineering different from prompt engineering?**
   *Answer:* prompt engineering chooses the words of one request. Loop engineering designs the repeating system around them: trigger, check, state, and stop rules. The prompt lives inside the loop.
5. **Which job should you design first, and why?**
   *Answer:* the check (BP-0.2), because it decides whether the loop ever converges and stops.

⬅ [README](README.md) · 🏠 [README](README.md) · [Level 1](01-level-1-starter.md) ➡
