# progress.md: {{LOOP_NAME}}

<!--
The loop's memory between runs. Each run reads this first and writes it last.
Keep entries short. A fresh agent should be able to pick up from this file alone.
Replace every {{PLACEHOLDER}}. Examples: {{STATUS}} = NOT YET · {{FINISHED_ITEM}} = "fix test_refund_rounding" · {{NEXT_ITEM}} = "fix test_tax_totals" ·
{{DECISION}} = "rounding is round-half-up" · {{PERSON}} = you · {{ATTEMPT}} = "rounded in refund()" · {{RESULT}} = "FAIL: same test" ·
{{LOOP_NAME}} = fix-tests · {{GOAL}} = copied from your Loop Spec · {{DATE}} = 2026-09-24 · {{N}} = 3 · {{LATER_ITEM}} = "fix test_discounts" ·
{{BLOCKED_ITEM}} = "test_currency" · {{WHY}} = "needs an exchange-rate decision" · {{WHO_OR_WHAT}} = you · {{WHAT}} = a few words · {{NONE_OR_WHAT}} = none.
Delete this comment block when you're done.
-->

**Status:** {{STATUS}} (NOT YET · STUCK · DONE, as decided by the checker)
**Goal:** {{GOAL}}
**Last updated:** {{DATE}}, iteration {{N}}

## Done
- [x] {{FINISHED_ITEM}}

## Next (the first unchecked item is the next run's job)
- [ ] {{NEXT_ITEM}}
- [ ] {{LATER_ITEM}}

## Blocked
- {{BLOCKED_ITEM}}: {{WHY}} (needs: {{WHO_OR_WHAT}})

## Decisions (follow these; only a person changes them)
- {{DATE}}: {{DECISION}} (decided by {{PERSON}})

## Attempts (last three, most recent last)
1. {{ATTEMPT}} → {{RESULT}}
2. {{ATTEMPT}} → {{RESULT}}
3. {{ATTEMPT}} → {{RESULT}}

## Log
## {{DATE}} · iteration {{N}} · did: {{WHAT}} · next: {{WHAT}} · blocked: {{NONE_OR_WHAT}}
