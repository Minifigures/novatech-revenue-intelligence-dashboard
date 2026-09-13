# NovaTech Ground-Truth Figures

Computed directly from the three starter CSVs by `analysis/ground_truth.py`.

Every number quoted in the verification log, Q exploration log, dashboard
annotations and executive report traces back to this file.


## 1. CRM Deals

| Metric | Value |
|---|---|
| Rows / columns | 499 / 20 |
| Unique accounts / companies | 85 / 85 |
| Won / Lost | 315 / 184 |
| Win rate | 63.1% |
| Total won revenue | $707,201.00 |
| Average won deal value | $2,245.08 |
| Median won deal value | $1,040.00 |
| Avg days to close (all) | 66.8 |
| Avg days to close (won / lost) | 71.9 / 57.9 |
| Closed date range | 2023-12-03 → 2025-01-31 |
| loss_reason nulls | 315 |

### Win rate & revenue by region

| Region | Deals | Won | Win rate | Revenue |
|---|---|---|---|---|
| Central | 206 | 144 | 69.9% | $274,285.00 |
| West | 165 | 97 | 58.8% | $248,243.00 |
| East | 128 | 74 | 57.8% | $184,673.00 |

### Win rate & revenue by company size tier

| Size tier | Deals | Won | Win rate | Revenue | Avg won deal |
|---|---|---|---|---|---|
| Enterprise | 201 | 127 | 63.2% | $319,423.00 | $2,515.14 |
| Large | 216 | 133 | 61.6% | $271,613.00 | $2,042.20 |
| Medium | 43 | 29 | 67.4% | $58,192.00 | $2,006.62 |
| Small | 39 | 26 | 66.7% | $57,973.00 | $2,229.73 |

### Revenue by product

| Product | Deals | Win rate | Revenue | Avg won deal |
|---|---|---|---|---|
| NovaPulse Professional | 76 | 57.9% | $208,724.00 | $4,743.73 |
| NovaPulse Enterprise | 51 | 66.7% | $188,843.00 | $5,554.21 |
| NovaEdge Advanced | 90 | 51.1% | $155,390.00 | $3,378.04 |
| NovaPulse Ultimate | 2 | 100.0% | $53,176.00 | $26,588.00 |
| NovaPulse Standard | 78 | 61.5% | $52,372.00 | $1,091.08 |
| NovaPulse Starter | 118 | 69.5% | $45,445.00 | $554.21 |
| NovaEdge Lite | 84 | 70.2% | $3,251.00 | $55.10 |

### Loss reasons

| Loss reason | Deals | % of losses |
|---|---|---|
| No Decision Made | 43 | 23.4% |
| Poor Product Fit | 43 | 23.4% |
| Competitor Won | 34 | 18.5% |
| Timing Not Right | 33 | 17.9% |
| Budget Constraints | 31 | 16.8% |

### Trend by close year

| Year | Deals | Win rate | Revenue | Avg days to close |
|---|---|---|---|---|
| 2023 | 41 | 90.2% | $83,259.00 | 79.5 |
| 2024 | 430 | 60.5% | $596,739.00 | 64.0 |
| 2025 | 28 | 64.3% | $27,203.00 | 90.1 |

## 2. Marketing Campaigns

| Metric | Value |
|---|---|
| Rows / columns | 2240 / 20 |
| Unique leads | 2240 |
| Unique accounts | 100 |
| Orphan accounts / rows | 15 / 150 (6.7%) |
| annual_income nulls | 24 (1.1%) |
| Responded | 609 (27.2%) |
| Total campaign spend | $12,359,497.34 |
| Total revenue attributed | $1,127,223.09 |
| Net | $-11,232,274.25 |
| Overall ROI | -90.9% |
| Campaign date range | 2023-01-01 → 2025-01-31 |

### Funnel stage distribution

| Funnel stage | Leads | % of leads |
|---|---|---|
| Prospect | 404 | 18.0% |
| Lead | 465 | 20.8% |
| Qualified Lead | 848 | 37.9% |
| Opportunity | 111 | 5.0% |
| Closed Won | 412 | 18.4% |

### Campaign performance (sorted by ROI)

| Campaign | Leads | Response rate | Spend | Revenue attributed | Net | ROI |
|---|---|---|---|---|---|---|
| NovaPulse Launch | 409 | 35.2% | $2,423,202.47 | $394,156.59 | $-2,029,045.88 | -83.7% |
| Enterprise Expansion | 389 | 27.8% | $2,114,968.95 | $194,356.76 | $-1,920,612.19 | -90.8% |
| Year-End Accelerator | 340 | 17.4% | $1,894,047.50 | $174,765.73 | $-1,719,281.77 | -90.8% |
| Digital Retarget | 419 | 34.8% | $2,423,781.95 | $196,249.17 | $-2,227,532.78 | -91.9% |
| Q3 Growth Sprint | 410 | 32.9% | $1,984,711.38 | $133,415.20 | $-1,851,296.18 | -93.3% |
| NovaEdge Awareness | 273 | 6.2% | $1,518,785.09 | $34,279.64 | $-1,484,505.45 | -97.7% |

### Channel performance (sorted by ROI)

| Channel | Leads | Response rate | Spend | Revenue attributed | Net | ROI |
|---|---|---|---|---|---|---|
| Direct Mail | 149 | 53.0% | $721,309.14 | $211,067.12 | $-510,242.02 | -70.7% |
| Partner Referral | 807 | 34.3% | $7,270,706.10 | $676,976.95 | $-6,593,729.15 | -90.7% |
| Paid Social | 325 | 40.3% | $2,336,908.53 | $180,187.48 | $-2,156,721.05 | -92.3% |
| Email | 288 | 8.7% | $490,321.32 | $24,939.68 | $-465,381.64 | -94.9% |
| Organic Search | 671 | 14.5% | $1,540,252.25 | $34,051.86 | $-1,506,200.39 | -97.8% |

### Channel → Closed Won conversion

| Channel | Leads | Closed Won | Closed-Won rate |
|---|---|---|---|
| Direct Mail | 149 | 73 | 49.0% |
| Partner Referral | 807 | 251 | 31.1% |
| Paid Social | 325 | 74 | 22.8% |
| Email | 288 | 8 | 2.8% |
| Organic Search | 671 | 6 | 0.9% |

## 3. Support Tickets

| Metric | Value |
|---|---|
| Rows / columns | 3000 / 20 |
| Unique tickets | 2996 |
| Unique accounts | 100 |
| Orphan accounts / rows | 15 / 204 (6.8%) |
| Unresolved tickets | 59 (2.0%) |
| Avg resolution | 58.7 h |
| Median resolution | 51.86 h |
| Ticket date range | 2023-06-01 → 2025-02-28 |
| Security incidents | 14 |
| Data-loss events | 11 |
| Total downtime (min) | 47,255 |

### Resolution time by priority

| Priority | Tickets | Resolved | Avg hours | Avg days |
|---|---|---|---|---|
| critical | 50 | 48 | 56.6 | 2.36 |
| high | 400 | 391 | 58.12 | 2.42 |
| medium | 1050 | 1037 | 58.0 | 2.42 |
| low | 1500 | 1465 | 59.42 | 2.48 |

### Product area load & resolution

| Product area | Tickets | Avg resolution (h) |
|---|---|---|
| Data Pipeline | 310 | 59.7 |
| Mobile App | 581 | 59.55 |
| Analytics Dashboard | 597 | 58.78 |
| Billing | 329 | 58.75 |
| Notifications | 601 | 58.33 |
| Authentication | 582 | 57.61 |

### Sentiment

| Sentiment | Tickets | % |
|---|---|---|
| neutral | 1953 | 65.1% |
| negative | 684 | 22.8% |
| positive | 304 | 10.1% |
|  | 59 | 2.0% |

### Top 10 accounts by ticket volume

| Account | Tickets |
|---|---|
| ACCT-041 | 334 |
| ACCT-035 | 180 |
| ACCT-076 | 176 |
| ACCT-043 | 171 |
| ACCT-060 | 142 |
| ACCT-036 | 140 |
| ACCT-020 | 109 |
| ACCT-072 | 90 |
| ACCT-025 | 89 |
| ACCT-018 | 83 |

## 4. Cross-Domain (unified)

| Metric | Value |
|---|---|
| Accounts in CRM / Marketing / Support | 85 / 100 / 100 |
| Accounts in all three | 85 |
| Orphan account IDs | ACCT-101, ACCT-102, ACCT-103, ACCT-104, ACCT-105, ACCT-106, ACCT-107, ACCT-108, ACCT-109, ACCT-110, ACCT-111, ACCT-112, ACCT-113, ACCT-114, ACCT-115 |
| Revenue ↔ ticket-volume correlation | 0.567 |
| At-risk accounts | 3 |
| Revenue at risk | $42,040.00 (5.9% of won revenue) |
| Top-10 revenue ∩ top-10 tickets | 4 accounts |

### Join row-count arithmetic (fan-out)

| Join | Rows |
|---|---|
| CRM only (anchor) | 499 |
| CRM ⟕ Support | 23,590 |
| CRM ⟕ Marketing | 13,738 |
| CRM ⟕ Marketing ⟕ Support (3-way) | 63,420 |
| Fan-out multiple vs CRM | 127.1× |

### At-risk accounts (above-median revenue + above-median tickets + ≥30% negative)

| Account | Company | Tier | Revenue | Tickets | Negative | Negative % | Crit/High |
|---|---|---|---|---|---|---|---|
| ACCT-011 | Falcon Software | Large | $20,912.00 | 37 | 15 | 40.5% | 6 |
| ACCT-072 | HavenCrest Communications | Enterprise | $13,789.00 | 90 | 28 | 31.1% | 17 |
| ACCT-022 | NorthStar Finance | Large | $7,339.00 | 11 | 6 | 54.5% | 1 |

### Top 10 accounts by revenue

| Account | Company | Revenue | Tickets | Negative % |
|---|---|---|---|---|
| ACCT-041 | YieldMax Software | $40,722.00 | 334 | 18.9% |
| ACCT-045 | CedarPoint Medical | $27,933.00 | 30 | 20.0% |
| ACCT-011 | Falcon Software | $20,912.00 | 37 | 40.5% |
| ACCT-062 | StoneHarbor Medical | $17,362.00 | 49 | 26.5% |
| ACCT-005 | CoralBay Pharma | $17,205.00 | 1 | 0.0% |
| ACCT-027 | RiverStone Imports | $16,866.00 | 6 | 16.7% |
| ACCT-035 | TrueNorth Electronics | $16,747.00 | 180 | 25.6% |
| ACCT-076 | LionGate Holdings | $16,275.00 | 176 | 21.6% |
| ACCT-060 | RedCedar Software | $15,780.00 | 142 | 24.6% |
| ACCT-024 | PeakVista Capital | $15,381.00 | 46 | 21.7% |

### Accounts with >3 tickets in trailing 30 days

| Metric | Value |
|---|---|
| Accounts (also in CRM) | 75 |
| Avg won deal value — those accounts | $2,241.88 |
| Avg won deal value — all other accounts | $2,272.42 |
