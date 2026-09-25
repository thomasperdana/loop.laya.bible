# Starter kit

Six files that turn the guide into a working loop. Copy the whole `kit/` folder into a scratch folder, or into a branch of the project you want to loop on. Never run it on your main branch.

| File | What it is | Use it in | Autonomy rung |
|---|---|---|---|
| [`LOOP-SPEC.md`](LOOP-SPEC.md) | The nine-box Loop Spec: a blank template, then a filled example (CS-1) | Level 1 onward | Any: it's a design |
| [`PROMPT.md`](PROMPT.md) | The per-run loop prompt, in five sections | Level 4 | Suggest (2) or higher |
| [`progress.md`](progress.md) | The state file each run reads first and writes last | Level 3 | Any |
| [`loop.sh`](loop.sh) | A minimal loop runner: dry run by default, hard caps, a stop file, protected files, and a CSV log | Level 4 | Watch (dry run) up to act with approval (3) |
| [`loop-generator.prompt.md`](loop-generator.prompt.md) | The Loop Generator: a one-paragraph goal in, a scored loop design out | Level 6 | Design only: it never runs anything |
| `README.md` | This file | — | — |

## The order to use them in

1. **Design:** copy `LOOP-SPEC.md` and fill in the nine boxes, starting from DONE WHEN. Or let `loop-generator.prompt.md` draft it for you, then review it.
2. **Write the prompt:** copy `PROMPT.md` and fill it from your spec.
3. **Start the state file:** copy `progress.md` into the folder the loop works in.
4. **Dry run:** run `loop.sh` with its defaults and watch every exit (below). No API, no account, no cost.
5. **Real run, on a branch:** set `DRY_RUN=0`, `AGENT_CMD`, `CHECK_CMD`, and `PROTECT`, with small caps.
6. **Read the log:** paste `loop-log.csv` into the workbook's Run Log sheet ([`../workbook/`](../workbook/)).

## Dry-run demos (safe, free)

Run these in a scratch copy of this folder:
```bash
chmod +x loop.sh
MOCK_PASS_AT=3 ./loop.sh     # DONE on iteration 3 → exit 0
MOCK_PASS_AT=99 ./loop.sh    # never passes → CAP after 5 iterations → exit 2
MOCK_STUCK=1 ./loop.sh       # the same failure 3 times → STUCK → exit 3
touch .loop-stop; ./loop.sh  # stop file → HUMAN → exit 4   (then: rm .loop-stop)
echo 'exit 0' > fake-check.sh; MOCK_TAMPER=1 PROTECT=fake-check.sh ./loop.sh   # DANGER → exit 5
```
Exit codes: **0** DONE · **1** script error · **2** CAP · **3** STUCK · **4** HUMAN · **5** DANGER.

## Before a real run: the safety checklist

- [ ] The loop works in its own branch or worktree, never on main.
- [ ] `MAX_ITERS` comes from CALC-2, and you know the ceiling per run from CALC-3.
- [ ] `PROTECT` lists the tests and the check script, so the agent can't game them.
- [ ] `AGENT_CMD` allows only the tools the loop needs (for example `--allowedTools "Read,Edit,Bash(npm test *)"`, ⚠VERIFY the flag names).
- [ ] No permission-skipping flags, unless this runs inside a disposable container or VM with no secrets.
- [ ] Secrets live in environment variables, never in `PROMPT.md` or `progress.md`.
- [ ] You know how to stop it: `touch .loop-stop` in the loop's folder, or Ctrl+C.
- [ ] The loop touches no money, health, legal, or production systems above rung 3.

## Where each file is taught

Loop Spec: [Level 1](../01-level-1-starter.md) · state and stop rules: [Level 3](../03-level-3-engineer.md) · `PROMPT.md` and `loop.sh`: [Level 4](../04-level-4-author.md) · the run log: [Level 5](../05-level-5-expert.md) · the Loop Generator: [Level 6](../06-level-6-hero.md).
