#!/usr/bin/env python3
"""
NovaTech Revenue Intelligence — ground-truth analytics.

Computes every figure quoted in the verification log, Q exploration log,
dashboard annotations and the executive report, straight from the three
starter CSVs. Pure standard library so it runs on stock macOS Python.

Usage:  python3 analysis/ground_truth.py
Output: analysis/ground_truth.json  +  analysis/ground_truth.md
"""

import csv
import json
import os
import statistics
from collections import Counter, defaultdict
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")

CRM_F = os.path.join(DATA, "novatech_crm_deals.csv")
MKT_F = os.path.join(DATA, "novatech_marketing_campaigns.csv")
SUP_F = os.path.join(DATA, "novatech_support_tickets.csv")


def load(path):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def f(v):
    """float or None for blank/invalid."""
    if v is None or v.strip() == "":
        return None
    try:
        return float(v)
    except ValueError:
        return None


def i(v):
    x = f(v)
    return None if x is None else int(x)


def d(v):
    """Parse YYYY-MM-DD or YYYY-MM-DD HH:MM:SS."""
    if v is None or v.strip() == "":
        return None
    v = v.strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            continue
    return None


def pct(n, total, nd=1):
    return round(100.0 * n / total, nd) if total else 0.0


def money(x):
    return round(x, 2)


def top_n(counter, n=10):
    return [{"key": k, "value": v} for k, v in counter.most_common(n)]


crm = load(CRM_F)
mkt = load(MKT_F)
sup = load(SUP_F)

R = {}

# ---------------------------------------------------------------- CRM ------
crm_accounts = {r["account_id"] for r in crm}
won = [r for r in crm if r["deal_stage"] == "Won"]
lost = [r for r in crm if r["deal_stage"] == "Lost"]
won_rev = sum(f(r["deal_value"]) or 0 for r in won)
all_rev = sum(f(r["deal_value"]) or 0 for r in crm)

days_to_close = []
for r in crm:
    a, b = d(r["deal_created_date"]), d(r["deal_closed_date"])
    if a and b:
        days_to_close.append((b - a).days)

dtc_won, dtc_lost = [], []
for r in crm:
    a, b = d(r["deal_created_date"]), d(r["deal_closed_date"])
    if a and b:
        (dtc_won if r["deal_stage"] == "Won" else dtc_lost).append((b - a).days)

# win rate / revenue cuts
def cut(rows, key, value_fn=None):
    agg = defaultdict(lambda: {"deals": 0, "won": 0, "revenue": 0.0})
    for r in rows:
        k = r[key]
        agg[k]["deals"] += 1
        if r["deal_stage"] == "Won":
            agg[k]["won"] += 1
        agg[k]["revenue"] += f(r["deal_value"]) or 0
    out = {}
    for k, v in agg.items():
        out[k] = {
            "deals": v["deals"],
            "won": v["won"],
            "win_rate_pct": pct(v["won"], v["deals"]),
            "revenue": money(v["revenue"]),
            "avg_deal_value_won": money(v["revenue"] / v["won"]) if v["won"] else 0.0,
        }
    return dict(sorted(out.items(), key=lambda kv: -kv[1]["revenue"]))


crm_dates = [d(r["deal_closed_date"]) for r in crm if d(r["deal_closed_date"])]
crm_created = [d(r["deal_created_date"]) for r in crm if d(r["deal_created_date"])]

R["crm"] = {
    "row_count": len(crm),
    "column_count": len(crm[0]),
    "unique_accounts": len(crm_accounts),
    "unique_companies": len({r["company_name"] for r in crm}),
    "unique_opportunities": len({r["opportunity_id"] for r in crm}),
    "unique_sales_reps": len({r["sales_rep"] for r in crm}),
    "won_count": len(won),
    "lost_count": len(lost),
    "win_rate_pct": pct(len(won), len(crm)),
    "total_revenue_won": money(won_rev),
    "total_revenue_all_rows": money(all_rev),
    "avg_deal_value_won": money(won_rev / len(won)) if won else 0,
    "median_deal_value_won": money(statistics.median([f(r["deal_value"]) for r in won])),
    "max_deal_value": money(max(f(r["deal_value"]) or 0 for r in crm)),
    "min_deal_value": money(min(f(r["deal_value"]) or 0 for r in crm)),
    "lost_deals_with_zero_value": sum(1 for r in lost if (f(r["deal_value"]) or 0) == 0),
    "loss_reason_nulls": sum(1 for r in crm if not r["loss_reason"].strip()),
    "loss_reasons": dict(Counter(r["loss_reason"] for r in lost).most_common()),
    "avg_days_to_close": round(statistics.mean(days_to_close), 1),
    "median_days_to_close": statistics.median(days_to_close),
    "avg_days_to_close_won": round(statistics.mean(dtc_won), 1),
    "avg_days_to_close_lost": round(statistics.mean(dtc_lost), 1),
    "min_days_to_close": min(days_to_close),
    "max_days_to_close": max(days_to_close),
    "closed_date_min": min(crm_dates).strftime("%Y-%m-%d"),
    "closed_date_max": max(crm_dates).strftime("%Y-%m-%d"),
    "created_date_min": min(crm_created).strftime("%Y-%m-%d"),
    "created_date_max": max(crm_created).strftime("%Y-%m-%d"),
    "by_region": cut(crm, "sales_region"),
    "by_product_category": cut(crm, "product_category"),
    "by_product": cut(crm, "product_name"),
    "by_size_tier": cut(crm, "company_size_tier"),
    "by_industry": cut(crm, "industry"),
    "by_manager": cut(crm, "sales_manager"),
    "industries": len({r["industry"] for r in crm}),
}

# top reps by revenue
rep_cut = cut(crm, "sales_rep")
R["crm"]["top_5_reps_by_revenue"] = list(rep_cut.items())[:5]
R["crm"]["bottom_5_reps_by_win_rate"] = sorted(
    [(k, v) for k, v in rep_cut.items() if v["deals"] >= 10],
    key=lambda kv: kv[1]["win_rate_pct"],
)[:5]

# days-to-close trend by close year
dtc_by_year = defaultdict(list)
rev_by_year = defaultdict(float)
won_by_year, deals_by_year = Counter(), Counter()
for r in crm:
    a, b = d(r["deal_created_date"]), d(r["deal_closed_date"])
    if a and b:
        dtc_by_year[b.year].append((b - a).days)
        deals_by_year[b.year] += 1
        rev_by_year[b.year] += f(r["deal_value"]) or 0
        if r["deal_stage"] == "Won":
            won_by_year[b.year] += 1
R["crm"]["by_close_year"] = {
    str(y): {
        "deals": deals_by_year[y],
        "won": won_by_year[y],
        "win_rate_pct": pct(won_by_year[y], deals_by_year[y]),
        "revenue": money(rev_by_year[y]),
        "avg_days_to_close": round(statistics.mean(v), 1),
    }
    for y, v in sorted(dtc_by_year.items())
}

# ---------------------------------------------------------- MARKETING ------
mkt_accounts = {r["account_id"] for r in mkt}
mkt_orphans = mkt_accounts - crm_accounts
mkt_orphan_rows = sum(1 for r in mkt if r["account_id"] in mkt_orphans)
responded = [r for r in mkt if i(r["campaign_response"]) == 1]
total_spend = sum(f(r["campaign_spend"]) or 0 for r in mkt)
total_attr = sum(f(r["revenue_attributed"]) or 0 for r in mkt)

def mkt_cut(key):
    agg = defaultdict(lambda: {"leads": 0, "responded": 0, "spend": 0.0, "revenue": 0.0})
    for r in mkt:
        k = r[key]
        agg[k]["leads"] += 1
        agg[k]["responded"] += 1 if i(r["campaign_response"]) == 1 else 0
        agg[k]["spend"] += f(r["campaign_spend"]) or 0
        agg[k]["revenue"] += f(r["revenue_attributed"]) or 0
    out = {}
    for k, v in agg.items():
        roi = ((v["revenue"] - v["spend"]) / v["spend"] * 100) if v["spend"] else 0
        out[k] = {
            "leads": v["leads"],
            "responded": v["responded"],
            "response_rate_pct": pct(v["responded"], v["leads"]),
            "spend": money(v["spend"]),
            "revenue_attributed": money(v["revenue"]),
            "net": money(v["revenue"] - v["spend"]),
            "roi_pct": round(roi, 1),
            "cost_per_response": money(v["spend"] / v["responded"]) if v["responded"] else None,
        }
    return dict(sorted(out.items(), key=lambda kv: -kv[1]["roi_pct"]))


funnel = Counter(r["funnel_stage"] for r in mkt)
FUNNEL_ORDER = ["Prospect", "Lead", "Qualified Lead", "Opportunity", "Closed Won"]
mkt_dates = [d(r["campaign_date"]) for r in mkt if d(r["campaign_date"])]

# funnel stage distribution by channel (which channel converts best to Closed Won)
chan_funnel = defaultdict(Counter)
for r in mkt:
    chan_funnel[r["campaign_channel"]][r["funnel_stage"]] += 1
chan_conv = {}
for ch, c in chan_funnel.items():
    tot = sum(c.values())
    chan_conv[ch] = {
        "leads": tot,
        "closed_won": c.get("Closed Won", 0),
        "closed_won_rate_pct": pct(c.get("Closed Won", 0), tot),
        "stages": dict(c),
    }
chan_conv = dict(sorted(chan_conv.items(), key=lambda kv: -kv[1]["closed_won_rate_pct"]))

R["marketing"] = {
    "row_count": len(mkt),
    "column_count": len(mkt[0]),
    "unique_leads": len({r["lead_id"] for r in mkt}),
    "unique_accounts": len(mkt_accounts),
    "orphan_account_ids": sorted(mkt_orphans),
    "orphan_account_count": len(mkt_orphans),
    "orphan_rows": mkt_orphan_rows,
    "orphan_rows_pct": pct(mkt_orphan_rows, len(mkt)),
    "annual_income_nulls": sum(1 for r in mkt if f(r["annual_income"]) is None),
    "annual_income_null_pct": pct(sum(1 for r in mkt if f(r["annual_income"]) is None), len(mkt)),
    "responded_count": len(responded),
    "response_rate_pct": pct(len(responded), len(mkt)),
    "total_campaign_spend": money(total_spend),
    "total_revenue_attributed": money(total_attr),
    "overall_net": money(total_attr - total_spend),
    "overall_roi_pct": round((total_attr - total_spend) / total_spend * 100, 1),
    "campaign_date_min": min(mkt_dates).strftime("%Y-%m-%d"),
    "campaign_date_max": max(mkt_dates).strftime("%Y-%m-%d"),
    "campaigns": len({r["campaign_name"] for r in mkt}),
    "channels": len({r["campaign_channel"] for r in mkt}),
    "funnel_stage_counts": {k: funnel[k] for k in FUNNEL_ORDER},
    "funnel_stage_pct": {k: pct(funnel[k], len(mkt)) for k in FUNNEL_ORDER},
    "by_campaign": mkt_cut("campaign_name"),
    "by_channel": mkt_cut("campaign_channel"),
    "by_segment": mkt_cut("customer_segment"),
    "by_market_code": mkt_cut("Mkt_Src_Cd"),
    "channel_conversion": chan_conv,
    "complaint_flag_count": sum(1 for r in mkt if i(r["complaint_flag"]) == 1),
}
R["marketing"]["campaigns_losing_money"] = {
    k: v for k, v in R["marketing"]["by_campaign"].items() if v["net"] < 0
}
R["marketing"]["channels_losing_money"] = {
    k: v for k, v in R["marketing"]["by_channel"].items() if v["net"] < 0
}

# ------------------------------------------------------------ SUPPORT ------
sup_accounts = {r["account_id"] for r in sup}
sup_orphans = sup_accounts - crm_accounts
sup_orphan_rows = sum(1 for r in sup if r["account_id"] in sup_orphans)

res_hours = []
res_by_priority = defaultdict(list)
res_by_area = defaultdict(list)
unresolved = 0
for r in sup:
    a, b = d(r["ticket_created_date"]), d(r["ticket_resolved_date"])
    if b is None:
        unresolved += 1
        continue
    if a:
        h = (b - a).total_seconds() / 3600.0
        res_hours.append(h)
        res_by_priority[r["priority"]].append(h)
        res_by_area[r["product_area"]].append(h)

sup_dates = [d(r["ticket_created_date"]) for r in sup if d(r["ticket_created_date"])]

tickets_by_account = Counter(r["account_id"] for r in sup)
sentiment = Counter(r["customer_sentiment"] for r in sup)
priority = Counter(r["priority"] for r in sup)

area_stats = {}
for area, hrs in res_by_area.items():
    area_stats[area] = {
        "tickets": sum(1 for r in sup if r["product_area"] == area),
        "resolved": len(hrs),
        "avg_resolution_hours": round(statistics.mean(hrs), 2),
        "median_resolution_hours": round(statistics.median(hrs), 2),
    }
area_stats = dict(sorted(area_stats.items(), key=lambda kv: -kv[1]["avg_resolution_hours"]))

prio_stats = {}
for p in ["critical", "high", "medium", "low"]:
    hrs = res_by_priority.get(p, [])
    prio_stats[p] = {
        "tickets": priority[p],
        "resolved": len(hrs),
        "avg_resolution_hours": round(statistics.mean(hrs), 2) if hrs else None,
        "median_resolution_hours": round(statistics.median(hrs), 2) if hrs else None,
        "avg_resolution_days": round(statistics.mean(hrs) / 24, 2) if hrs else None,
    }

R["support"] = {
    "row_count": len(sup),
    "column_count": len(sup[0]),
    "unique_tickets": len({r["ticket_id"] for r in sup}),
    "unique_accounts": len(sup_accounts),
    "orphan_account_ids": sorted(sup_orphans),
    "orphan_account_count": len(sup_orphans),
    "orphan_rows": sup_orphan_rows,
    "orphan_rows_pct": pct(sup_orphan_rows, len(sup)),
    "unresolved_tickets": unresolved,
    "unresolved_pct": pct(unresolved, len(sup)),
    "avg_resolution_hours": round(statistics.mean(res_hours), 2),
    "median_resolution_hours": round(statistics.median(res_hours), 2),
    "max_resolution_hours": round(max(res_hours), 2),
    "ticket_date_min": min(sup_dates).strftime("%Y-%m-%d"),
    "ticket_date_max": max(sup_dates).strftime("%Y-%m-%d"),
    "priority_counts": dict(priority.most_common()),
    "priority_stats": prio_stats,
    "product_area_stats": area_stats,
    "product_area_counts": dict(Counter(r["product_area"] for r in sup).most_common()),
    "sentiment_counts": dict(sentiment.most_common()),
    "sentiment_pct": {k: pct(v, len(sup)) for k, v in sentiment.most_common()},
    "contact_channel_counts": dict(Counter(r["contact_channel"] for r in sup).most_common()),
    "customer_tier_counts": dict(Counter(r["customer_tier"] for r in sup).most_common()),
    "region_counts": dict(Counter(r["region"] for r in sup).most_common()),
    "security_incidents": sum(1 for r in sup if i(r["security_incident"]) == 1),
    "data_loss_events": sum(1 for r in sup if i(r["data_loss"]) == 1),
    "payment_impact_tickets": sum(1 for r in sup if i(r["payment_impact"]) == 1),
    "total_downtime_minutes": sum(i(r["downtime_minutes"]) or 0 for r in sup),
    "total_users_affected": sum(i(r["users_affected"]) or 0 for r in sup),
    "top_10_accounts_by_tickets": top_n(tickets_by_account, 10),
}
R["support"]["critical_vs_low_gap_hours"] = round(
    prio_stats["critical"]["avg_resolution_hours"] - prio_stats["low"]["avg_resolution_hours"], 2
)

# --------------------------------------------------------- CROSS-DOMAIN ----
# Account-level 360 rollup (CRM anchor)
acct_rev = defaultdict(float)
acct_deals = Counter()
acct_won = Counter()
acct_company = {}
acct_tier = {}
acct_industry = {}
for r in crm:
    a = r["account_id"]
    acct_rev[a] += f(r["deal_value"]) or 0
    acct_deals[a] += 1
    if r["deal_stage"] == "Won":
        acct_won[a] += 1
    acct_company[a] = r["company_name"]
    acct_tier[a] = r["company_size_tier"]
    acct_industry[a] = r["industry"]

acct_neg = Counter()
acct_tickets = Counter()
acct_crit = Counter()
acct_downtime = defaultdict(int)
for r in sup:
    a = r["account_id"]
    acct_tickets[a] += 1
    if r["customer_sentiment"] == "negative":
        acct_neg[a] += 1
    if r["priority"] in ("critical", "high"):
        acct_crit[a] += 1
    acct_downtime[a] += i(r["downtime_minutes"]) or 0

acct_leads = Counter()
acct_spend = defaultdict(float)
for r in mkt:
    acct_leads[r["account_id"]] += 1
    acct_spend[r["account_id"]] += f(r["campaign_spend"]) or 0

account_360 = []
for a in sorted(crm_accounts):
    tickets = acct_tickets.get(a, 0)
    neg = acct_neg.get(a, 0)
    account_360.append({
        "account_id": a,
        "company_name": acct_company[a],
        "industry": acct_industry[a],
        "size_tier": acct_tier[a],
        "deals": acct_deals[a],
        "won": acct_won[a],
        "win_rate_pct": pct(acct_won[a], acct_deals[a]),
        "revenue": money(acct_rev[a]),
        "leads": acct_leads.get(a, 0),
        "marketing_spend": money(acct_spend.get(a, 0.0)),
        "tickets": tickets,
        "critical_high_tickets": acct_crit.get(a, 0),
        "negative_tickets": neg,
        "negative_pct": pct(neg, tickets) if tickets else 0.0,
        "downtime_minutes": acct_downtime.get(a, 0),
    })

# Risk definition: above-median revenue AND above-median tickets AND >=30% negative sentiment
med_rev = statistics.median([a["revenue"] for a in account_360])
med_tix = statistics.median([a["tickets"] for a in account_360])
at_risk = [
    a for a in account_360
    if a["revenue"] > med_rev and a["tickets"] > med_tix and a["negative_pct"] >= 30.0
]
at_risk.sort(key=lambda a: -a["revenue"])

top_rev_accounts = sorted(account_360, key=lambda a: -a["revenue"])[:10]
top_tix_accounts = sorted(account_360, key=lambda a: -a["tickets"])[:10]
overlap = {a["account_id"] for a in top_rev_accounts} & {a["account_id"] for a in top_tix_accounts}

# correlation between revenue and ticket volume across accounts
rev_series = [a["revenue"] for a in account_360]
tix_series = [a["tickets"] for a in account_360]
try:
    corr = round(statistics.correlation(rev_series, tix_series), 3)
except AttributeError:  # py<3.10
    mx, my = statistics.mean(rev_series), statistics.mean(tix_series)
    num = sum((x - mx) * (y - my) for x, y in zip(rev_series, tix_series))
    den = (sum((x - mx) ** 2 for x in rev_series) * sum((y - my) ** 2 for y in tix_series)) ** 0.5
    corr = round(num / den, 3) if den else None

# Exact 3-way join fan-out (CRM anchor, LEFT JOIN marketing, LEFT JOIN support)
rows_crm_sup = sum(acct_deals[a] * max(acct_tickets.get(a, 0), 1) for a in crm_accounts)
rows_crm_mkt = sum(acct_deals[a] * max(acct_leads.get(a, 0), 1) for a in crm_accounts)
rows_3way = sum(
    acct_deals[a] * max(acct_leads.get(a, 0), 1) * max(acct_tickets.get(a, 0), 1)
    for a in crm_accounts
)

R["cross_domain"] = {
    "accounts_in_crm": len(crm_accounts),
    "accounts_in_marketing": len(mkt_accounts),
    "accounts_in_support": len(sup_accounts),
    "accounts_in_all_three": len(crm_accounts & mkt_accounts & sup_accounts),
    "orphans_all": sorted((mkt_accounts | sup_accounts) - crm_accounts),
    "median_account_revenue": money(med_rev),
    "median_account_tickets": med_tix,
    "revenue_ticket_correlation": corr,
    "at_risk_accounts": at_risk,
    "at_risk_count": len(at_risk),
    "at_risk_revenue": money(sum(a["revenue"] for a in at_risk)),
    "at_risk_revenue_pct_of_total": pct(sum(a["revenue"] for a in at_risk), won_rev),
    "top_10_accounts_by_revenue": top_rev_accounts,
    "top_10_accounts_by_tickets": top_tix_accounts,
    "overlap_top10_rev_and_tickets": sorted(overlap),
    "overlap_count": len(overlap),
    "join_row_counts": {
        "crm_only": len(crm),
        "crm_left_join_support": rows_crm_sup,
        "crm_left_join_marketing": rows_crm_mkt,
        "crm_left_join_both_3way": rows_3way,
        "fanout_multiple_vs_crm": round(rows_3way / len(crm), 1),
    },
    "account_360": account_360,
}

# avg deal size for accounts with >3 tickets in last 30 days (per-ticket flag)
accts_high_recent = {r["account_id"] for r in sup if (i(r["tickets_last_30_days"]) or 0) > 3}
hv = [f(r["deal_value"]) or 0 for r in won if r["account_id"] in accts_high_recent]
lv = [f(r["deal_value"]) or 0 for r in won if r["account_id"] not in accts_high_recent]
R["cross_domain"]["high_recent_ticket_accounts"] = {
    "account_count": len(accts_high_recent & crm_accounts),
    "avg_won_deal_value": money(statistics.mean(hv)) if hv else None,
    "avg_won_deal_value_others": money(statistics.mean(lv)) if lv else None,
    "won_deals": len(hv),
}

# ------------------------------------------------------------- OUTPUT ------
with open(os.path.join(ROOT, "analysis", "ground_truth.json"), "w") as fh:
    json.dump(R, fh, indent=2)


def md_table(rows, headers):
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)


L = []
L.append("# NovaTech Ground-Truth Figures\n")
L.append("Computed directly from the three starter CSVs by `analysis/ground_truth.py`.\n")
L.append("Every number quoted in the verification log, Q exploration log, dashboard\n"
         "annotations and executive report traces back to this file.\n")

c = R["crm"]
L.append("\n## 1. CRM Deals\n")
L.append(md_table([
    ["Rows / columns", f'{c["row_count"]} / {c["column_count"]}'],
    ["Unique accounts / companies", f'{c["unique_accounts"]} / {c["unique_companies"]}'],
    ["Won / Lost", f'{c["won_count"]} / {c["lost_count"]}'],
    ["Win rate", f'{c["win_rate_pct"]}%'],
    ["Total won revenue", f'${c["total_revenue_won"]:,.2f}'],
    ["Average won deal value", f'${c["avg_deal_value_won"]:,.2f}'],
    ["Median won deal value", f'${c["median_deal_value_won"]:,.2f}'],
    ["Avg days to close (all)", c["avg_days_to_close"]],
    ["Avg days to close (won / lost)", f'{c["avg_days_to_close_won"]} / {c["avg_days_to_close_lost"]}'],
    ["Closed date range", f'{c["closed_date_min"]} → {c["closed_date_max"]}'],
    ["loss_reason nulls", c["loss_reason_nulls"]],
], ["Metric", "Value"]))

L.append("\n### Win rate & revenue by region\n")
L.append(md_table(
    [[k, v["deals"], v["won"], f'{v["win_rate_pct"]}%', f'${v["revenue"]:,.2f}']
     for k, v in c["by_region"].items()],
    ["Region", "Deals", "Won", "Win rate", "Revenue"]))

L.append("\n### Win rate & revenue by company size tier\n")
L.append(md_table(
    [[k, v["deals"], v["won"], f'{v["win_rate_pct"]}%', f'${v["revenue"]:,.2f}',
      f'${v["avg_deal_value_won"]:,.2f}']
     for k, v in c["by_size_tier"].items()],
    ["Size tier", "Deals", "Won", "Win rate", "Revenue", "Avg won deal"]))

L.append("\n### Revenue by product\n")
L.append(md_table(
    [[k, v["deals"], f'{v["win_rate_pct"]}%', f'${v["revenue"]:,.2f}', f'${v["avg_deal_value_won"]:,.2f}']
     for k, v in c["by_product"].items()],
    ["Product", "Deals", "Win rate", "Revenue", "Avg won deal"]))

L.append("\n### Loss reasons\n")
L.append(md_table([[k, v, f'{pct(v, c["lost_count"])}%'] for k, v in c["loss_reasons"].items()],
                  ["Loss reason", "Deals", "% of losses"]))

L.append("\n### Trend by close year\n")
L.append(md_table(
    [[y, v["deals"], f'{v["win_rate_pct"]}%', f'${v["revenue"]:,.2f}', v["avg_days_to_close"]]
     for y, v in c["by_close_year"].items()],
    ["Year", "Deals", "Win rate", "Revenue", "Avg days to close"]))

m = R["marketing"]
L.append("\n## 2. Marketing Campaigns\n")
L.append(md_table([
    ["Rows / columns", f'{m["row_count"]} / {m["column_count"]}'],
    ["Unique leads", m["unique_leads"]],
    ["Unique accounts", m["unique_accounts"]],
    ["Orphan accounts / rows", f'{m["orphan_account_count"]} / {m["orphan_rows"]} ({m["orphan_rows_pct"]}%)'],
    ["annual_income nulls", f'{m["annual_income_nulls"]} ({m["annual_income_null_pct"]}%)'],
    ["Responded", f'{m["responded_count"]} ({m["response_rate_pct"]}%)'],
    ["Total campaign spend", f'${m["total_campaign_spend"]:,.2f}'],
    ["Total revenue attributed", f'${m["total_revenue_attributed"]:,.2f}'],
    ["Net", f'${m["overall_net"]:,.2f}'],
    ["Overall ROI", f'{m["overall_roi_pct"]}%'],
    ["Campaign date range", f'{m["campaign_date_min"]} → {m["campaign_date_max"]}'],
], ["Metric", "Value"]))

L.append("\n### Funnel stage distribution\n")
L.append(md_table([[k, v, f'{m["funnel_stage_pct"][k]}%'] for k, v in m["funnel_stage_counts"].items()],
                  ["Funnel stage", "Leads", "% of leads"]))

L.append("\n### Campaign performance (sorted by ROI)\n")
L.append(md_table(
    [[k, v["leads"], f'{v["response_rate_pct"]}%', f'${v["spend"]:,.2f}',
      f'${v["revenue_attributed"]:,.2f}', f'${v["net"]:,.2f}', f'{v["roi_pct"]}%']
     for k, v in m["by_campaign"].items()],
    ["Campaign", "Leads", "Response rate", "Spend", "Revenue attributed", "Net", "ROI"]))

L.append("\n### Channel performance (sorted by ROI)\n")
L.append(md_table(
    [[k, v["leads"], f'{v["response_rate_pct"]}%', f'${v["spend"]:,.2f}',
      f'${v["revenue_attributed"]:,.2f}', f'${v["net"]:,.2f}', f'{v["roi_pct"]}%']
     for k, v in m["by_channel"].items()],
    ["Channel", "Leads", "Response rate", "Spend", "Revenue attributed", "Net", "ROI"]))

L.append("\n### Channel → Closed Won conversion\n")
L.append(md_table(
    [[k, v["leads"], v["closed_won"], f'{v["closed_won_rate_pct"]}%']
     for k, v in m["channel_conversion"].items()],
    ["Channel", "Leads", "Closed Won", "Closed-Won rate"]))

s = R["support"]
L.append("\n## 3. Support Tickets\n")
L.append(md_table([
    ["Rows / columns", f'{s["row_count"]} / {s["column_count"]}'],
    ["Unique tickets", s["unique_tickets"]],
    ["Unique accounts", s["unique_accounts"]],
    ["Orphan accounts / rows", f'{s["orphan_account_count"]} / {s["orphan_rows"]} ({s["orphan_rows_pct"]}%)'],
    ["Unresolved tickets", f'{s["unresolved_tickets"]} ({s["unresolved_pct"]}%)'],
    ["Avg resolution", f'{s["avg_resolution_hours"]} h'],
    ["Median resolution", f'{s["median_resolution_hours"]} h'],
    ["Ticket date range", f'{s["ticket_date_min"]} → {s["ticket_date_max"]}'],
    ["Security incidents", s["security_incidents"]],
    ["Data-loss events", s["data_loss_events"]],
    ["Total downtime (min)", f'{s["total_downtime_minutes"]:,}'],
], ["Metric", "Value"]))

L.append("\n### Resolution time by priority\n")
L.append(md_table(
    [[k, v["tickets"], v["resolved"], v["avg_resolution_hours"], v["avg_resolution_days"]]
     for k, v in s["priority_stats"].items()],
    ["Priority", "Tickets", "Resolved", "Avg hours", "Avg days"]))

L.append("\n### Product area load & resolution\n")
L.append(md_table(
    [[k, v["tickets"], v["avg_resolution_hours"]] for k, v in s["product_area_stats"].items()],
    ["Product area", "Tickets", "Avg resolution (h)"]))

L.append("\n### Sentiment\n")
L.append(md_table([[k, v, f'{s["sentiment_pct"][k]}%'] for k, v in s["sentiment_counts"].items()],
                  ["Sentiment", "Tickets", "%"]))

L.append("\n### Top 10 accounts by ticket volume\n")
L.append(md_table([[r["key"], r["value"]] for r in s["top_10_accounts_by_tickets"]],
                  ["Account", "Tickets"]))

x = R["cross_domain"]
L.append("\n## 4. Cross-Domain (unified)\n")
L.append(md_table([
    ["Accounts in CRM / Marketing / Support",
     f'{x["accounts_in_crm"]} / {x["accounts_in_marketing"]} / {x["accounts_in_support"]}'],
    ["Accounts in all three", x["accounts_in_all_three"]],
    ["Orphan account IDs", ", ".join(x["orphans_all"])],
    ["Revenue ↔ ticket-volume correlation", x["revenue_ticket_correlation"]],
    ["At-risk accounts", x["at_risk_count"]],
    ["Revenue at risk", f'${x["at_risk_revenue"]:,.2f} ({x["at_risk_revenue_pct_of_total"]}% of won revenue)'],
    ["Top-10 revenue ∩ top-10 tickets", f'{x["overlap_count"]} accounts'],
], ["Metric", "Value"]))

j = x["join_row_counts"]
L.append("\n### Join row-count arithmetic (fan-out)\n")
L.append(md_table([
    ["CRM only (anchor)", f'{j["crm_only"]:,}'],
    ["CRM ⟕ Support", f'{j["crm_left_join_support"]:,}'],
    ["CRM ⟕ Marketing", f'{j["crm_left_join_marketing"]:,}'],
    ["CRM ⟕ Marketing ⟕ Support (3-way)", f'{j["crm_left_join_both_3way"]:,}'],
    ["Fan-out multiple vs CRM", f'{j["fanout_multiple_vs_crm"]}×'],
], ["Join", "Rows"]))

L.append("\n### At-risk accounts (above-median revenue + above-median tickets + ≥30% negative)\n")
L.append(md_table(
    [[a["account_id"], a["company_name"], a["size_tier"], f'${a["revenue"]:,.2f}',
      a["tickets"], a["negative_tickets"], f'{a["negative_pct"]}%', a["critical_high_tickets"]]
     for a in x["at_risk_accounts"]],
    ["Account", "Company", "Tier", "Revenue", "Tickets", "Negative", "Negative %", "Crit/High"]))

L.append("\n### Top 10 accounts by revenue\n")
L.append(md_table(
    [[a["account_id"], a["company_name"], f'${a["revenue"]:,.2f}', a["tickets"], f'{a["negative_pct"]}%']
     for a in x["top_10_accounts_by_revenue"]],
    ["Account", "Company", "Revenue", "Tickets", "Negative %"]))

h = x["high_recent_ticket_accounts"]
L.append("\n### Accounts with >3 tickets in trailing 30 days\n")
L.append(md_table([
    ["Accounts (also in CRM)", h["account_count"]],
    ["Avg won deal value — those accounts", f'${h["avg_won_deal_value"]:,.2f}'],
    ["Avg won deal value — all other accounts", f'${h["avg_won_deal_value_others"]:,.2f}'],
], ["Metric", "Value"]))

with open(os.path.join(ROOT, "analysis", "ground_truth.md"), "w") as fh:
    fh.write("\n".join(L) + "\n")

print("CRM rows:", R["crm"]["row_count"], "| MKT rows:", R["marketing"]["row_count"],
      "| SUP rows:", R["support"]["row_count"])
print("Win rate:", R["crm"]["win_rate_pct"], "% | Won revenue: $", R["crm"]["total_revenue_won"])
print("3-way join rows:", f'{j["crm_left_join_both_3way"]:,}', f'({j["fanout_multiple_vs_crm"]}x)')
print("At-risk accounts:", x["at_risk_count"])
print("Wrote analysis/ground_truth.json + analysis/ground_truth.md")
