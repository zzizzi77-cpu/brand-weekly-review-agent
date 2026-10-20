"""Compute weekly brand performance metrics and flag issues.

Usage:
  python src/metrics.py --margin 0.35

Reads data/ads_weekly.csv and data/sales_weekly.csv.
Writes reports/metrics_summary.json for the agent to interpret.

Definitions
  ROAS  = ad sales / ad spend
  ACoS  = ad spend / ad sales
  TACoS = ad spend / total sales
  Break-even ACoS = pre-ad profit margin
"""

import argparse
import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent


def safe_div(a, b):
    return float(a) / float(b) if b else None


def pct(x):
    return None if x is None else round(x * 100, 1)


def load():
    ads = pd.read_csv(ROOT / "data" / "ads_weekly.csv")
    sales = pd.read_csv(ROOT / "data" / "sales_weekly.csv")
    return ads, sales


def weekly_totals(ads, sales):
    spend = ads.groupby("week_start")["spend_usd"].sum()
    df = sales.set_index("week_start").join(spend.rename("spend_usd"))
    df["roas"] = df["ad_sales_usd"] / df["spend_usd"]
    df["acos"] = df["spend_usd"] / df["ad_sales_usd"]
    df["tacos"] = df["spend_usd"] / df["total_sales_usd"]
    return df.sort_index().reset_index()


def by_type(ads, week):
    w = ads[ads["week_start"] == week].groupby("campaign_type")[["spend_usd", "ad_sales_usd"]].sum()
    out = {}
    for ctype, r in w.iterrows():
        out[ctype] = {
            "spend_usd": round(r.spend_usd, 2),
            "ad_sales_usd": round(r.ad_sales_usd, 2),
            "roas": round(safe_div(r.ad_sales_usd, r.spend_usd) or 0, 2),
            "acos_pct": pct(safe_div(r.spend_usd, r.ad_sales_usd)),
        }
    return out


def flags(ads, margin, this_week, last_week):
    found = []
    cur = ads[ads["week_start"] == this_week].set_index("target")
    prev = ads[ads["week_start"] == last_week].set_index("target")
    for target, r in cur.iterrows():
        acos = safe_div(r.spend_usd, r.ad_sales_usd)
        if r.ad_sales_usd == 0 and r.spend_usd > 0:
            found.append({"type": "spend_no_sales", "target": target,
                          "campaign_type": r.campaign_type, "spend_usd": r.spend_usd})
        elif acos is not None and acos > margin:
            found.append({"type": "above_break_even", "target": target,
                          "campaign_type": r.campaign_type,
                          "acos_pct": pct(acos), "break_even_pct": pct(margin),
                          "spend_usd": r.spend_usd})
        if target in prev.index:
            p = prev.loc[target]
            p_roas = safe_div(p.ad_sales_usd, p.spend_usd)
            c_roas = safe_div(r.ad_sales_usd, r.spend_usd)
            profitable = acos is not None and acos <= margin
            if profitable and p_roas and c_roas is not None and c_roas >= p_roas * 1.25:
                found.append({"type": "improving", "target": target,
                              "campaign_type": r.campaign_type,
                              "roas_prev": round(p_roas, 2), "roas_now": round(c_roas, 2)})
    return found


def profit_after_ads(t, margin):
    return round(t["total_sales_usd"] * margin - t["spend_usd"], 2)


def profit_decline_flag(trend, margin):
    """Brand-level warning when profit after ads fell two weeks in a row.

    Expects `trend` sorted by week_start, oldest first.
    """
    if len(trend) < 3:
        return []
    p2, p1, p0 = (profit_after_ads(t, margin) for t in trend[-3:])
    if p1 < p2 and p0 < p1:
        return [{"type": "profit_decline_2w", "target": "brand_total",
                 "profit_after_ads_usd": [p2, p1, p0],
                 "weeks": [t["week_start"] for t in trend[-3:]]}]
    return []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--margin", type=float, default=0.35,
                        help="pre-ad profit margin, used as break-even ACoS")
    args = parser.parse_args()

    ads, sales = load()
    weeks = sorted(ads["week_start"].unique())
    this_week, last_week = weeks[-1], weeks[-2]
    totals = weekly_totals(ads, sales)

    trend = [{
        "week_start": r.week_start,
        "spend_usd": round(r.spend_usd, 2),
        "ad_sales_usd": round(r.ad_sales_usd, 2),
        "organic_sales_usd": round(r.organic_sales_usd, 2),
        "total_sales_usd": round(r.total_sales_usd, 2),
        "roas": round(r.roas, 2),
        "acos_pct": pct(r.acos),
        "tacos_pct": pct(r.tacos),
    } for r in totals.itertuples()]

    cur, prev = trend[-1], trend[-2]
    profit = lambda t: profit_after_ads(t, args.margin)

    summary = {
        "note": "Synthetic demo data. Not a real brand or account.",
        "this_week": this_week,
        "break_even_acos_pct": pct(args.margin),
        "headline": {
            "this_week": cur,
            "last_week": prev,
            "profit_after_ads_usd": {"this_week": profit(cur), "last_week": profit(prev)},
        },
        "by_campaign_type": by_type(ads, this_week),
        "flags": profit_decline_flag(trend, args.margin)
                 + flags(ads, args.margin, this_week, last_week),
        "trend_8w": trend,
    }

    out = ROOT / "reports" / "metrics_summary.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"Wrote {out}")
    print(f"ROAS {cur['roas']} | ACoS {cur['acos_pct']}% | TACoS {cur['tacos_pct']}% | flags {len(summary['flags'])}")


if __name__ == "__main__":
    main()
