# Sources

⬅ [Glossary](11-glossary.md) · 🏠 [README](README.md) · [Council QA Report](13-council-qa-report.md) ➡

Where this guide's facts come from, and how firmly each one was checked. The build ran on September 24, 2026, in an environment that could reach some sites and not others. So sources fall into two groups: pages that were **opened and read**, and sources known only from **search-result summaries**. Everything in the second group stays marked ⚠VERIFY in the guide.

## Opened and read during the build (September 24, 2026)

| Source | Used for |
|---|---|
| Claude Code docs, "Keep Claude working toward a goal": https://code.claude.com/docs/en/goal | How `/goal` works: a separate small model checks the condition after each turn; it doesn't run commands or read files; condition-writing advice; adding a turn or time clause; stopping after several turns with no progress; "completion is decided by a fresh model rather than the one doing the work" (Levels 2–4, FAQ) |
| Claude Code docs, "Run prompts on a schedule": https://code.claude.com/docs/en/scheduled-tasks | `/loop` (fixed or self-paced intervals), the seven-day expiry of recurring tasks, and the comparison of cloud, desktop, and `/loop` scheduling (Levels 3–4, FAQ) |
| Claude Code docs, "Run Claude Code programmatically": https://code.claude.com/docs/en/headless | `claude -p`, exit codes, `--allowedTools`, permission modes, `--bare` and its API-key requirement, `--output-format json` with `total_cost_usd`, and hooks loading in untrusted folders without `--bare` (Level 4, FAQ) |
| Claude Code docs, "Automate actions with hooks": https://code.claude.com/docs/en/hooks-guide | Stop hooks that block with a reason, prompt-based hooks, the cap of eight blocks in a row without progress, and `PreToolUse` denies that hold even when permission checks are skipped (Levels 2–4) |
| Anthropic, "Loop Engineering: Getting Started with Loops" (June 30, 2026; Delba de Oliveira and Michael Segner): https://claude.com/blog/getting-started-with-loops | Loops as "agents repeating cycles of work until a stop condition is met"; four loop types (turn-based, goal-based, time-based, proactive); the advice to use a second, fresh-context reviewer (Levels 0–2, 6). Read through a summarizing fetch tool, so check exact wording on the page ⚠VERIFY |
| anthropics/claude-code, Ralph loop plugin README: https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum | `/ralph-loop` with `--max-iterations` (default unlimited) and `--completion-promise`; the credit to Geoffrey Huntley, "Ralph is a Bash loop" (Levels 3–4, FAQ) |

## Reported, not opened (⚠VERIFY before quoting)

These sources were found through search summaries only; the build environment couldn't open their pages. The guide paraphrases them, dates them loosely ("early June 2026"), and keeps the ⚠VERIFY mark.

| Source | What the summaries say |
|---|---|
| Addy Osmani, "Loop Engineering": https://addyosmani.com/blog/loop-engineering/ · follow-up "Practical Loop Engineering": https://addyosmani.com/blog/practical-loop-engineering/ | Named the practice in June 2026 and described its building blocks (scheduled or triggered runs, isolation, skills, connectors, subagents as verifiers, external state) and practical stop rules |
| Peter Steinberger, a post in early June 2026 | "You shouldn't be prompting coding agents anymore. You should be designing loops that prompt your agents." (wording as reported) |
| Boris Cherny (leads Claude Code at Anthropic), quoted in secondary sources | No longer prompts Claude by hand; loops he writes do it (paraphrased) |
| Lulla, Nersesyan, Mohsenimofidi, Treude, Baltes, "Loop Engineering: Building Blocks, Adoption, and Impact", arXiv 2608.21884 (August 2026): https://arxiv.org/abs/2608.21884 | Studies how far loop-engineering building blocks show up in open-source repositories; notes maker/checker separation as the most emphasized block |
| IBM, "What Is Loop Engineering?": https://www.ibm.com/think/topics/loop-engineering | Defines it as designing agentic workflows that iteratively guide agents toward user-defined goals with minimal human intervention |
| Sonar, "Loop engineering without verification is just automation": https://www.sonarsource.com/blog/loop-engineering-without-verification-is-just-automation/ | The title is quoted in Level 2 as a summary of the checker's importance |

## General knowledge (not tied to one source)

Feedback control and the spinning-ball (centrifugal) governor, thermostats, PID loops in industrial control, the reason-act-observe agent loop, git worktrees, and the known tendency of model judges to favor longer answers. These are long-established and are presented without numbers or quotes.

## What the guide does *not* rely on

No statistics, benchmark numbers, success stories, or real prices. Every case study is labeled ILLUSTRATIVE, and every price in the examples is an invented round number, labeled as invented.

⬅ [Glossary](11-glossary.md) · 🏠 [README](README.md) · [Council QA Report](13-council-qa-report.md) ➡
