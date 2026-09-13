# Revenue Intelligence Dashboard — Report for VP Sarah Chen

**From:** Marco Anthony Ayuste, Business Intelligence Analyst
**Date:** 13 September 2026
**Re:** Unifying CRM, marketing and support data into one dashboard

---

## What you asked for, and what you now have

You asked for one place the revenue team can go instead of three, with three
views — Marketing Funnel, Sales Pipeline and Customer Health — and the ability
to ask questions in plain English. That dashboard is built and published.

It covers 499 deals, 2,240 marketing leads and 3,000 support tickets, all
connected through the account ID that exists in all three systems. The Monday
morning copy-paste exercise is replaced by filters the team can set themselves.

Two things are worth your attention before the team starts using it. First,
**the marketing numbers and the CRM numbers do not agree**, and CRM is the one
to trust. Second, **support priority is not changing how fast tickets get
resolved** — which is the clearest fixable problem in the data.

---

## How the data was put together

**The three sources.** CRM deals are the record of what NovaTech actually sold.
Marketing campaigns record every lead touchpoint and what was spent reaching
them. Support tickets record every customer issue. Each row in all three carries
an account ID, which is what makes a unified view possible.

**The join.** I anchored the unified dataset on CRM deals and attached marketing
and support to it with what is called a *left join* — a rule that keeps every
deal even when an account has no marketing activity or no tickets. The
alternative, an inner join, would have silently discarded 354 marketing and
support rows belonging to 15 accounts (ACCT-101 to ACCT-115) that exist
downstream but were never created in the CRM.

**Row multiplication, and why it matters.** When you attach a table that has
many rows per account, each deal repeats once for every matching row. NovaTech's
499 deals become 63,420 rows in the unified table — a 127-fold expansion. This
is expected and is not an error, but it means a naive total on the joined table
would overstate revenue by roughly 127 times. To prevent that, the dashboard
takes every revenue and ticket total from the single-source datasets, and uses
the unified dataset only where a genuine cross-system comparison is needed, such
as comparing an account's revenue against its ticket volume.

**Data quality.** I ran 20 checks against the supplied data dictionary before
building anything. Fifteen passed. Five did not, and four of those changed how
the dashboard had to be built:

- **Ticket IDs are not unique.** Four IDs are used twice by two different
  accounts. Tickets are therefore counted by row, not by unique ID — counting by
  ID would under-report by four.
- **59 tickets have no recorded sentiment**, although the dictionary says the
  field is never blank. Rather than drop them, they are labelled "Unresolved" so
  the sentiment chart still accounts for all 3,000 tickets.
- **Marketing over-states results.** Marketing reports 412 closed-won leads and
  $1,127,223 of revenue. CRM records 315 won deals and $707,201 actually booked.
  Marketing counts a lead per touchpoint while CRM counts a deal, so the same
  sale can be counted more than once on the marketing side.
- **Marketing spend looks misallocated.** Recorded campaign spend totals
  $12.36M against $707,201 of booked revenue. That gap is too large to be a
  performance problem; it indicates spend is being attributed per lead
  touchpoint rather than per campaign.

**The practical rule this produced:** booked CRM revenue is the single source of
truth for any revenue figure. Marketing's attributed revenue is used only to
rank campaigns against each other, never to state an absolute return. This is
stated on the dashboard itself so nobody re-derives the wrong number later.

---

## How the dashboard is laid out, and why

Each sheet answers the questions you listed in your brief, in the order a reader
naturally asks them: how many, then how good, then what to do.

**Marketing Funnel** leads with four summary cards — leads, response rate,
spend, attributed revenue — then breaks lead volume down by channel, shows what
share of each channel's leads actually close, and charts spend against
attributed revenue per campaign. Volume and conversion sit side by side
deliberately: the channel with the most leads is not the channel that converts.

**Sales Pipeline** leads with total booked revenue, win rate, average deal value
and average days to close, then breaks revenue down by product and win rate by
region, and shows why deals are lost. Average deal value is calculated on won
deals only; including lost deals at zero would halve the figure and mislead.

**Customer Health** is the view nobody had before. It shows ticket volume by
product area, how long tickets take to resolve by priority level, the sentiment
mix, and — using the unified dataset — which accounts combine high revenue with
high support load.

**Interactivity.** Filter controls for region, deal stage, industry, company
size, channel and segment sit at the top of the sheets. Clicking a bar filters
the other visuals on that sheet, so selecting a channel or a product immediately
narrows everything around it, and a navigation link moves between sheets so an
account spotted on one view can be followed to another.

A note on one number: resolution time is reported in **exact elapsed hours**.
Quick Chat measures the same thing in whole calendar days, which is why it will
quote a lower figure. Both are correct; they are different clocks, and the
dashboard labels which one it uses.

---

## What the data says, and what I recommend

### 1. Over half the marketing budget flows through channels that do not convert

Direct Mail converts 49.0% of its leads to closed won. Organic Search converts
0.9%. Yet Direct Mail receives 149 leads (6.7% of the total) while Organic
Search receives 671. Organic Search and Email together consume $2.03M of
recorded spend and produce 14 closed-won leads between them.

**Recommendation:** shift Organic Search and Email budget into Direct Mail and
Partner Referral for one quarter and re-measure. Treat Organic Search as a brand
channel, not a demand channel, and stop counting its leads as pipeline.

### 2. Support priority is not being acted on

Critical tickets are resolved in 56.6 hours on average. Low-priority tickets
take 59.4 hours. Being marked critical buys a customer 2.8 hours. Only 50
tickets (1.7%) are critical, so prioritising them properly would cost very
little capacity.

**Recommendation:** set an explicit target of 8 hours for critical tickets and
route them to a dedicated queue rather than the shared backlog. This is the
single highest-leverage change available and it requires no new headcount.

### 3. Our biggest customer is also our biggest support burden

YieldMax Software is the highest-revenue account at $40,722 and files 334
tickets — 11.1% of every ticket NovaTech receives, nearly double the next
account. This is not an outlier: across all 85 accounts, revenue and ticket
volume move together (a correlation of 0.57), and 4 of the top 10 revenue
accounts are also top 10 by ticket volume.

Three accounts — Falcon Software, HavenCrest Communications and NorthStar
Finance — combine above-average revenue, above-average ticket volume and
negative sentiment on 31% to 55% of their tickets. Together they represent
$42,040, or 5.9% of booked revenue.

**Recommendation:** assign named technical account managers to those three plus
YieldMax and review them monthly. Treat any account passing 30% negative
sentiment as a renewal risk regardless of current spend.

### 4. Nearly half of lost deals were losable

"No Decision Made" (43 deals) and "Poor Product Fit" (43 deals) account for
46.7% of the 184 losses. Losing to a competitor accounts for only 18.5%. We are
losing more deals to stalled decisions and poor qualification than to rivals,
and both are controllable earlier in the cycle.

**Recommendation:** add a qualification gate before proposal stage requiring a
named budget holder and a confirmed use-case fit. Target bringing the combined
no-decision and poor-fit share below 35%.

### 5. A 12-point regional win-rate gap

Central closes 69.9% of its deals; East closes 57.8%. On East's existing 128
deals, closing at Central's rate would have won about 15 more deals — roughly
$38,600 of additional booked revenue with no additional lead spend.

**Recommendation:** have Central's managers walk East through their
qualification and discovery process, then re-check the gap in 90 days.

---

## Where the AI agreed with the dashboard, and where it did not

Quick Chat is the plain-English layer. Before configuring it, I asked it
questions whose answers I had already calculated independently from the raw
files, so that agreement or disagreement would be meaningful rather than
reassuring.

**Where it agreed — which was most of the time.** On totals and counts it was
exact: 499 deals, 315 won and 184 lost; $707,201 of booked revenue and an
average won deal of $2,245.08; 2,240 leads with 609 responses; the ticket split
across priority levels; and the 24 missing income values. These matched the
dashboard and my own calculations to the cent.

**Where it differed.** Asked about resolution times, Quick Chat reported 1.79
days for critical and 1.97 days for low priority, against the dashboard's 56.6
and 59.4 hours. This is not an error by either system. Quick Chat counts whole
calendar days and discards the time of day; the dashboard measures exact elapsed
time. I reproduced the calendar-day method by hand and got 1.79 and 1.97 exactly,
which confirms the explanation. Importantly, **both methods lead to the same
conclusion** — critical tickets are barely faster than low-priority ones — and
Quick Chat volunteered that interpretation without being prompted.

**Where it added something.** Asked only for spend and revenue totals, Quick
Chat noted unprompted that spend far exceeded attributed revenue and suggested
looking at which campaigns were driving the gap. That is the same
over-attribution problem described above, found independently.

**What this means for how the team should use it.** Quick Chat is reliable for
"what is the number" questions and genuinely fast for ad-hoc ones nobody
anticipated. It is less reliable when a metric depends on a definition — a
window, a unit, or which rows to exclude — because it will pick a reasonable
definition without announcing it. The rule I would give the team: use the
dashboard when the number goes in front of a customer or a board, and use Quick
Chat to explore and to decide what to look at next. When the two disagree, the
difference is almost always a definition, and it is worth understanding rather
than overriding.

---

## Terms used in this report

- **Left join** — a rule for combining tables that keeps every row from the main
  table even when the other table has no match for it.
- **Row multiplication (fan-out)** — when combining tables causes one row to
  repeat because the other table has several matching rows.
- **SPICE** — the in-memory engine that stores the data so the dashboard
  responds instantly instead of re-querying the source systems.
- **Topic** — a business-language description of the data that teaches the
  natural-language tool what the fields mean.
- **Attributed revenue** — revenue the marketing system credits to a campaign,
  as distinct from revenue actually booked in the CRM.
