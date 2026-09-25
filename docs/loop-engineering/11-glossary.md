# Glossary

⬅ [Quick Reference](10-quick-reference.md) · 🏠 [README](README.md) · [Sources](12-sources.md) ➡

Every term this guide defines, in plain words. The level where it's taught is in brackets.

**Agent.** An AI model that can take actions (read files, run commands, edit documents), not just reply with text. Claude Code is an agent. [L0]

**Anchored rubric.** A grading rubric where each score has a short description of what it looks like, so "5" means the same thing every time. [L2]

**Auto mode.** A Claude Code permission mode in which a classifier reviews actions instead of asking you about each one. It removes prompts *within* a turn; `/goal` removes them *between* turns. ⚠VERIFY [L4]

**Autonomy ladder, rung.** Four levels of how much a loop may do alone: 1 watch, 2 suggest, 3 act with approval, 4 act alone. You climb one rung at a time, on evidence. Money, health, legal, and production work stops at rung 3. [L1, L6]

**Backpressure.** Checks that push back on every turn (failing tests, type errors, lint warnings), keeping a loop close to the goal. [L2]

**Build checklist.** The ten steps from goal to scored loop that organize this guide. [README]

**Ceiling (per run, monthly).** The most a loop can spend if every try fails: the iteration cap times the cost per iteration, and that times runs per month. [L4, CALC-3]

**Checker (verifier).** Whatever decides whether the work is done: a script, a separate agent with a rubric, or a person. Never the maker itself. [L2]

**Checksum.** In this guide, a worked example with exact inputs and results, used to test that a calculator, workbook, or chart is right. Also a fingerprint of a file (see *fingerprint*). [L2–L5]

**Claude Code.** Anthropic's agent for working in a code project from the terminal, desktop app, or web, with built-in loop features. ⚠VERIFY feature details [L4]

**Compaction.** When a long conversation fills the context window, older parts get summarized to make room, and details can blur. [L3]

**Context, context window.** Everything the model can see in one request: instructions, files, history. The window has a size limit. [L0, L3]

**Context engineering.** Choosing everything in the model's window for one request. The term spread in 2025. [L0]

**Context rot.** The slow loss of quality as a long session fills up and gets compacted. [L3, L5]

**Core cycle.** Trigger → plan → act → observe → verify → decide, with state written down after every turn. [L0]

**Deterministic check.** A check that gives the same answer every time for the same input: tests, type checks, linters, schema validation, word counts, exact match. [L2]

**Dry run.** Running a loop with a harmless mock instead of a real agent, to test its plumbing for free. The kit's `loop.sh` does this by default. [L4]

**Escalation, escalation package.** What a loop hands a person when it stops without success: the goal, why it stopped, what it tried, the evidence, and its best guess. [L3]

**Eval, golden set.** A fixed set of test tasks with known answers, run after every change so versions can be compared fairly. [L5]

**False-pass rate (F).** The share of wrong work that the checker passes anyway. Measured with spot checks. [L2, L5]

**FIELD WORK.** Something only you can supply, such as current prices, a source text, or your own data exports. The guide never fills these in from memory. [All]

**Fingerprint.** A checksum of a set of files (the kit uses `cksum`). If the fingerprint changes, a file changed. The kit uses this for DANGER. [L2, L4]

**Goal (end state).** What the world looks like when the work is done, written so a machine can check it. The opposite of a chore. [L1]

**Harness, harness engineering.** The machinery around a model (tools, permissions, runtime), and the skill of designing it. [L0]

**Headless run.** A non-interactive run of Claude Code from a script, with `claude -p`. It exits with a status code a script can read. ⚠VERIFY flags [L4]

**Hook.** A script or prompt Claude Code runs at a set moment. A **Stop hook** runs when Claude finishes a turn and can send it back to work; a **PreToolUse hook** runs before a tool call and can deny it. ⚠VERIFY [L4]

**Iteration.** One pass through the loop: act, observe, verify, decide. [L0]

**Isolation.** Giving each loop its own workspace (a branch, worktree, or container) so mistakes stay contained. [L3]

**Kill switch, stop file.** A way for a person to stop a loop at once. In the kit, creating `.loop-stop` stops `loop.sh` before its next iteration. [L3]

**Least privilege.** Allowing a loop exactly the tools and permissions it needs, and nothing more. [L4]

**Loop.** A system that prompts an AI agent, checks the result, writes down what happened, and decides whether to go again. [L0]

**Loop engineering.** Designing the system that prompts an AI agent for you: what starts each run, the goal it works toward, the tools and context it gets, how its work gets checked, what it writes down between runs, and when it stops or calls a human. [L0]

**Loop Generator.** The kit's reusable prompt that turns a one-paragraph goal into a complete, scored loop design. [L6]

**Loop Spec.** The one-page, nine-box design for a loop: goal, done when, trigger, actor, context, checker, state, limits, escalation. [L1]

**Maker, maker/checker.** The maker does the work; a separate checker decides whether it's done. The core design rule of loop engineering. [L2]

**MCP, connector.** A standard way to connect an agent to outside tools and data (the Model Context Protocol). ⚠VERIFY [L4]

**Meta-loop.** A loop that works on another loop, for example by proposing a better prompt and testing it on the golden set. [L6]

**Model judge.** A model call that grades work against a rubric (also called LLM-as-judge). Useful for tone and meaning; needs calibration. [L2]

**Orchestrator, workers.** A team shape where one agent splits a job and several workers do the pieces in separate workspaces. [L6]

**p.** In the calculators, the chance that one attempt (CALC-2) is right, or the share of attempts that are right before checking (CALC-1). [L2, L3]

**Paper trading.** Practicing trades with no real money, to test a process safely. [CS-3]

**Permission mode.** A Claude Code setting for how tool calls get approved (for example, asking every time, auto-approving edits, or auto mode). ⚠VERIFY [L4]

**Progress file.** `progress.md`: the loop's memory between runs (what's done, next, blocked, and decided). [L3]

**Prompt.** The words a loop hands its agent or its checker. [L0]

**Prompt engineering.** Choosing the words of one request. [L0]

**Prompt injection.** Instructions hidden in outside text (an issue, an email, a web page) that try to hijack an agent. [L4]

**Ralph loop (Ralph Wiggum loop).** A shell loop that feeds the same prompt file to a fresh agent until the work is done, credited to Geoffrey Huntley ("Ralph is a Bash loop"). [L4]

**Registry.** A table of every loop you run: name, version, owner, rung, ceiling, review date. [L6]

**Routine.** A saved Claude Code automation that runs in Anthropic's cloud on a schedule, from an API call, or on a GitHub event. ⚠VERIFY [L4]

**Run log.** One row per iteration, in fixed columns, recording what the loop did. [L5]

**Scheduled task, `/loop`.** Claude Code's way to re-run a prompt on an interval (fixed or self-paced) while a session is open. Recurring tasks expire after seven days. ⚠VERIFY [L4]

**Skill.** A packaged set of instructions (and sometimes scripts) that Claude can load, such as your verification steps. ⚠VERIFY [L4]

**Spot check.** Checking a random sample of a loop's passes by hand, to measure the false-pass rate. [L5]

**State.** What a loop writes down between turns and runs: a progress file, commits, a run log. [L3]

**Stop families.** The five ways a loop stops: DONE (the checker passes), CAP (a limit runs out), STUCK (no progress), DANGER (something risky), and HUMAN (a person says stop). [L3]

**Subagent.** A separate agent with its own context, started by another agent. Good as a fresh-context checker. [L4, L6]

**`/goal`.** A Claude Code command that keeps working toward a stated condition; a separate small model checks the condition after each turn. ⚠VERIFY [L4]

**Token.** A small chunk of text that models read and write; usage and cost are counted in tokens. [L4]

**Trigger.** What starts a run: you, a goal, a schedule, or an event. [L1]

**Trust (CALC-1).** The share of a checker's passes that are really right: p·S ÷ (p·S + (1 − p)·F). [L2]

**Worktree.** A second working folder attached to the same git repository, on its own branch, so parallel loops don't collide. [L3]

**⚠VERIFY.** A mark on any fact that changes fast (features, flags, prices, limits, and this field's history). Check it against current documentation before relying on it. [All]

⬅ [Quick Reference](10-quick-reference.md) · 🏠 [README](README.md) · [Sources](12-sources.md) ➡
