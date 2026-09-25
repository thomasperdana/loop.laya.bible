# Calculator Toolkit

⬅ [FAQ](08-faq.md) · 🏠 [README](README.md) · [Quick Reference](10-quick-reference.md) ➡

All four blank worksheets and spreadsheet formulas in one place. The lessons, worked examples, and assumptions live in the levels (linked below); the [workbook](workbook/loop-engineering-workbook.xlsx) has every calculator with live formulas and a checksum table, plus a CSV per sheet in [`workbook/csv/`](workbook/csv/).

Spreadsheet formulas work in both Google Sheets and Excel. Prices are always **FIELD WORK**: take them from Anthropic's current pricing page ⚠VERIFY, never from memory.

---

## 🧮 CALC-1 · Verifier Trust ([Level 2](02-level-2-apprentice.md))

*When the checker says "pass", how often is the work really right?*

```text
CALC-1 · VERIFIER TRUST
p  (share correct before any check)   = ______
S  (checker passes correct work)      = ______
F  (checker passes wrong work)        = ______
p × S                                 = ______
(1 − p) × F                           = ______
Trust = p×S ÷ (p×S + (1 − p)×F)       = ______   → band: ______
Bands: 95%+ unattended with spot checks · 80–94% a human checks a sample · under 80% don't run unattended
```

With p in B2, S in B3, and F in B4:
```text
Trust:  =B2*B3/(B2*B3+(1-B2)*B4)
```

---

## 🧮 CALC-2 · Tries-to-Success ([Level 3](03-level-3-engineer.md))

*How many tries should the cap allow?*

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
Bands: 5 or fewer comfortable · 6–15 add a budget ceiling (CALC-3) · over 15 better checker or smaller steps
```

With p in B2, C in B3, and a cap n in B4:
```text
Tries needed:               =ROUNDUP(LN(1-B3)/LN(1-B2)-1E-9,0)
Chance of success within n: =1-(1-B2)^B4
Average tries:              =1/B2
Average tries with cap n:   =(1-(1-B2)^B4)/B2
```

---

## 🧮 CALC-3 · Loop Budget ([Level 4](04-level-4-author.md))

*What can one run, and a month of runs, cost in money and time?*

```text
CALC-3 · LOOP BUDGET                     (prices from the CURRENT pricing page)
Tin  (input tokens per iteration)     = ______
Tout (output tokens per iteration)    = ______
Pin  ($ per million input tokens)     = ______   ⚠VERIFY
Pout ($ per million output tokens)    = ______   ⚠VERIFY
Cost per iteration = (Tin×Pin + Tout×Pout) ÷ 1,000,000   = $______
p (from CALC-2) = ____   Typical run ≈ (1 ÷ p) × cost     = $______
N (cap, from CALC-2) = ____   Ceiling per run = N × cost  = $______
R (runs per month) = ____   Monthly ceiling = R × ceiling = $______
M (minutes per iteration) = ____   Time ceiling = N × M   = ______ min
```

With Tin in B2, Tout in B3, Pin in B4, Pout in B5, p in B6, N in B7, M in B8, R in B9, cost per iteration in B10, and ceiling per run in B12:
```text
Cost per iteration:  =(B2*B4+B3*B5)/1000000
Typical run:         =(1/B6)*B10
Ceiling per run:     =B7*B10
Monthly ceiling:     =B9*B12
Time ceiling (min):  =B7*B8
```

---

## 🧮 CALC-4 · Loop Scorecard /100 ([Level 5](05-level-5-expert.md))

*How ready is this loop to run without you, and which fixes are worth the most?*

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
Bands: 0–59 draft · 60–74 working · 75–89 strong · 90–100 hero-grade
```

With the eight ratings in B2:B9, and the score in B10:
```text
Score: =3*SUM(B2:B5)+2*SUM(B6:B9)
Band:  =IF(B10>=90,"hero-grade",IF(B10>=75,"strong",IF(B10>=60,"working","draft")))
```

---

## Checksums: fill these in to test your own spreadsheet

If your copy gives these results, your formulas are right.

| Calculator | Inputs | Result |
|---|---|---|
| CALC-1 | p 0.30 · S 0.90 · F 0.20 | 0.659 |
| CALC-1 | p 0.30 · S 0.90 · F 0.02 | 0.951 |
| CALC-1 | p 0.50 · S 0.90 · F 0.20 | 0.818 |
| CALC-2 | p 0.5 · C 0.95 | 5 tries · 0.969 |
| CALC-2 | p 0.2 · C 0.90 | 11 tries · 0.914 |
| CALC-3 | Tin 20,000 · Tout 2,000 · $4 / $20 (invented) · p 0.5 · N 5 · M 3 · R 30 | $0.12 · $0.24 · $0.60 · $18.00 · 15 min |
| CALC-4 | 2, 1, 0, 1, 1, 1, 1, 1 | 20 (draft) |
| CALC-4 | 5, 5, 5, 4, 4, 4, 4, 4 | 89 (strong) |

⬅ [FAQ](08-faq.md) · 🏠 [README](README.md) · [Quick Reference](10-quick-reference.md) ➡
