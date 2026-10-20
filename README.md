# Brand Weekly Review Agent

A small Claude Code workflow that turns raw Amazon Ads data into a one-page weekly review a brand CEO can act on.

Built by Soon Young Park as a working demo. All data is synthetic.

I spent 12 years at Coca-Cola and 16 years at KGC (JungKwanJang) on the brand side. This review is designed around the questions a brand CEO actually asks every week.

## Why

Partner Success teams spend hours each week pulling numbers and writing the same review. The judgment part is what matters: is a high ACoS a real loss, or is it building organic sales? This workflow does the arithmetic in Python and leaves the judgment to an agent with clear rules, so a PSM reviews and edits instead of starting from zero.

## How it works

1. `data/generate_sample.py` creates 8 weeks of SP, SB and SD data for a fictional supplement brand, with planted problems.
2. `src/metrics.py` computes ROAS, ACoS, TACoS and profit after ads, and flags targets above break-even ACoS, spend with no sales, and fast improvers. It also warns when brand-level profit after ads has fallen two weeks in a row.
3. `/weekly-review` (a Claude Code slash command in `.claude/commands/`) reads the summary and writes a one-page report with three actions, owners, expected dollar effect and a check for next week.

## Run it

```bash
pip install pandas
python data/generate_sample.py
python src/metrics.py --margin 0.35
claude            # then type: /weekly-review 0.35
```

Sample output: `reports/weekly_review_2026-10-12.md`.

## Design choices

- Numbers come from code, not from the model. The model only interprets.
- Every judgment uses break-even ACoS (the client's margin), not a generic benchmark.
- No budget cut is recommended on ACoS alone. TACoS and profit after ads are checked first.
- Ad copy suggestions never include health claims. Supplements are a regulated category.

## Next steps

- Connect the Amazon Ads API through an MCP server instead of CSV files.
- Add new-to-brand customer data to judge awareness campaigns fairly.
- Save each week's decisions to a notes vault so the team builds a shared playbook.
