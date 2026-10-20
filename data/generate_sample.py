"""Generate synthetic Amazon Ads data for a fictional Korean red ginseng brand.

All numbers are invented for demonstration. No real brand or account data is used.

Output:
  data/ads_weekly.csv     keyword-level weekly ad performance (SP, SB, SD)
  data/sales_weekly.csv   weekly total and organic sales
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(42)

OUT = Path(__file__).resolve().parent
WEEKS = 8
START = date(2026, 8, 24)  # Monday

# (campaign_type, campaign, target, base_spend_usd, base_roas)
TARGETS = [
    ("SP", "SP_Brand", "hanbit red ginseng", 180, 7.5),
    ("SP", "SP_Generic", "korean red ginseng", 420, 3.1),
    ("SP", "SP_Generic", "ginseng supplement", 380, 2.6),
    ("SP", "SP_Generic", "energy supplement for women", 260, 1.9),
    ("SP", "SP_Competitor", "competitor asin B0XXXX01", 220, 1.6),
    ("SB", "SB_Brand_Video", "red ginseng extract", 300, 3.4),
    ("SB", "SB_Category", "natural energy booster", 240, 2.2),
    ("SD", "SD_Retargeting", "viewed not purchased 30d", 200, 4.0),
    ("SD", "SD_Audience", "wellness in-market audience", 180, 1.4),
]

AVG_PRICE = 39.0  # USD per unit


def ads_rows():
    rows = []
    for w in range(WEEKS):
        week_start = START + timedelta(weeks=w)
        for ctype, campaign, target, base_spend, base_roas in TARGETS:
            spend = base_spend * random.uniform(0.85, 1.15)
            roas = base_roas * random.uniform(0.8, 1.2)

            # Planted issues for the agent to find
            if target == "energy supplement for women" and w >= 5:
                spend *= 1.8   # budget creep
                roas *= 0.45   # efficiency collapse
            if target == "competitor asin B0XXXX01" and w == WEEKS - 1:
                roas = 0.0     # spend with no sales
            if target == "red ginseng extract" and w >= 6:
                roas *= 1.35   # video creative working

            sales = spend * roas
            cpc = random.uniform(0.9, 2.4)
            clicks = max(1, round(spend / cpc))
            impressions = round(clicks / random.uniform(0.004, 0.012))
            orders = round(sales / AVG_PRICE)
            rows.append({
                "week_start": week_start.isoformat(),
                "campaign_type": ctype,
                "campaign": campaign,
                "target": target,
                "impressions": impressions,
                "clicks": clicks,
                "spend_usd": round(spend, 2),
                "orders": orders,
                "ad_sales_usd": round(sales, 2),
            })
    return rows


def sales_rows(ads):
    rows = []
    organic = 9000.0
    for w in range(WEEKS):
        week_start = (START + timedelta(weeks=w)).isoformat()
        ad_sales = sum(r["ad_sales_usd"] for r in ads if r["week_start"] == week_start)
        organic *= random.uniform(0.98, 1.06)
        rows.append({
            "week_start": week_start,
            "ad_sales_usd": round(ad_sales, 2),
            "organic_sales_usd": round(organic, 2),
            "total_sales_usd": round(ad_sales + organic, 2),
        })
    return rows


def write(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    ads = ads_rows()
    write(OUT / "ads_weekly.csv", ads)
    write(OUT / "sales_weekly.csv", sales_rows(ads))
    print(f"Wrote {len(ads)} ad rows and {WEEKS} sales rows to {OUT}")
