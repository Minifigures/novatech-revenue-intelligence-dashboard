# NovaTech Data Dictionary

Defines every field across the three NovaTech datasets. All three files
share `account_id` as the primary join key.

---

## Dataset Overview

| Dataset | File | Rows | Columns | Date Range |
|---------|------|------|---------|------------|
| CRM Deals | novatech_crm_deals.csv | 499 | 20 | 2023-06-17 to 2025-01-25 |
| Marketing Campaigns | novatech_marketing_campaigns.csv | 2,240 | 20 | 2023-01-01 to 2025-01-31 |
| Support Tickets | novatech_support_tickets.csv | 3,000 | 20 | 2023-06-01 to 2025-02-28 |

## How the Datasets Connect

```
novatech_crm_deals.csv
        |
        +-- account_id --+-- novatech_marketing_campaigns.csv
                         |
                         +-- novatech_support_tickets.csv
```

- **CRM** contains 85 unique accounts (ACCT-001 through ACCT-085).
- **Marketing** and **Support** reference those same account IDs, plus a
  small number of orphan IDs (ACCT-101 through ACCT-115) that do not
  appear in CRM. This is intentional — not every marketing lead or
  support ticket maps to a known CRM account.

---

## 1. novatech_crm_deals.csv

Sales pipeline data — 499 closed deals (won and lost).

#### `account_id`

- **Type:** String
- **Description:** Unique account identifier. Primary join key across all three datasets.
- **Example:** ACCT-007, ACCT-042, ACCT-085
- **Nulls:** None
- **Notes:** 85 unique accounts. Format: `ACCT-XXX` (zero-padded 3-digit number).

#### `company_name`

- **Type:** String
- **Description:** Company name associated with the account.
- **Example:** RavenCroft Studios, Horizon Marketing, IndigoVault Finance
- **Nulls:** None
- **Notes:** 85 unique companies. One-to-one with account_id.

#### `industry`

- **Type:** String
- **Description:** Industry vertical.
- **Valid values:** Business Services, Financial Services, Healthcare, Marketing & Advertising, Media & Entertainment, Professional Services, Retail, Software, Technology, Telecommunications
- **Nulls:** None

#### `company_size_tier`

- **Type:** String
- **Description:** Company size classification based on employee count.
- **Valid values:** Enterprise, Large, Medium, Small
- **Nulls:** None
- **Notes:** Small (<200 employees), Medium (200–999), Large (1,000–4,999), Enterprise (5,000+).

#### `annual_revenue_usd`

- **Type:** Float
- **Description:** Annual revenue in millions of USD.
- **Example:** 4.54 – 11,698.03
- **Nulls:** None
- **Notes:** Represents company-level revenue, not deal-level.

#### `employee_count`

- **Type:** Integer
- **Description:** Total number of employees at the company.
- **Example:** 9 – 34,288
- **Nulls:** None

#### `headquarters`

- **Type:** String
- **Description:** Country where the company is headquartered.
- **Valid values:** Belgium, Brazil, China, Germany, Italy, Japan, Jordan, Kenya, Korea, Norway, Panama, Philipines, Poland, Romania, United States
- **Nulls:** None

#### `opportunity_id`

- **Type:** String
- **Description:** Unique identifier for each sales opportunity.
- **Example:** OPP-13278, OPP-24592, OPP-93810
- **Nulls:** None
- **Notes:** Format: `OPP-XXXXX`.

#### `sales_rep`

- **Type:** String
- **Description:** Name of the sales representative who managed the deal.
- **Example:** Oliver Dubois, Raj Patel, Nadia Volkov
- **Nulls:** None
- **Notes:** 30 unique reps.

#### `sales_manager`

- **Type:** String
- **Description:** Manager of the sales representative.
- **Valid values:** Amanda Foster, Brian Nakamura, David Kim, Michael Chen, Rachel Torres, Sarah Mitchell
- **Nulls:** None

#### `sales_region`

- **Type:** String
- **Description:** Sales region.
- **Valid values:** Central, East, West
- **Nulls:** None

#### `product_name`

- **Type:** String
- **Description:** NovaTech product sold in the deal.
- **Valid values:** NovaEdge Advanced, NovaEdge Lite, NovaPulse Enterprise, NovaPulse Professional, NovaPulse Standard, NovaPulse Starter, NovaPulse Ultimate
- **Nulls:** None

#### `product_category`

- **Type:** String
- **Description:** Product line the product belongs to.
- **Valid values:** NovaEdge, NovaPulse
- **Nulls:** None
- **Notes:** NovaPulse is the core platform line; NovaEdge is the secondary line.

#### `list_price`

- **Type:** Integer
- **Description:** Standard list price of the product in USD.
- **Example:** 55 – 26,768
- **Nulls:** None

#### `deal_stage`

- **Type:** String
- **Description:** Final outcome of the deal.
- **Valid values:** Won, Lost
- **Nulls:** None
- **Notes:** Won: 315 rows, Lost: 184 rows.

#### `deal_created_date`

- **Type:** Date (YYYY-MM-DD)
- **Description:** Date the sales opportunity was created.
- **Example:** 2024-08-15, 2023-12-06, 2024-08-23
- **Nulls:** None

#### `deal_closed_date`

- **Type:** Date (YYYY-MM-DD)
- **Description:** Date the deal was closed (won or lost).
- **Example:** 2024-12-17, 2024-03-20, 2024-09-06
- **Nulls:** None
- **Notes:** Students can compute days-to-close as `deal_closed_date − deal_created_date`.

#### `deal_value`

- **Type:** Float
- **Description:** Actual revenue from the deal in USD.
- **Example:** 0.00 – 27,385.00
- **Nulls:** None
- **Notes:** Always 0 for Lost deals.

#### `loss_reason`

- **Type:** String
- **Description:** Why the deal was lost.
- **Valid values:** Budget Constraints, Competitor Won, No Decision Made, Poor Product Fit, Timing Not Right
- **Nulls:** 315 rows (blank for all Won deals)

#### `data_source`

- **Type:** String
- **Description:** Identifies which dataset this row belongs to.
- **Valid values:** CRM
- **Nulls:** None
- **Notes:** Constant value. Useful after joining datasets to identify row origin.

---

## 2. novatech_marketing_campaigns.csv

Marketing lead and campaign interaction data — 2,240 rows.

#### `account_id`

- **Type:** String
- **Description:** Account identifier. Join key to CRM and Support datasets.
- **Example:** ACCT-012, ACCT-047, ACCT-109
- **Nulls:** None
- **Notes:** Some IDs (ACCT-101 through ACCT-115) are orphans that do not appear in CRM. Orphan rows: 150 (6.7% of rows).

#### `lead_id`

- **Type:** String
- **Description:** Unique identifier for each marketing lead.
- **Example:** LEAD-01826, LEAD-00001, LEAD-10476
- **Nulls:** None
- **Notes:** Format: `LEAD-XXXXX`. One row per lead.

#### `campaign_name`

- **Type:** String
- **Description:** Name of the marketing campaign the lead is associated with.
- **Valid values:** Digital Retarget, Enterprise Expansion, NovaEdge Awareness, NovaPulse Launch, Q3 Growth Sprint, Year-End Accelerator
- **Nulls:** None

#### `campaign_channel`

- **Type:** String
- **Description:** Channel through which the campaign reached the lead.
- **Valid values:** Direct Mail, Email, Organic Search, Paid Social, Partner Referral
- **Nulls:** None

#### `campaign_date`

- **Type:** Date (YYYY-MM-DD)
- **Description:** Date of the campaign interaction.
- **Example:** 2025-01-16, 2025-01-15, 2024-12-10
- **Nulls:** None

#### `funnel_stage`

- **Type:** String
- **Description:** Where the lead sits in the sales funnel.
- **Valid values:** Closed Won, Lead, Opportunity, Prospect, Qualified Lead
- **Nulls:** None
- **Notes:** Ordered progression: Prospect → Lead → Qualified Lead → Opportunity → Closed Won.

#### `customer_segment`

- **Type:** String
- **Description:** Segment classification of the lead.
- **Valid values:** Enterprise, Growth, Professional, Standard, Starter
- **Nulls:** None

#### `annual_income`

- **Type:** Float
- **Description:** Annual household income of the lead contact.
- **Example:** 1,730.00 – 666,666.00
- **Nulls:** 24 rows (1.1%)
- **Notes:** 24 rows have missing income — this is real-world-style missing data.

#### `household_size`

- **Type:** Integer
- **Description:** Number of people in the lead contact's household.
- **Example:** 1 – 4
- **Nulls:** None

#### `days_since_last_engagement`

- **Type:** Integer
- **Description:** Days since the lead last interacted with NovaTech.
- **Example:** 0 – 99
- **Nulls:** None

#### `product_spend_tier1`

- **Type:** Integer
- **Description:** Lead's spend on NovaPulse platform products (USD).
- **Example:** 0 – 1,493
- **Nulls:** None

#### `product_spend_tier2`

- **Type:** Integer
- **Description:** Lead's spend on NovaEdge platform products (USD).
- **Example:** 0 – 1,725
- **Nulls:** None

#### `product_spend_tier3`

- **Type:** Integer
- **Description:** Lead's spend on add-on services (USD).
- **Example:** 0 – 362
- **Nulls:** None

#### `campaign_spend`

- **Type:** Float
- **Description:** Marketing cost attributed to this lead/touchpoint (USD).
- **Example:** 501.71 – 14,995.14
- **Nulls:** None
- **Notes:** Varies by channel. Students can compute campaign ROI as `(revenue_attributed − campaign_spend) / campaign_spend`.

#### `revenue_attributed`

- **Type:** Float
- **Description:** Revenue attributed to this campaign interaction (USD).
- **Example:** 0.00 – 5,575.51
- **Nulls:** None
- **Notes:** 0 for leads that did not convert (campaign_response = 0).

#### `web_visits_per_month`

- **Type:** Integer
- **Description:** Average monthly website visits by this lead.
- **Example:** 0 – 20
- **Nulls:** None

#### `campaign_response`

- **Type:** Integer
- **Description:** Whether the lead responded positively to a campaign.
- **Valid values:** 0 (no response), 1 (responded)
- **Nulls:** None
- **Notes:** Response rate: 27.2% (609 of 2240 leads).

#### `Mkt_Src_Cd`

- **Type:** String
- **Description:** Market source code — the geographic market for this lead.
- **Valid values:** AU, CA, DE, ES, IN, MX, SA, US
- **Nulls:** None
- **Notes:** Two-letter country codes (ISO 3166-1 alpha-2). AU=Australia, CA=Canada, DE=Germany, ES=Spain, IN=India, MX=Mexico, SA=Saudi Arabia, US=United States.

#### `complaint_flag`

- **Type:** Integer
- **Description:** Whether the lead has filed a complaint.
- **Valid values:** 0 (no complaint), 1 (complaint filed)
- **Nulls:** None

#### `data_source`

- **Type:** String
- **Description:** Identifies which dataset this row belongs to.
- **Valid values:** Marketing
- **Nulls:** None
- **Notes:** Constant value.

---

## 3. novatech_support_tickets.csv

Customer support ticket data — 3,000 rows.

#### `account_id`

- **Type:** String
- **Description:** Account identifier. Join key to CRM and Marketing datasets.
- **Nulls:** None
- **Notes:** Some IDs (ACCT-101 through ACCT-115) are orphans that do not appear in CRM. Orphan rows: 204 (6.8% of rows).

#### `ticket_id`

- **Type:** String
- **Description:** Unique identifier for each support ticket.
- **Example:** TKT-966028, TKT-768507, TKT-786393
- **Nulls:** None
- **Notes:** Format: `TKT-XXXXXX`.

#### `ticket_created_date`

- **Type:** Date (YYYY-MM-DD)
- **Description:** Date the ticket was opened.
- **Example:** 2024-07-27, 2023-09-02, 2024-04-07
- **Nulls:** None

#### `ticket_resolved_date`

- **Type:** DateTime (YYYY-MM-DD HH:MM:SS)
- **Description:** Timestamp when the ticket was resolved.
- **Example:** 2024-07-27 07:28:19, 2023-09-05 21:24:38, 2024-04-11 17:48:46
- **Nulls:** 59 rows (2.0%)
- **Notes:** Blank for unresolved tickets. Students can compute resolution time as `ticket_resolved_date − ticket_created_date`.

#### `priority`

- **Type:** String
- **Description:** Ticket severity level.
- **Valid values:** critical, high, low, medium
- **Nulls:** None
- **Notes:** Distribution: low=1500, medium=1050, high=400, critical=50.

#### `product_area`

- **Type:** String
- **Description:** NovaTech product area the ticket relates to.
- **Valid values:** Analytics Dashboard, Authentication, Billing, Data Pipeline, Mobile App, Notifications
- **Nulls:** None

#### `contact_channel`

- **Type:** String
- **Description:** How the customer filed the ticket.
- **Valid values:** Email, Live Chat, Phone, Web Portal
- **Nulls:** None

#### `reported_by`

- **Type:** String
- **Description:** Role of the person who reported the issue.
- **Valid values:** DevOps, Executive, Finance, Product Manager, Support Staff
- **Nulls:** None

#### `customer_tier`

- **Type:** String
- **Description:** The customer's service tier.
- **Valid values:** Basic, Enterprise, Plus
- **Nulls:** None

#### `company_size`

- **Type:** String
- **Description:** Size of the reporting company.
- **Valid values:** Large, Medium, Small
- **Nulls:** None

#### `region`

- **Type:** String
- **Description:** Geographic region.
- **Valid values:** AMER, APAC, EMEA
- **Nulls:** None
- **Notes:** AMER=Americas, EMEA=Europe/Middle East/Africa, APAC=Asia-Pacific.

#### `users_affected`

- **Type:** Integer
- **Description:** Number of end-users impacted by the reported issue.
- **Example:** 0 – 19,417
- **Nulls:** None

#### `error_rate_pct`

- **Type:** Float
- **Description:** Error rate at the time of the ticket, as a percentage.
- **Example:** 0.00 – 83.39
- **Nulls:** None

#### `downtime_minutes`

- **Type:** Integer
- **Description:** Minutes of system downtime caused by the issue.
- **Example:** 0 – 919
- **Nulls:** None

#### `payment_impact`

- **Type:** Integer
- **Description:** Whether payment processing was affected.
- **Valid values:** 0 (no impact), 1 (payment systems affected)
- **Nulls:** None

#### `security_incident`

- **Type:** Integer
- **Description:** Whether the issue involved a security incident.
- **Valid values:** 0 (no), 1 (yes)
- **Nulls:** None

#### `data_loss`

- **Type:** Integer
- **Description:** Whether any data loss occurred.
- **Valid values:** 0 (no), 1 (yes)
- **Nulls:** None

#### `customer_sentiment`

- **Type:** String
- **Description:** Customer's sentiment when filing the ticket.
- **Valid values:** negative, neutral, positive
- **Nulls:** None

#### `tickets_last_30_days`

- **Type:** Integer
- **Description:** Number of tickets this account filed in the previous 30 days.
- **Example:** 0 – 17
- **Nulls:** None
- **Notes:** Higher values may indicate recurring issues or at-risk accounts.

#### `data_source`

- **Type:** String
- **Description:** Identifies which dataset this row belongs to.
- **Valid values:** Support
- **Nulls:** None
- **Notes:** Constant value.
