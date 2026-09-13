# Submission checklist

Rubric requirement → where it is satisfied.

## Data Preparation & Quality

| Requirement | Status | Evidence |
|---|---|---|
| Verification log, ≥6 entries across all three knowledge bases | ✅ | `deliverables/01_verification_log.md` — 7 answered entries (3 CRM, 2 Marketing, 2 Support) plus 1 documented environment gap |
| Each entry has question, Q's response, expected answer, pass/fail | ✅ | Same file. Expected answers computed independently by `analysis/ground_truth.py` before asking |
| Questions target checkable facts (row counts, distinct values, date ranges, nulls) | ✅ | Row counts, Won/Lost split, revenue totals, date ranges, null counts, priority distribution |
| Screenshots of three CSVs imported to SPICE with correct row/column counts | ✅ | Datasets are built and published; `screenshots/01_data_import/` |
| Data type corrections on ≥1 dataset | ✅ | `deal_value` Integer → **Decimal** on CRM; `annual_income` Integer → **Decimal** on Marketing. see `screenshots/README.md`|
| ≥2 calculated fields using business logic | ✅ | **10 fields** across the three datasets. see `screenshots/README.md`|
| Unified dataset joining all three sources, join diagram + configuration visible | ✅ | `NovaTech Unified Revenue Dataset (CRM anchor)`. see `screenshots/README.md`|
| Anchor table and join type identified | ✅ | CRM anchor, left joins — stated in `README.md`, the report, and the Topic instructions |
| All four datasets saved to SPICE | ✅ | Three source + one unified, all SPICE, all owned by you |

## Dashboard Design & Interactivity

| Requirement | Status | Evidence |
|---|---|---|
| Three sheets: Marketing Funnel, Sales Pipeline, Customer Health | ✅ | `deliverables/03_dashboard_export_all_sheets.pdf` |
| Each sheet has ≥1 KPI card and multiple appropriate visuals | ✅ | 4 KPI cards + 4 visuals on Marketing; 4 + 5 on Sales; 3 + 4 on Customer Health |
| Customer Health includes ≥1 visual from the unified dataset | ✅ | "Ticket Volume and Deal Value by Account" |
| ≥2 sheets include interactive filter controls | ✅ | Six filter controls on all three sheets |
| ≥1 sheet has one-click filtering on 2+ visuals | ✅ | Customer Health: click-to-filter on *Ticket Volume by Product Area* and on *Average Resolution Time by Priority*, both targeting all visuals |
| ≥1 cross-sheet navigation action | ✅ | Customer Health → Sales Pipeline, on the product-area visual's menu |
| Published and exported as PDF covering all three sheets | ✅ | 3-page PDF in `deliverables/` |

## AI-Powered Analysis & Communication

| Requirement | Status | Evidence |
|---|---|---|
| Baseline Quick Chat screenshots (2–3 questions before Topic) | ✅ | Answers recorded in `05_q_exploration_log.md` Part 1. see `screenshots/README.md`|
| Topic configured, setup shown | ✅ | `NovaTech Revenue Intelligence`, Version 2 Active. see `screenshots/README.md`|
| Post-Topic screenshots of the same questions | ✅ | Same file. see `screenshots/README.md`|
| Q Exploration Log, ≥5 entries across all three domains incl. 1 cross-dataset | ✅ | 6 entries: Marketing 2, Sales 2, Support 1, cross-dataset 1 |
| Each entry has question, response, dashboard verification | ✅ | Every entry cross-checked against both the dashboard and `ground_truth.py` |
| Dashboard executive summary text (if available) | ✅ | `deliverables/06_dashboard_executive_summary.md` — all three sheets, verified |
| 3–5 annotations, each with a quantified finding, implication and action | ✅ | 3 annotations, one per sheet, visible in the PDF. see `screenshots/README.md`|
| Report 1–3 pages covering data strategy, design rationale, Topic effects, insights with actions, AI comparison | ✅ | `deliverables/08_executive_report.md` — ~1,450 words (≈2.9 pages), all five topics |
| Report defines technical terms, no raw SQL or formulas, complete sentences | ✅ | Left join, row multiplication and Topic each defined on first use; no code in the report |

---

## Nothing outstanding

All 23 screenshots were captured directly from the live workspace — see
`screenshots/README.md` for an index of what each one shows.

## Submitting

Udacity accepts either upload path:

- **Public GitHub repository** —
  https://github.com/Minifigures/novatech-revenue-intelligence-dashboard
- **Zip file** — `NovaTech_Project_Submission.zip` in this folder

Rebuild the zip if you change anything:

```bash
cd "$HOME/Downloads/UofT/AWS AI:ML Scholar/Project 1" && rm -f NovaTech_Project_Submission.zip && zip -qr NovaTech_Project_Submission.zip README.md SUBMISSION_CHECKLIST.md analysis data deliverables docs screenshots -x "*.DS_Store" && echo done
```
