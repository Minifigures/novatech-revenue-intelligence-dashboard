# NovaTech Data Verification Log

**Student Name:** Marco Anthony Ayuste
**Date:** 13 September 2026
**Environment:** Amazon Quick Suite (Vocareum lab, `UdacityQuicksightLab`, us-west-2)
**Method:** Each question was asked in Quick Chat scoped to a single pre-indexed
dataset. The expected answer was computed independently from the raw CSVs before
asking, using `analysis/ground_truth.py`, so every check is decisive rather than
confirmatory.

---

## Verification Log

| # | Knowledge Base | Question Asked | Expected Answer | Q's Actual Answer | Match? | Notes |
|---|---|---|---|---|---|---|
| 1 | NovaTech CRM Deals | How many total deal records are in this dataset, and how many are Won versus Lost? | 499 rows; Won 315, Lost 184 (63.1% win rate) | Total Deals **499**; Won **315 (63.1%)**; Lost **184 (36.9%)** | ✅ Pass | Exact match on all three figures. Confirms the full 499 rows reached SPICE with no truncation, and that the win-rate KPI can be trusted. |
| 2 | NovaTech CRM Deals | What is the total deal_value for Won deals, and what is the average Won deal value? | Total $707,201.00; average $2,245.08; 315 won deals | Total Deal Value **$707,201.00**; Average Deal Value **$2,245.08**; Number of Won Deals **315** | ✅ Pass | Exact to the cent. This is the revenue figure every other revenue KPI is reconciled against. |
| 3 | NovaTech CRM Deals | What is the earliest and latest deal_created_date, and how many rows have a blank loss_reason? | 2023-06-17 → 2025-01-25; 315 blank loss_reason | Earliest **June 17, 2023**; Latest **January 25, 2025**; **315 rows** blank | ✅ Pass | Confirms the data dictionary's stated date range refers to `deal_created_date`, not `deal_closed_date` (which actually runs to 2025-01-31). Q correctly reasoned that the 315 blanks align with the 315 Won deals. |
| 4 | NovaTech Marketing Campaigns | How many lead records are in this dataset, and how many responded to a campaign? | 2,240 leads; 609 responded (27.2%) | Total Lead Records **2,240**; Responded **609 (~27.2%)**; Did Not Respond **1,631 (~72.8%)** | ✅ Pass | Exact match. Confirms one row per lead and validates the response-rate KPI on the Marketing Funnel sheet. |
| 5 | NovaTech Marketing Campaigns | How many rows have a missing annual_income? Total campaign_spend and total revenue_attributed? | 24 blank incomes; spend $12,359,497.34; attributed $1,127,223.09 | **24 rows** missing; Total Campaign Spend **$12,359,497.34**; Total Revenue Attributed **$1,127,223.09** | ✅ Pass | Exact to the cent. Q additionally volunteered that spend far exceeds attributed revenue, independently surfacing the negative-ROI problem discussed in the report. |
| 6 | NovaTech Support Tickets | How many ticket records, how many have no ticket_resolved_date, and what is the count per priority? | 3,000 rows; 59 unresolved; low 1,500 / medium 1,050 / high 400 / critical 50 | **59** unresolved; Low **1,500 (50.0%)**; Medium **1,050 (35.0%)**; High **400 (13.3%)**; Critical **50 (1.7%)** | ✅ Pass | Exact match on every priority bucket and on the documented 59 unresolved tickets. |
| 7 | NovaTech Support Tickets | Average resolution time for critical vs low priority tickets? How many tickets have blank customer_sentiment? | Critical 56.60 h (2.36 d); Low 59.42 h (2.48 d). **59** blank customer_sentiment — a value the data dictionary claims is never null | Critical **1.79 days (~42.9 h)**; Low **1.97 days (~47.3 h)**; **59 tickets** blank `customer_sentiment` | ⚠️ Partial — explained | **Sentiment count: exact match, and it contradicts the data dictionary** (which states `customer_sentiment` has no nulls). **Resolution time: a measurement-definition difference, not an error.** Q measures whole calendar days and drops the time of day; I measure exact elapsed time. Reproduced locally: the calendar-day method yields exactly 1.79 and 1.97 days, matching Q to two decimals. Both methods agree on the business conclusion. |
| 8 | NovaTech Reference Documents | (Attempted) Query the Company Background knowledge base | Company background facts: ~200 employees, ~$50M annual revenue, 85 accounts | **No knowledge base exists in the workspace** — the Knowledge Bases tab reports "You haven't created any knowledge base yet" | ❌ Fail — environment gap | The Environment Setup page lists a "Company Background knowledge base" as pre-provisioned, but only the four *datasets* are present in this lab. Documented rather than worked around; company context was taken from the supplied `novatech_company_background.pdf` instead. |

**Coverage:** 7 answered entries across all three required knowledge bases
(3 CRM, 2 Marketing, 2 Support), plus 1 documented environment gap — above the
6-entry minimum.

---

## The one discrepancy, in detail

Entry 7 is the only case where Q's number differed from the expected value, and
the cause is a definition difference rather than a data fault.

| Method | Critical | Low | Gap |
|---|---|---|---|
| Exact elapsed time (`resolved_at − created_at`) | 56.60 h / 2.36 d | 59.42 h / 2.48 d | 2.82 h |
| Whole calendar days (drops time of day) | 1.79 d | 1.97 d | 0.18 d (~4.4 h) |
| **Q's answer** | **1.79 d (~42.9 h)** | **1.97 d (~47.3 h)** | **0.18 d (~4.4 h)** |

`ticket_created_date` is a plain date (implicitly midnight) while
`ticket_resolved_date` is a full timestamp. Counting whole calendar days between
them discards up to 24 hours of the first partial day, which is why Q's figure
is roughly half a day lower. Reproducing the calendar-day method locally
returned 1.79 and 1.97 days — matching Q exactly — which confirms the
explanation.

**Why it does not change any conclusion:** both methods rank the four priority
levels identically and both show critical tickets resolving only marginally
faster than low-priority ones. Q reached the same interpretation unprompted,
noting the difference "is relatively small, which could suggest room for
improvement in prioritizing critical issue resolution." The dashboard reports
exact elapsed hours, and that choice is stated on the Customer Health sheet so
the two numbers can never be silently compared.

---

## Cross-Check

Independent confirmation of one fact outside Quick Chat.

- **Fact verified:** Total revenue from Won deals.
- **Chat said:** $707,201.00 across 315 Won deals (average $2,245.08).
- **Independent computation:** Summing `deal_value` over the 315 rows where
  `deal_stage = 'Won'` directly from `novatech_crm_deals.csv` gives
  **$707,201.00**, average **$2,245.08**.
- **Dashboard shows:** The Total Won Revenue KPI card on the Sales Pipeline
  sheet reads $707,201.
- **Consistent?** Yes — all three agree exactly.

---

## Data-quality issues found during verification

Verification surfaced four defects that are **not** documented in the data
dictionary. Each one changed how a metric was built; full detail in
`analysis/data_quality.md`.

1. **Undocumented null sentiment (confirmed by Q, entry 7).** 59 tickets carry
   no `customer_sentiment` despite the dictionary stating the field is never
   null. They are relabelled "Unresolved" on the dashboard rather than dropped,
   so the sentiment chart still totals 3,000.
2. **Reused ticket IDs.** `ticket_id` is described as unique, but 4 IDs appear
   twice (TKT-284055, TKT-679459, TKT-946331, TKT-634299) — 2,996 distinct IDs
   across 3,000 rows. Each pair belongs to two different accounts, so the rows
   are genuinely separate tickets with a collided ID. Ticket counts are
   therefore taken by row, never by distinct ID.
3. **Marketing over-attribution.** Marketing reports 412 "Closed Won" leads and
   $1,127,223 of attributed revenue against 315 Won deals and $707,201 booked in
   CRM — a 1.59× overstatement. CRM is treated as the single source of truth for
   revenue; attributed revenue is used only to rank campaigns against each other.
4. **Orphan account IDs.** 150 marketing rows and 204 support rows reference
   ACCT-101–115, which do not exist in CRM. This is documented and expected, and
   it is the reason the unified dataset uses left joins from a CRM anchor rather
   than inner joins — an inner join would silently discard 354 rows.
