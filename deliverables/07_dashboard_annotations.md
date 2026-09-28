# Dashboard Annotations

The published dashboard carries three text annotations, one text box per sheet
(`deliverables/03_dashboard_export_all_sheets.pdf`, `screenshots/05_annotations/`). The
five annotations below, plus an optional sixth, are the longer drafts those
three boxes were condensed from; the heading under each one says where it ended
up. Each states a quantified finding, explains why it matters commercially, and
recommends a specific action. Every figure is reproducible from
`analysis/ground_truth.py`.

---

## Annotation 1 — Marketing Funnel sheet
### On the dashboard: the main text of the Marketing Funnel text box

> **Direct Mail converts 54× better than Organic Search but receives 6.7% of the
> leads.** Direct Mail turns 49.0% of its 149 leads into Closed Won, against
> 0.9% of Organic Search's 671 leads. Organic Search and Email together consume
> $2.03M of spend and produce 14 closed-won leads between them.
>
> **Why it matters:** more than half the lead volume is flowing through the two
> channels that almost never convert, which inflates lead counts while starving
> the pipeline of qualified demand.
>
> **Recommended action:** move the Organic Search and Email budget into Direct
> Mail and Partner Referral for one quarter, and re-measure closed-won rate by
> channel. Treat Organic Search as a brand channel, not a demand channel, and
> stop reporting its lead count as pipeline.

---

## Annotation 2 — Marketing Funnel sheet
### On the dashboard: only its spend-allocation caveat, as the CAVEAT line of the Marketing Funnel text box

> **All six campaigns are underwater, and NovaEdge Awareness is the worst at
> −97.7% return.** It spends $1.52M to attribute $34K of revenue, with a 6.2%
> response rate — the lowest of any campaign. NovaPulse Launch is the strongest
> performer and still returns −83.7%.
>
> **Why it matters:** the gap is too large to be a pricing or timing problem.
> Attributed revenue across all campaigns totals $1.13M against $12.36M of
> recorded spend, which means the spend figure is being allocated per lead
> touchpoint rather than per campaign.
>
> **Recommended action:** pause NovaEdge Awareness and audit how `campaign_spend`
> is allocated before making budget decisions from this chart. Until the
> allocation is confirmed, use these numbers to rank campaigns against each
> other, not to state an absolute return.

---

## Annotation 3 — Sales Pipeline sheet
### On the dashboard: combined with Annotation 4 in the Sales Pipeline text box

> **Central closes 69.9% of its deals; East closes 57.8%.** Central won 144 of
> 206 deals and booked $274,285. East won 74 of 128 and booked $184,673. The
> 12.1-point spread is the widest performance gap in the pipeline.
>
> **Why it matters:** on East's 128 deals, closing at Central's rate would have
> won roughly 15 more deals — about $38,600 of additional booked revenue at
> East's average won-deal size of $2,496, with no extra lead spend.
>
> **Recommended action:** have Central's managers walk the East team through
> their qualification and discovery process this quarter, then re-check the gap
> after 90 days.

---

## Annotation 4 — Sales Pipeline sheet
### On the dashboard: combined with Annotation 3 in the Sales Pipeline text box

> **Nearly half of all losses are self-inflicted: 46.7% are "No Decision Made"
> (43) or "Poor Product Fit" (43), out of 184 lost deals.** Competitor Won
> accounts for only 34 losses (18.5%).
>
> **Why it matters:** NovaTech is losing more deals to stalled decisions and
> mis-qualified prospects than to competitors. Both are controllable earlier in
> the cycle; competitive losses usually are not.
>
> **Recommended action:** add a qualification gate before a deal reaches
> proposal, requiring a named economic buyer and a confirmed use-case fit.
> Target reducing the combined No-Decision and Poor-Fit share from 46.7% to
> below 35%.

---

## Annotation 5 — Customer Health sheet
### On the dashboard: the Customer Health text box

> **Our single largest customer is also our heaviest support burden.**
> YieldMax Software (ACCT-041) is the top revenue account at $40,722 and files
> 334 tickets — 11.1% of every ticket NovaTech receives, nearly twice the next
> account. Across all 85 accounts, revenue and ticket volume are positively
> correlated at 0.57, and 4 of the top 10 revenue accounts are also in the top
> 10 by ticket volume.
>
> **Why it matters:** support load rises with account value, so the accounts
> that cost the most to keep happy are the ones NovaTech can least afford to
> lose. Three accounts — Falcon Software, HavenCrest Communications and
> NorthStar Finance — combine above-median revenue, above-median ticket volume
> and negative sentiment on 31–55% of their tickets, putting $42,040 (5.9% of
> booked revenue) at elevated risk.
>
> **Recommended action:** assign named technical account managers to those three
> accounts plus YieldMax, and review them monthly. Treat any account crossing
> 30% negative sentiment as a renewal risk regardless of its current spend.

---

## Optional sixth annotation — Customer Health sheet
### Not placed on the dashboard

> **Priority is not changing how fast tickets get resolved.** Critical tickets
> average 56.6 hours to resolve; low-priority tickets average 59.4 hours. The
> entire benefit of being marked critical is 2.8 hours, and 50 critical tickets
> is only 1.7% of volume.
>
> **Why it matters:** the priority field is being recorded but not acted on. A
> customer reporting a critical outage waits essentially as long as one
> reporting a cosmetic bug, which is the fastest way to turn a high-value
> account into a negative-sentiment account.
>
> **Recommended action:** set an explicit target — critical tickets resolved
> within 8 hours — and route them to a dedicated on-call queue rather than the
> shared backlog. This is the single highest-leverage fix on this sheet.

---

## Note on placement

Each sheet has one text box, at the bottom left below the visuals (PDF pages 1
to 3, `screenshots/05_annotations/`). Each box is headed in capitals and follows the same
FINDING, WHY IT MATTERS, ACTION structure as the drafts above; the Marketing
Funnel box adds a CAVEAT line.
