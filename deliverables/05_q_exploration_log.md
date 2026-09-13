# NovaTech Q Exploration Log

**Student Name:** Marco Anthony Ayuste
**Date:** 13 September 2026
**Environment:** Amazon Quick Suite — Quick Chat scoped to the **NovaTech Revenue
Intelligence** Topic (Version 2, Active) over four SPICE datasets.

Every answer below was cross-checked against the published dashboard **and**
against `analysis/ground_truth.py`, which computes the same figures directly
from the raw CSVs. That means an agreement is a real verification, not two
copies of the same mistake.

---

## Part 1 — Before / after Topic configuration

The same three questions were asked twice: first scoped to the published
dashboard (baseline), then scoped to the configured Topic.

| # | Question | Baseline (dashboard-scoped) | After Topic | Change |
|---|---|---|---|---|
| B1 | What is the total revenue from closed-won deals? | "$707,201 across 315 won deals." Correct, but took **5 reasoning steps** — it first hit the Total Deal Value KPI (all deals) and had to work out that it needed to filter to Won. | "The total **booked revenue** from closed-won deals is **$707,201**." **1 step.** | ✅ Same correct answer, 5 steps → 1 step, and it adopted the glossary term *booked revenue* |
| B2 | Which marketing channel has the highest closed-won rate? | Direct Mail 48.99%, Partner Referral 31.10%, Paid Social 22.77%, Email 2.78%, Organic Search 0.89%. Correct. **2 steps.** | Same five rates, correct, **1 step** — but it added a "Lead Count" column that was **wrong for four of five channels** | ⚠️ Faster and still correct on the rate; introduced a wrong supporting column |
| B3 | Average resolution time, critical vs low priority? | Critical 56.59 h, Low 59.41 h, difference 2.82 h, plus the full four-level breakdown. Correct. | Critical 56.61 h, Low 59.50 h, difference ~2.9 h, and it stated "**Unresolved tickets were excluded from these calculations**" — following the Topic instruction | ✅ Correct to within 0.1 h and now explicitly states its exclusion rule |

**What the Topic actually bought us.** The headline finding is *not* that
answers went from wrong to right — the baseline was already accurate, because
the dashboard was carefully modelled. What changed is **how the answer is
reached and how it is expressed**: the revenue question dropped from five
reasoning steps to one, Q began using NovaTech's own vocabulary ("booked
revenue"), and it started declaring its assumptions (excluding unresolved
tickets) instead of applying them silently. On a shared dashboard, a stated
assumption is worth as much as a correct number.

**What it did not fix.** Topic configuration did not make every number in a
response trustworthy — see B2 and entry 3 below.

---

## Part 2 — Exploration questions

| # | Question Asked | Q's Answer (summarised) | Dashboard Visual Used to Cross-Check | Dashboard / Ground Truth Shows | Match? | Notes |
|---|---|---|---|---|---|---|
| 1 | What is the total revenue from closed-won deals? *(Sales)* | Booked revenue **$707,201** | Sales Pipeline — Total Deal Value KPI | $707,201 across 315 Won deals | ✅ Exact | The anchor figure for every other revenue number. |
| 2 | Which marketing channel has the highest closed-won rate? *(Marketing)* | **Direct Mail 48.99%**, Partner Referral 31.10%, Paid Social 22.77%, Email 2.78%, Organic Search 0.89% | Marketing Funnel — Closed-Won Rate by Marketing Channel | 49.0% / 31.1% / 22.8% / 2.8% / 0.9% | ✅ Exact on rates / ❌ on lead counts | **Partially wrong.** The rates are exact, but the "Lead Count" column read 149 / 164 / 202 / 144 / 341 when the true counts are 149 / 807 / 325 / 288 / 671. Only Direct Mail was right, and the five wrong values sum to exactly 1,000 — the signature of a truncated result set. |
| 3 | How many leads did each marketing channel generate in total? *(Marketing)* | **2,240 total.** Partner Referral largest (~36%), Organic Search 671 (~30%), Email 288, Direct Mail 149 | Marketing Funnel — Lead Count by Campaign Channel | 807 / 671 / 325 / 288 / 149, total 2,240 | ✅ Exact | Asked as the *primary* question, the same metric came back correct. So entry 2's error was a one-off artefact of a secondary column, not a systematic failure — but it proves supporting columns need checking too. |
| 4 | Average resolution time for critical vs low priority tickets? *(Support)* | Critical **56.61 h** (49 tickets), Low **59.50 h** (1,479 tickets), gap ~2.9 h. Noted the small critical sample and that unresolved tickets were excluded | Customer Health — Average Resolution Time by Priority | Critical 56.60 h (48 resolved of 50), Low 59.42 h (1,465 resolved of 1,500) | ⚠️ Partial | Averages agree to within 0.1 h. The **ticket counts do not reconcile** to either the resolved counts (48 / 1,465) or the totals (50 / 1,500). Same pattern as entry 2: reliable headline metric, unreliable supporting count. |
| 5 | What are the primary loss reasons, and how many deals each? *(Sales)* | Across **184 lost deals**: Poor Product Fit **43** and No Decision Made **43** tied (~47% combined), Competitor Won **34**, Budget Constraints **31** (least common) | Sales Pipeline — Deal Count by Loss Reason | 43 / 43 / 34 / 33 / 31 across 184 losses; combined 46.7% | ✅ Exact | Q added the useful observation that budget is the *least* common reason, so "pricing is the problem" is not supported by the data. |
| 6 | **Cross-dataset:** Which accounts file the most support tickets, and what is the booked revenue for those same accounts? | **ACCT-041** an outlier at **334 tickets** (~2× the next) and also the top revenue account at **$40,722**. Top 10 high-ticket accounts booked **~$154.7K ≈ 22%** of the $707K total. Flagged that ACCT-036 files 140 tickets for only $7,950 while ACCT-072 books $13,789 on 90 tickets | Customer Health — Ticket Volume and Deal Value by Account (unified dataset) | ACCT-041 334 / $40,722; ACCT-036 140 / $7,950; ACCT-072 90 / $13,789; top 10 total **$154,709 = 21.9%** | ✅ Exact | **The most important check in this log.** The unified dataset fans out 499 deals into 63,420 rows, so a naive revenue sum here would be inflated ~127×. Q returned correct per-account revenue, which means the fan-out rule written into the Topic was actually applied. |

**Coverage:** 6 entries — Marketing (2), Sales (2), Support (1), cross-dataset
(1) — spanning all three domains, above the 5-entry minimum.

---

## Reflection

**Where did Q agree with the dashboard?**
On every headline metric. Total booked revenue, win rate, closed-won rate by
channel, loss-reason counts, resolution time by priority, and the account-level
ticket-versus-revenue comparison all matched the dashboard and my independent
calculation exactly — in the cross-dataset case down to $154,709 against Q's
"~$154.7K". Q was also willing to volunteer interpretation without being asked:
it flagged the flat resolution times as a prioritisation problem, and noted that
budget is the least common loss reason.

**Where did Q disagree or struggle?**
Twice, and both times in the same way: **the metric I asked for was right, while
a supporting count printed beside it was wrong.** In entry 2 the closed-won
rates were exact but the lead counts were wrong for four of five channels (and
summed to exactly 1,000, indicating a truncated result set). In entry 4 the
resolution averages were right to a tenth of an hour but the ticket counts
reconciled to neither the resolved nor the total ticket counts. Notably, when
the same lead-count metric was asked as the *main* question (entry 3), it came
back correct — so this is not a broken metric, it is a weaker guarantee on
numbers the model adds for context.

Before the Topic existed, Q's difficulty was different and more visible: it took
five steps to answer the revenue question because the dashboard's headline KPI
covers all deals rather than won deals, and it had to reason its way to the
right filter.

**When would I use Q rather than the dashboard?**
Use the **dashboard** whenever the number leaves the building — a board deck, a
customer conversation, a target. Its definitions are fixed, visible and
reviewable. Use **Q** to explore: to ask the question nobody built a chart for,
to test a hunch in fifteen seconds, and to decide what deserves a chart. Q is
strongest at "what is X" and at cross-system questions that would otherwise need
a manual join.

The operating rule I would give the revenue team is simple: **trust the number
you asked for; verify any number that arrives alongside it.** Both of Q's misses
were in columns nobody requested. And when Q and the dashboard disagree, assume
a definition difference before assuming an error — the one discrepancy found
during initial verification (resolution time in whole calendar days versus exact
elapsed hours) turned out to be exactly that, and it disappeared once the
dashboard and Topic made the definition explicit.
