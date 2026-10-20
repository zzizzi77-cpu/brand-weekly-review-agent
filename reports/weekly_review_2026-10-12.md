# Weekly Performance Review, week of 2026-10-12

Synthetic demo data.

Break-even ACoS for this review: **35.0%** (pre-ad margin supplied as `--margin 0.35`).

## Headline

- **Total sales $17,379.71**, down $308.42 (-1.7%) from $17,688.13. Ad sales fell $550.13 (-7.2%); organic sales rose $241.71 (+2.4%) to an eight-week high of $10,256.66. The decline is entirely an advertising decline.
- **Profit after ads $3,472.46**, down $139.79 (-3.9%) from $3,612.25. This splits into -$224.39 from advertising and +$84.60 of margin on the extra organic sales.
- **TACoS 15.0%**, up 0.4 points from 14.6%. This is the top of the eight-week range (14.1%-15.2%), not a break from it. Spend rose 1.2% while total sales fell 1.7%.

Brand-level ACoS is 36.6%, which is 1.6 points above break-even. On ad-attributed sales alone the account lost money this week. Whether it lost money overall depends on the organic halo, which the current data cannot prove.

## What changed

| Campaign type | Spend | Ad sales | ROAS | ACoS | vs break-even |
|---|---|---|---|---|---|
| SP | $1,691.59 | $3,906.23 | 2.31 | 43.3% | -8.3 pts |
| SB | $526.41 | $2,173.78 | 4.13 | 24.2% | +10.8 pts |
| SD | $392.44 | $1,043.04 | 2.66 | 37.6% | -2.6 pts |
| **Total** | **$2,610.44** | **$7,123.05** | **2.73** | **36.6%** | -1.6 pts |

Sponsored Products carries the whole problem. SP spend rose $53.83 while SP ad sales fell $816.57, taking SP from +$15.22 profit to -$324.41. Sponsored Brands moved the other way: spend down $42.90, sales up $259.25, profit up $133.63. Sponsored Display was roughly flat at a small loss.

## Issues

No `profit_decline_2w` flag this week. Profit after ads rose in the week of 2026-10-05 ($3,381.60 to $3,612.25) before falling this week, so the two-week rule did not trigger. This is a one-week decline.

Ranked by dollars lost per week, where loss = spend minus 35% margin on the ad sales it produced:

1. **energy supplement for women (SP) — losing $348.25/week, third week running.** ACoS 108.2%. This broke on 2026-09-28: spend went from about $250/week to $433, $420, $515, while orders stayed flat at 11-12. Conversion rate fell from 10.3% to 4.2%. Cumulative loss since the break is roughly $1,000. This is the single largest fixable item in the account.
2. **competitor asin B0XXXX01 (SP) — $230.16 spent, 0 orders.** Flagged as `spend_no_sales`. **This number looks wrong.** The prior seven weeks ran 6 to 10 orders on 93-201 clicks (3.3%-9.5% conversion). A clean zero on 108 clicks is more consistent with a tracking gap, a stock-out, or a lost buy box than with a genuine collapse. Do not act on it as a performance result until it is checked.
3. **hanbit red ginseng (SP, brand defense) — profit down $91.25/week.** Not flagged, because its ACoS is a healthy 13.6%. It is here because impressions fell 79% (25,417 to 5,431) while CPC rose 113% ($1.13 to $2.41) and orders fell 38 to 30. This is the most profitable target in the account and it under-delivered. Losing volume on a cheap target costs as much as overspending on an expensive one.
4. **korean red ginseng (SP) — ACoS 36.4%, losing $14.46/week.** Flagged as above break-even, but it is 1.4 points over on $366 of spend. Treat it as break-even, not as a problem. See the note below before touching it.
5. **wellness in-market audience (SD) — losing $77.23/week.** ACoS 61.5%, but improved from 77.6% last week. 83 clicks is a thin base for a decision.
6. **natural energy booster (SB) — losing $45.23/week.** ACoS 44.5%, stable in the 38%-53% band for eight weeks. Consistently below break-even, never dramatically.
7. **red ginseng extract (SB) — improving.** ROAS 4.12 to 5.40, profit up $131.04. The one clear gain this week.

**On cutting high-ACoS campaigns.** I am not recommending a cut on `korean red ginseng` or `wellness in-market audience`. Organic sales rose $241.71 this week and are at an eight-week high, and `korean red ginseng` delivered 282 of the week's clicks as the main generic head term. A halo is plausible, but nothing in this dataset proves it. Two reports would settle it: new-to-brand order share by campaign, and organic rank history for the term. The ads file has no NTB column, so the question is currently unanswerable from our side.

## Next week

1. **Cap `energy supplement for women` to $250/week and pull its search-term report.** Owner: PSM. Expected effect: weekly loss narrows from -$348 to roughly -$170, worth about **+$175/week**. The cap is a stop-loss, not a fix; the search-term report is what identifies which queries started converting at 4%. Check next week: spend at or under $250, and conversion rate on that target.
2. **Verify the zero on `competitor asin B0XXXX01` before deciding anything.** Owner: PSM. Confirm stock status, buy box ownership, and attribution for 2026-10-12. Expected effect: either about $100/week of sales reappears as a reporting correction, or we confirm a real $230/week loss and pause the target the following Monday. Check next week: the target shows a non-zero order count, or we have a documented reason it is zero.
3. **Restore brand-term delivery on `hanbit red ginseng`.** Owner: brand sets the budget, PSM sets the bids. Impressions fell 79% and CPC doubled, which points to a budget cap or a competitor bidding on the brand term. Expected effect: **+$90/week** of profit at the target's current 13.6% ACoS. Check next week: impressions back above 20,000 and CPC back under $1.50.

These three total roughly $265-$365/week of recovered profit against a $139.79 decline, so the account should clear last week's level if nothing else moves.

## Questions for the client

**1. Is 35% still the right break-even margin after Amazon referral fees and FBA?** This is the first question because every number in this report moves with it. At 35% the account cleared $3,472.46 this week and five targets are in loss. At 30% it clears $2,603.47 and six are, because `ginseng supplement` flips from +$20.34 to -$43.05 and `viewed not purchased 30d` falls to +$12.30. If the real figure is below 35%, action 1 stops being a budget cap and becomes a pause decision.

**2. Did anything change on the women's energy product in the week of 2026-09-28** — listing copy, main image, price, review count, or stock? Conversion on that target halved that week and has stayed down for three weeks while traffic kept rising, and that pattern usually comes from the product page rather than from the campaign.

## Data notes

- The 35% margin is an input supplied at run time, not a measured figure. See question 1; it is unconfirmed, and it sets every profit number here.
- The ads file has no new-to-brand column, so halo and acquisition arguments cannot be tested from this data.
- `competitor asin B0XXXX01` at 0 orders is treated as suspect, not as fact. See Issue 2.
