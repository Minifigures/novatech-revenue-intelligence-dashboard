# NovaTech Data-Quality Audit

Each dataset checked against the claims in `novatech_data_dictionary.txt`.
Produced by `analysis/data_quality.py`.

**20 checks — 15 pass, 5 fail.**

The failures are genuine defects in the shipped data, not import errors. Each
one changes how a metric must be built, so each is carried through to the
dashboard and the executive report.

| ID | Dataset | Check | Expected | Actual | Verdict |
|---|---|---|---|---|---|
| DQ-01 | CRM Deals | Row count | 499 rows (data dictionary) | 499 rows | **PASS** |
| DQ-02 | Marketing | Row count | 2,240 rows | 2240 rows | **PASS** |
| DQ-03 | Support | Row count | 3,000 rows | 3000 rows | **PASS** |
| DQ-04 | CRM Deals | Won / Lost split | Won 315, Lost 184 | Won 315, Lost 184 | **PASS** |
| DQ-05 | CRM Deals | Unique accounts | 85 unique accounts | 85 unique accounts | **PASS** |
| DQ-06 | Support | ticket_id uniqueness | ticket_id described as the unique identifier for each ticket | 2996 distinct ids across 3000 rows — 4 ids reused: TKT-284055, TKT-634299, TKT-679459, TKT-946331 | **FAIL** |
| DQ-07 | Marketing | lead_id uniqueness | One row per lead, 2,240 unique lead_ids | 2240 unique lead_ids | **PASS** |
| DQ-08 | Marketing | annual_income nulls | 24 rows (1.1%) documented as missing | 24 blank rows | **PASS** |
| DQ-09 | Support | ticket_resolved_date nulls | 59 rows (2.0%) documented as unresolved | 59 blank rows | **PASS** |
| DQ-10 | Support | customer_sentiment nulls | Data dictionary states Nulls: None | 59 blank rows (2.0%) | **FAIL** |
| DQ-11 | CRM Deals | loss_reason nulls | 315 blank (one per Won deal) | 315 blank rows | **PASS** |
| DQ-12 | CRM Deals | Date range interpretation | Dictionary lists 2023-06-17 to 2025-01-25 | created 2023-06-17 → 2025-01-25; closed 2023-12-03 → 2025-01-31 | **PASS (clarified)** |
| DQ-13 | CRM Deals | Close date after create date | 0 negative durations | 0 deals close before they are created | **PASS** |
| DQ-14 | Cross-system | Closed-Won count: Marketing vs CRM | Marketing 'Closed Won' leads should reconcile to CRM Won deals (315) | Marketing reports 412 Closed-Won leads vs 315 Won deals in CRM (+97, 30.8% higher) | **FAIL** |
| DQ-15 | Cross-system | Revenue: attributed vs booked | Attributed marketing revenue should not exceed booked CRM revenue | Marketing attributes $1,127,223 vs $707,201 booked in CRM (1.59× overstatement) | **FAIL** |
| DQ-16 | Cross-system | Orphan account_ids | ACCT-101–115 orphans: 150 marketing rows, 204 support rows | 15 orphan ids — 150 marketing rows (6.7%), 204 support rows (6.8%) | **PASS** |
| DQ-17 | CRM Deals | deal_value vs deal_stage | deal_value is 0 for every Lost deal and > 0 for every Won deal | 0 Won deals at $0; 0 Lost deals above $0 | **PASS** |
| DQ-18 | Marketing | campaign_response vs revenue_attributed | revenue_attributed is 0 exactly when campaign_response = 0 | 0 responders with $0 revenue; 0 non-responders with revenue | **PASS** |
| DQ-19 | CRM Deals | headquarters spelling | 15 country values | 15 values; 'Philipines' is misspelled (should be 'Philippines') | **FAIL (cosmetic)** |
| DQ-20 | Cross-system | account_id format | Every account_id matches ACCT-XXX | 0 malformed ids | **PASS** |

## Why each finding matters

- **DQ-01 — CRM Deals: Row count (PASS)** — Import is complete; SPICE row count can be checked against this.
- **DQ-02 — Marketing: Row count (PASS)** — Import is complete.
- **DQ-03 — Support: Row count (PASS)** — Import is complete.
- **DQ-04 — CRM Deals: Won / Lost split (PASS)** — Win-rate KPI (63.1%) is trustworthy.
- **DQ-05 — CRM Deals: Unique accounts (PASS)** — Account-level joins will not silently drop accounts.
- **DQ-06 — Support: ticket_id uniqueness (FAIL)** — ticket_id cannot be used as a primary key or a distinct-count basis. Each reused id belongs to two different accounts, so the rows are genuine separate tickets with a collided id — count tickets by row, not by id.
- **DQ-07 — Marketing: lead_id uniqueness (PASS)** — Lead counts and response rates are safe to compute as row counts.
- **DQ-08 — Marketing: annual_income nulls (PASS)** — Documented gap; exclude nulls from income averages rather than treating as 0.
- **DQ-09 — Support: ticket_resolved_date nulls (PASS)** — Resolution-time averages must exclude these 59 open tickets.
- **DQ-10 — Support: customer_sentiment nulls (FAIL)** — Undocumented nulls. A sentiment breakdown will show a blank category unless it is filtered or relabelled 'Unresolved'.
- **DQ-11 — CRM Deals: loss_reason nulls (PASS)** — Blank is meaningful, not missing — filter to Lost deals for loss analysis.
- **DQ-12 — CRM Deals: Date range interpretation (PASS (clarified))** — The documented range is the deal_created_date range. Closed dates run to 2025-01-31, so date filters must state which date field they use.
- **DQ-13 — CRM Deals: Close date after create date (PASS)** — days-to-close calculated field is safe — no negative values to guard against.
- **DQ-14 — Cross-system: Closed-Won count: Marketing vs CRM (FAIL)** — Marketing counts a lead per touchpoint, CRM counts a deal. The two are not interchangeable — never present them as the same number on one chart.
- **DQ-15 — Cross-system: Revenue: attributed vs booked (FAIL)** — Marketing attribution double-counts revenue across touchpoints. Report booked revenue from CRM as the single source of truth; treat attributed revenue as a relative ranking signal between campaigns only.
- **DQ-16 — Cross-system: Orphan account_ids (PASS)** — Expected and documented. An inner join on account_id would silently discard 354 rows — this is the reason the unified dataset uses left joins from CRM.
- **DQ-17 — CRM Deals: deal_value vs deal_stage (PASS)** — Revenue KPIs can sum deal_value directly without filtering on stage.
- **DQ-18 — Marketing: campaign_response vs revenue_attributed (PASS)** — Response flag and attributed revenue are internally consistent.
- **DQ-19 — CRM Deals: headquarters spelling (FAIL (cosmetic))** — Cosmetic only — it is spelled the same way in every row, so grouping still works. Worth correcting in the dataset editor before the dashboard ships.
- **DQ-20 — Cross-system: account_id format (PASS)** — The join key is clean across all three systems — no trimming or casting needed.

## The four that change the build

1. **DQ-06 — reused ticket ids.** Count support tickets by row, never by `distinct_count(ticket_id)`; the latter under-reports by 4.
2. **DQ-10 — undocumented blank sentiment.** 59 tickets carry no sentiment. They are relabelled rather than dropped so the sentiment chart still sums to 3,000.
3. **DQ-14 / DQ-15 — marketing over-attribution.** Marketing claims 412 closed-won leads and $1.13M of revenue against 315 deals and $707K booked in CRM. Booked CRM revenue is the single source of truth on every revenue KPI; attributed revenue is used only to rank campaigns against each other.
4. **DQ-16 — orphan accounts.** 354 marketing and support rows reference accounts that do not exist in CRM. This is why the unified dataset anchors on CRM with left joins instead of inner joins.
