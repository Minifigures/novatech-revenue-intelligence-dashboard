# Screenshot shot list

Everything below is **already built and saved** in the Vocareum Amazon Quick
workspace. Each row is a direct link plus what to capture. Press **⌘⇧4** then
**Space** to capture the whole browser window, and save with the filename given.

> The rubric asks for screenshots of the import, the transformations, the join,
> the Topic, and the before/after Quick Chat responses. The dashboard itself is
> already covered by `deliverables/03_dashboard_export_all_sheets.pdf`, so these
> are the remaining items.

**Prerequisite:** the Cloud Resource must be running. If the links 404, reopen
the lab from the Udacity **Cloud Resources** tab → *Open Cloud Console* →
`UdacityQuicksightLab`, then use the links below.

---

## 1. Data import into SPICE  → `screenshots/01_data_import/`

| # | Link | Capture | Save as |
|---|---|---|---|
| 1.1 | [Datasets list](https://us-west-2.quicksight.aws.amazon.com/sn/account/UdacityQuicksightLab/start/data?tab=dataset) | The four datasets owned by **Me**, each tagged **SPICE**: NovaTech CRM Deals (prepared), NovaTech Marketing Campaigns (prepared), NovaTech Support Tickets (prepared), NovaTech Unified Revenue Dataset (CRM anchor) | `01_datasets_in_spice.png` |

*Row counts to quote in the caption: CRM 499, Marketing 2,240, Support 3,000,
Unified 63,420.*

---

## 2. Transformations  → `screenshots/02_transformations/`

| # | Link | Capture | Save as |
|---|---|---|---|
| 2.1 | [CRM dataset editor](https://us-west-2.quicksight.aws.amazon.com/sn/account/UdacityQuicksightLab/data-sets/f094ef46-e0d2-4e14-a29e-243b687cd2f3/prepare) | Click the **Change data type 1** node. Shows six corrected types — note `deal_value` set to **Decimal** (Quick had auto-detected Integer) | `02_data_type_corrections.png` |
| 2.2 | Same page | Click the **Add calculated…** node. Shows 3 calculated fields: `days_to_close`, `is_won`, `discount_from_list_pct` | `03_calculated_fields_crm.png` |
| 2.3 | [Support dataset editor](https://us-west-2.quicksight.aws.amazon.com/sn/account/UdacityQuicksightLab/data-sets/0c10913b-5621-44fd-a365-2dfdba710982/prepare) | The **Add calculated…** node: `resolution_hours`, `sentiment_clean`, `is_high_priority`, `is_negative_sentiment` | `04_calculated_fields_support.png` |
| 2.4 | [Marketing dataset editor](https://us-west-2.quicksight.aws.amazon.com/sn/account/UdacityQuicksightLab/data-sets/c3509507-46ee-4d87-bca5-915b01a1c3f0/prepare) | The **Add calculated…** node: `campaign_roi_pct`, `is_closed_won_lead`, `net_campaign_contribution` | `05_calculated_fields_marketing.png` |

---

## 3. The join  → `screenshots/02_transformations/`

| # | Link | Capture | Save as |
|---|---|---|---|
| 3.1 | [Unified dataset editor](https://us-west-2.quicksight.aws.amazon.com/sn/account/UdacityQuicksightLab/data-sets/0e5a2b1b-9021-4729-ab2a-b622cd309e1b/prepare) | The **flow diagram** at the top: `novatech_crm_deals.csv → Change data type 1 → Join 1 → Join 2`, with Marketing and Support feeding in as RIGHT inputs | `06_join_diagram.png` |
| 3.2 | Same page | Click the **Join 2** node. Shows **Left join**, left table `Join 1`, right table `NovaTech Support Tickets (prepared)`, join keys `account_id.1 = account_id` | `07_join_configuration.png` |
| 3.3 | Same page | Click the **Join 1** node. Shows **Left join**, CRM → Marketing on `account_id = account_id` | `08_join_configuration_marketing.png` |

---

## 4. Topic before / after  → `screenshots/04_topic_before_after/`

| # | Link | Capture | Save as |
|---|---|---|---|
| 4.1 | [Baseline chat (before Topic)](https://us-west-2.quicksight.aws.amazon.com/sn/account/UdacityQuicksightLab/start/chat?conversationId=ce07c8e5-8331-4509-b667-efdc6cafed16) | Scroll to the top. Three Q&As scoped to the **dashboard**. Capture each — note the revenue answer says "Completed 5 steps" | `09_baseline_q1_revenue.png`, `10_baseline_q2_channel.png`, `11_baseline_q3_resolution.png` |
| 4.2 | [Topic definition](https://us-west-2.quicksight.aws.amazon.com/sn/account/UdacityQuicksightLab/topics/5EuUlREohi3Z0hxZABAWosyGgEMpIkIQ) | The **Datasets (4)** tab, showing the Topic name, description and Version 2 (Active) | `12_topic_setup.png` |
| 4.3 | Same page → **Custom instructions** tab | The business glossary, data-quality rules, fan-out rule and fields-to-ignore list | `13_topic_custom_instructions.png` |
| 4.4 | [Post-Topic chat](https://us-west-2.quicksight.aws.amazon.com/sn/account/UdacityQuicksightLab/start/chat?conversationId=94151d4a-7876-4e56-b2c0-1b887eb840e3) | The same three questions, scoped to the **Topic**. Note the revenue answer now says "Completed 1 step" | `14_after_q1_revenue.png`, `15_after_q2_channel.png`, `16_after_q3_resolution.png` |
| 4.5 | Same chat, further down | The cross-dataset answer (top accounts by tickets + booked revenue, ~$154.7K / 22%) | `17_cross_dataset_question.png` |

---

## 5. Annotated dashboard  → `screenshots/05_annotations/`

| # | Link | Capture | Save as |
|---|---|---|---|
| 5.1 | [Dashboard — Marketing Funnel](https://us-west-2.quicksight.aws.amazon.com/sn/account/UdacityQuicksightLab/dashboards/9431eba0-ab20-45cb-bf1e-103f3005e657) | Scroll to the bottom of the sheet — the **CHANNEL MIX IS UPSIDE DOWN** annotation | `18_annotation_marketing.png` |
| 5.2 | Same dashboard → **Sales Pipeline** tab | Bottom of sheet — **REGIONAL WIN-RATE GAP AND LOSABLE LOSSES** | `19_annotation_sales.png` |
| 5.3 | Same dashboard → **Customer Health** tab | Bottom of sheet — **AT-RISK ACCOUNTS** | `20_annotation_customer_health.png` |

---

## 6. Interactivity (optional but strengthens the submission)

| # | Where | Capture | Save as |
|---|---|---|---|
| 6.1 | Dashboard → Customer Health | Click a bar in **Ticket Volume by Product Area** — the other visuals filter. Capture the filtered state | `21_one_click_filter.png` |
| 6.2 | Dashboard → Customer Health | Right-click a bar in the same chart — the menu shows **"Go to Sales Pipeline for this account"** | `22_cross_sheet_navigation.png` |
| 6.3 | Any sheet | Open a filter control at the top (e.g. `sales_region`) and pick one value; capture the updated visuals | `23_filter_control_in_action.png` |
