# Revenue Intelligence Dashboard — Report for VP Sarah Chen

**From:** Marco Anthony Ayuste, Business Intelligence Analyst
**Date:** 13 September 2026
**Re:** Unifying CRM, marketing and support data into one dashboard

---

## Summary

You asked for one place the revenue team can go instead of three, covering
Marketing Funnel, Sales Pipeline and Customer Health, with the ability to ask
questions in plain English. That dashboard is built and published. It covers 499
deals, 2,240 marketing leads and 3,000 support tickets, connected through the
account ID that appears in all three systems.

Two things deserve your attention before the team starts using it. **The
marketing numbers and the CRM numbers disagree, and CRM is the one to trust.**
And **support priority is not changing how fast tickets get resolved**, which is
the clearest fixable problem in the data.

## How the data was put together

**The join.** I anchored the combined dataset on CRM deals and attached
marketing and support using a *left join* — a rule that keeps every deal even
when an account has no marketing activity or no tickets. The alternative would
have silently discarded 354 rows belonging to 15 accounts (ACCT-101 to ACCT-115)
that exist downstream but were never created in the CRM.

**Row multiplication.** Attaching tables that hold many rows per account makes
each deal repeat. Our 499 deals become 63,420 rows — a 127-fold expansion. This
is expected, not an error, but it means a naive total on the combined table
would overstate revenue roughly 127 times. Every revenue and ticket total on the
dashboard therefore comes from the single-source datasets; the combined dataset
is used only where a genuine cross-system comparison is needed, such as weighing
an account's revenue against its support load.

**Data quality.** I ran 20 checks against the supplied data dictionary before
building anything. Fifteen passed. Four of the five failures changed how the
dashboard had to be built:

- **Ticket IDs are not unique.** Four IDs are used twice by different accounts,
  so tickets are counted by row, not by unique ID.
- **59 tickets have no recorded sentiment**, though the dictionary says the field
  is never blank. They are labelled "Unresolved" rather than dropped, so the
  sentiment chart still accounts for all 3,000 tickets.
- **Marketing overstates results.** It reports 412 closed-won leads and
  $1,127,223 of revenue against 315 won deals and $707,201 actually booked.
  Marketing counts a lead per touchpoint while CRM counts a deal, so the same
  sale is counted more than once.
- **Marketing spend looks misallocated.** Recorded campaign spend totals $12.36M
  against $707,201 of booked revenue — a gap too large to be a performance
  problem, indicating spend is attributed per touchpoint rather than per campaign.

The rule this produced, and which is stated on the dashboard itself: booked CRM
revenue is the single source of truth for any revenue figure. Marketing's
attributed revenue is used only to rank campaigns against each other.

## How the dashboard is laid out

Each sheet answers your questions in the order a reader asks them: how many, then
how good, then what to do.

**Marketing Funnel** leads with leads, response rate, spend and attributed
revenue, then breaks lead volume down by channel and shows what share of each
channel's leads actually close. Volume and conversion sit side by side
deliberately — the channel with the most leads is not the channel that converts.

**Sales Pipeline** leads with booked revenue, win rate and sales-cycle length,
then breaks revenue down by product, win rate by region, and shows why deals are
lost.

**Customer Health** is the view nobody had. It shows ticket volume by product
area, resolution time by priority, the sentiment mix, and — using the combined
dataset — which accounts pair high revenue with heavy support load.

Filter controls for region, deal stage, industry, company size, channel and
segment sit at the top of each sheet. Clicking a bar filters the other visuals
around it, and a navigation link moves between sheets so an account spotted on
one view can be followed to another.

## What the data says, and what I recommend

**1. Over half the marketing budget flows through channels that do not convert.**
Direct Mail converts 49.0% of its leads to closed won; Organic Search converts
0.9%. Yet Direct Mail receives 149 leads (6.7% of the total) against Organic
Search's 671. Organic Search and Email together consume $2.03M of recorded spend
and produce 14 closed-won leads.
*Recommendation:* shift that budget into Direct Mail and Partner Referral for one
quarter and re-measure. Treat Organic Search as a brand channel, not a demand
channel.

**2. Support priority is not being acted on.** Critical tickets resolve in 56.6
hours; low-priority tickets take 59.4. Being marked critical buys a customer 2.8
hours. Only 50 tickets (1.7%) are critical, so prioritising them properly costs
very little capacity.
*Recommendation:* set an 8-hour target for critical tickets and route them to a
dedicated queue. This is the highest-leverage change available and needs no new
headcount.

**3. Our biggest customer is our biggest support burden.** YieldMax Software is
the highest-revenue account at $40,722 and files 334 tickets — 11.1% of every
ticket we receive. This is not an outlier: across all 85 accounts, revenue and
ticket volume move together, and 4 of the top 10 revenue accounts are also top
10 by ticket volume. Falcon Software, HavenCrest Communications and NorthStar
Finance combine above-average revenue, above-average ticket volume and negative
sentiment on 31–55% of their tickets — $42,040, or 5.9% of booked revenue.
*Recommendation:* assign named technical account managers to those three plus
YieldMax and review monthly. Treat any account passing 30% negative sentiment as
a renewal risk.

**4. Nearly half of lost deals were losable.** "No Decision Made" (43) and "Poor
Product Fit" (43) account for 46.7% of our 184 losses; losing to a competitor
accounts for 18.5%. We lose more to stalled decisions and poor qualification than
to rivals, and both are controllable earlier.
*Recommendation:* add a qualification gate before proposal requiring a named
budget holder and a confirmed use-case fit.

**5. A 12-point regional win-rate gap.** Central closes 69.9% of its deals; East
closes 57.8%. On East's existing 128 deals, closing at Central's rate would have
won about 15 more — roughly $38,600 of additional booked revenue with no extra
lead spend.
*Recommendation:* have Central's managers walk East through their qualification
process, then re-check in 90 days.

## Where the AI agreed with the dashboard, and where it did not

Quick Chat is the plain-English layer. I asked it questions whose answers I had
already calculated independently from the raw files, so agreement would be a real
check rather than a reassurance.

**It agreed on every headline metric:** booked revenue, win rate, closed-won rate
by channel, loss-reason counts, resolution times, and the account-level
comparison of tickets against revenue. It also volunteered useful
interpretation — it flagged the flat resolution times as a prioritisation problem
without being asked.

**Configuring a Topic changed how it answers, not whether it is right.** A
*Topic* is a description of the data in business language — what "revenue" means
here, which fields to ignore, which counting rules apply. After building one, the
revenue question dropped from five reasoning steps to one, Quick Chat began
replying in our own vocabulary ("booked revenue"), and it started declaring its
assumptions, stating that it excludes unresolved tickets rather than doing so
silently. On the hardest question — the one spanning the combined data where a
naive total would be overstated 127 times — it returned $154.7K for the top ten
accounts against an independently computed $154,709.

**It was not uniformly reliable.** Twice the metric I asked for was exact while a
figure printed beside it was wrong: an unrequested lead-count column was wrong
for four of five channels, and a ticket count reconciled to neither the resolved
nor the total figures. Separately, the auto-generated summary of the Sales
Pipeline sheet cited the three *smallest* loss reasons as the "top" ones,
omitting the two tied at the top. Each number it quoted was individually correct,
so nothing looked wrong until the full ranking was checked.

**How the team should use it.** Use the dashboard whenever a number leaves the
building — a board deck, a customer conversation, a target — because its
definitions are fixed and reviewable. Use Quick Chat to explore, and to decide
what deserves a chart. The working rule: **trust the number you asked for; verify
any number that arrives alongside it.** When the two disagree, assume a
definition difference before assuming an error — the one real discrepancy found
in this project turned out to be exactly that, a question of whether resolution
time is counted in whole days or exact hours.
