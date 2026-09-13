# Screenshot index

23 screenshots captured from the live Amazon Quick workspace
(`UdacityQuicksightLab`, us-west-2) on 13 September 2026. Browser chrome is
cropped so each image shows only the application.

## 01 — Data import into SPICE

| File | Shows |
|---|---|
| `01_datasets_in_spice.png` | All four datasets owned by **Me**, each tagged **SPICE**: CRM Deals (prepared), Marketing Campaigns (prepared), Support Tickets (prepared), and the Unified Revenue Dataset (CRM anchor) |

## 02 — Transformations and the join

| File | Shows |
|---|---|
| `02_data_type_corrections.png` | CRM "Change data type" step — six corrected types. **`deal_value` set to Decimal**, correcting Quick's auto-detected Integer |
| `03_calculated_fields_crm.png` | CRM calculated fields: `days_to_close`, `is_won`, `discount_from_list_pct`, with formulas visible |
| `04_calculated_fields_support.png` | Support calculated fields: `resolution_hours`, `sentiment_clean`, `is_high_priority`, `is_negative_sentiment` |
| `05_calculated_fields_marketing.png` | Marketing calculated fields: `campaign_roi_pct`, `is_closed_won_lead`, `net_campaign_contribution` |
| `06_join_diagram.png` | **Join diagram**: `novatech_crm_deals.csv → Change data type 1 → Join 1 → Join 2`, with Marketing and Support entering as RIGHT inputs |
| `07_join_configuration_support.png` | **Join 2 configuration** — Left join, left table `Join 1`, right table `Support Tickets (prepared)`, keys `account_id.1 = account_id` |
| `08_join_configuration_marketing.png` | **Join 1 configuration** — Left join, CRM → Marketing on `account_id = account_id`, with Quick's auto-rename notice for conflicting column names |

## 03 — Dashboard interactivity

| File | Shows |
|---|---|
| `21_one_click_filter_applied.png` | One-click filtering in action. Clicking the **Notifications** bar filtered the whole sheet: tickets 3K → **601**, avg resolution 58.69 → **58.32** h, negative rate 0.23 → **0.21** |
| `22_cross_sheet_navigation_action.png` | The cross-sheet navigation action in the visual's menu: **"Go to Sales Pipeline for this account"** |

*The three dashboard sheets themselves are in
`deliverables/03_dashboard_export_all_sheets.pdf`.*

## 04 — Quick Chat before and after the Topic

**Baseline — scoped to the published dashboard, before any Topic existed:**

| File | Shows |
|---|---|
| `09_baseline_q1_revenue_5steps.png` | "Total revenue from closed-won deals?" → $707,201 across 315 won deals. Marked **"Completed 5 steps"** — it had to reason past the all-deals KPI |
| `10_baseline_q2_channel.png` | Closed-won rate by channel: Direct Mail highest, Partner Referral 31.10%, Paid Social 22.77%, Email 2.78%, Organic Search 0.89% |
| `11_baseline_q3_resolution.png` | Critical 56.59 h vs Low 59.41 h, difference 2.82 h, with the full four-level breakdown |

**The Topic:**

| File | Shows |
|---|---|
| `12_topic_setup.png` | Topic `NovaTech Revenue Intelligence`, **Version 2 (Active)**, four datasets attached |
| `13_topic_custom_instructions.png` | The semantic enrichment: business glossary, six data-quality rules, the fan-out rule, and the fields-to-ignore list |

**After — the same three questions, scoped to the Topic:**

| File | Shows |
|---|---|
| `14_after_q1_revenue_1step.png` | Same $707,201, now **"Completed 1 step"** (down from 5) and phrased as "**booked revenue**" — the glossary term |
| `15_after_q2_channel_with_bad_leadcount.png` | Rates still exact, but the added **"Lead Count" column is wrong** for four of five channels (164/202/144/341 vs the true 807/325/288/671) |
| `16_after_q3_resolution_states_exclusion.png` | Now explicitly states "**Unresolved tickets were excluded from these calculations**" — following the Topic instruction |
| `17_leadcount_correct_when_asked_directly.png` | The same lead-count metric asked as the *main* question returns **correct** values (Partner Referral 807, Organic Search 671) — proving the error above was a one-off in a secondary column |
| `18_cross_dataset_tickets_vs_revenue.png` | **The cross-dataset question.** Top 10 accounts by ticket volume with booked revenue — ACCT-041 at 334 tickets / $40,722 through ACCT-018 at 83 / $8,974. Every value matches `analysis/ground_truth.py` exactly, confirming the fan-out rule held where a naive sum would be ~127× too high |

## 05 — Dashboard annotations

| File | Shows |
|---|---|
| `18_annotation_marketing_funnel.png` | "CHANNEL MIX IS UPSIDE DOWN" — finding, why it matters, action, and the attribution caveat |
| `19_annotation_sales_pipeline.png` | "REGIONAL WIN-RATE GAP AND LOSABLE LOSSES" — the 12.1-point gap and the $38,600 opportunity |
| `20_annotation_customer_health.png` | "AT-RISK ACCOUNTS" — YieldMax, the 0.57 correlation, and the $42,040 at risk. Also shows the unified-dataset table and the sentiment donut including the relabelled **"Unresolved"** slice |
