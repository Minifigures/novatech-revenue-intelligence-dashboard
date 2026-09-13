# NovaTech Revenue Intelligence Dashboard

Unifying siloed CRM, marketing and support data into a single interactive
dashboard with natural-language querying, built on **Amazon Quick Suite**
(QuickSight, Quick Chat and Topics).

AWS AI/ML Scholars — Business Intelligence & Knowledge Management Foundations,
Project 1.

---

## The problem

NovaTech Solutions is a B2B SaaS company whose revenue data lives in three
systems that do not talk to each other: a CRM, a marketing platform, and a
support ticketing system. Every Monday the revenue team manually pulls reports
from all three to answer basic cross-functional questions. Nobody can answer
"are our highest-value customers also the ones filing the most tickets?"
without an hour of spreadsheet work.

The brief, from VP of Revenue Sarah Chen, was to unify the three sources into
one dashboard with three views — Marketing Funnel, Sales Pipeline and Customer
Health — and make the data queryable in plain English.

---

## What the data actually says

Every figure below is computed from the raw CSVs by
[`analysis/ground_truth.py`](analysis/ground_truth.py) and cross-checked against
the dashboard.

| Finding | Evidence |
|---|---|
| **Direct Mail converts 54× better than Organic Search** | 49.0% of Direct Mail's 149 leads reach Closed Won vs 0.9% of Organic Search's 671. Organic Search + Email burn $2.03M to produce 14 closed-won leads. |
| **Priority is not driving support response** | Critical tickets resolve in 56.6 h, low-priority in 59.4 h — a 2.8 h difference. The priority field is recorded but not acted on. |
| **The biggest customer is the biggest support burden** | YieldMax Software is the top revenue account ($40,722) *and* files 334 tickets — 11.1% of all tickets. Revenue and ticket volume correlate at **0.57** across 85 accounts. |
| **Half of all losses are self-inflicted** | "No Decision Made" (43) and "Poor Product Fit" (43) account for 46.7% of 184 losses; Competitor Won is only 18.5%. |
| **Marketing over-reports revenue by 1.59×** | Marketing attributes $1,127,223 against $707,201 actually booked in CRM, and claims 412 closed-won leads against 315 won deals. |
| **A 12.1-point regional win-rate gap** | Central closes 69.9%, East 57.8%. Closing East at Central's rate is worth roughly $38,600 on the same lead volume. |

---

## Data quality: 20 checks, 5 failures

The shipped data disagrees with its own data dictionary in four ways that
change how metrics must be built — see
[`analysis/data_quality.md`](analysis/data_quality.md).

1. **`ticket_id` is not unique.** 2,996 distinct IDs across 3,000 rows; 4 IDs are
   reused by two different accounts. Ticket counts are taken by row, never by
   distinct ID.
2. **59 tickets have null `customer_sentiment`**, a field the dictionary says is
   never null. Handled with a `sentiment_clean` calculated field that relabels
   them "Unresolved" so the sentiment chart still totals 3,000.
3. **Marketing over-attributes revenue** (see table above). CRM is treated as the
   single source of truth for revenue; attributed revenue only ranks campaigns
   against each other.
4. **354 orphan rows** reference accounts ACCT-101–115 that do not exist in CRM.
   This is why the unified dataset uses left joins from a CRM anchor — an inner
   join would silently discard them.

---

## Join strategy

The unified dataset anchors on **CRM deals** and **left joins** marketing and
support on `account_id`:

```
crm_deals (499)
   └─ LEFT JOIN marketing_campaigns  ON account_id     → 13,738 rows
        └─ LEFT JOIN support_tickets ON account_id     → 63,420 rows
```

Anchoring on CRM keeps every deal even where an account has no marketing
touchpoint or no tickets; left joins preserve the orphan-free deal list while
still admitting accounts that exist only downstream.

**Row multiplication is real and expected.** Each deal fans out across that
account's leads *and* tickets, so 499 deals become 63,420 rows — a **127×**
expansion. That makes the unified dataset safe for *account-level* questions
("do high-revenue accounts file more tickets?") and unsafe for naive sums:
summing `deal_value` over the joined table would overstate revenue by roughly
127×. The dashboard therefore takes every revenue and ticket KPI from the
single-source datasets, and uses the unified dataset only where a genuine
cross-domain comparison is needed.

---

## Repository layout

```
├── analysis/
│   ├── ground_truth.py        # every figure quoted anywhere, from the raw CSVs
│   ├── ground_truth.md        # readable output
│   ├── data_quality.py        # 20 checks against the data dictionary
│   └── data_quality.md        # readable output
├── data/                      # the three source CSVs
├── deliverables/              # submission artifacts (logs, report, annotations)
├── docs/                      # data dictionary, company background, VP brief
└── screenshots/               # dashboard and Quick Chat evidence
```

## Reproducing the analysis

No dependencies beyond the Python standard library:

```bash
python3 analysis/ground_truth.py && python3 analysis/data_quality.py
```

---

## Deliverables

| File | What it is |
|---|---|
| [`01_verification_log.md`](deliverables/01_verification_log.md) | 7 Quick Chat checks across all three knowledge bases, each against an independently computed expected answer |
| [`05_q_exploration_log.md`](deliverables/05_q_exploration_log.md) | Natural-language exploration, cross-checked against the dashboard |
| [`07_dashboard_annotations.md`](deliverables/07_dashboard_annotations.md) | Annotation text: quantified finding → business implication → action |
| [`08_executive_report.md`](deliverables/08_executive_report.md) | 1–3 page report for VP Sarah Chen |

---

## Built with

Amazon Quick Suite (Quick Sight, Quick Chat, Topics), SPICE in-memory engine,
no-code ETL in the Data section, and Python 3 for independent verification.
