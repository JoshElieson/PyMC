"""Generate small synthetic datasets used to probe Daimon's charting behaviour.

Run:  python probes/make_probe_data.py
Writes CSVs into probes/data/. Seeded, so output is reproducible.

Each dataset is designed to expose a specific visual-communication weakness:
  - channel_spend.csv   -> does Daimon show uncertainty on channel effects, or just bars of point estimates?
  - monthly_revenue.csv -> does a forecast get a fan chart with credible bands, or a single line?
  - ab_test.csv         -> does the comparison show the posterior difference, or two bars with no interval?
  - regional_sales.csv  -> with 12 groups, does the hierarchical result get a readable forest plot or a crammed grid?
"""
from pathlib import Path

import numpy as np
import pandas as pd

rng = np.random.default_rng(20261010)
out = Path(__file__).parent / "data"
out.mkdir(exist_ok=True)

# 1. Marketing channel spend vs revenue, 78 weeks. True effects: search > social > display ~ 0.
weeks = pd.date_range("2025-01-06", periods=78, freq="W-MON")
search = rng.gamma(4, 2500, len(weeks))
social = rng.gamma(3, 2000, len(weeks))
display = rng.gamma(2, 1500, len(weeks))
revenue = 40_000 + 3.2 * search + 1.4 * social + 0.1 * display + rng.normal(0, 9000, len(weeks))
pd.DataFrame({"week": weeks, "search_spend": search.round(), "social_spend": social.round(),
              "display_spend": display.round(), "revenue": revenue.round()}).to_csv(out / "channel_spend.csv", index=False)

# 2. Monthly revenue, 30 months, trend + seasonality + noise. Ask for a 6-month forecast.
months = pd.date_range("2024-01-01", periods=30, freq="MS")
t = np.arange(len(months))
rev = 120_000 + 1_800 * t + 15_000 * np.sin(2 * np.pi * t / 12) + rng.normal(0, 8_000, len(months))
pd.DataFrame({"month": months, "revenue": rev.round()}).to_csv(out / "monthly_revenue.csv", index=False)

# 3. A/B test with a small, uncertain lift. Variant B true rate 0.052 vs A 0.048.
n_a, n_b = 4200, 4100
ab = pd.DataFrame({"variant": ["A"] * n_a + ["B"] * n_b,
                   "converted": np.concatenate([rng.binomial(1, 0.048, n_a), rng.binomial(1, 0.052, n_b)])})
ab.sample(frac=1, random_state=1).to_csv(out / "ab_test.csv", index=False)

# 4. Regional sales, 12 regions with very unequal sample sizes -> hierarchical shrinkage story.
regions = [f"R{i:02d}" for i in range(1, 13)]
rows = []
for i, r in enumerate(regions):
    n = int(rng.choice([6, 12, 40, 120]))
    mu = 1000 + 150 * np.sin(i) + rng.normal(0, 80)
    rows.append(pd.DataFrame({"region": r, "order_value": rng.normal(mu, 300, n).round(2)}))
pd.concat(rows).to_csv(out / "regional_sales.csv", index=False)

print("wrote", sorted(p.name for p in out.iterdir()))
