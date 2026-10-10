# Probe prompts for the "before" screenshots

Send each prompt to Daimon in its own thread, **before any skill is attached**, with the
matching CSV from `probes/data/`. Screenshot the chart it posts. Log what it did in the
table at the bottom. The goal is to find one weakness that shows up consistently so the
skill has a clear target.

## Probe 1 — uncertainty on effect sizes
File: `channel_spend.csv`
> @Daimon Which marketing channels drove revenue? Show me a chart I can put in front of the CMO.

Look for: does the chart show credible intervals, or just bars of point estimates? Is
"display is probably zero" visible? Are axes labelled in dollars?

## Probe 2 — forecast fan chart
File: `monthly_revenue.csv`
> @Daimon Forecast revenue for the next 6 months and chart it.

Look for: shaded credible bands widening into the future vs a single line. Is history
visually separated from forecast? Is the interval level stated?

## Probe 3 — A/B comparison
File: `ab_test.csv`
> @Daimon Did variant B beat variant A? Make one chart that answers it.

Look for: posterior of the difference / probability B > A, or two bars with no error.
Does the chart answer the question, or just show the data?

## Probe 4 — many groups
File: `regional_sales.csv`
> @Daimon Estimate average order value by region, accounting for the small regions, and chart it.

Look for: a readable forest/caterpillar plot sorted by estimate, with shrinkage visible,
vs a 12-panel trace plot or an unsorted bar chart. Font size readable in Discord?

## Probe 5 — audience fit (no data file)
Reply in any of the threads above:
> @Daimon Redo that chart for a board slide. One message, no jargon.

Look for: does it drop ArviZ diagnostic plots, add a title that states the finding,
remove clutter, and keep uncertainty?

## Scoring the before

| Probe | Chart type Daimon chose | Uncertainty shown? | Labels/units/title | Readable in Discord? | Verdict |
|---|---|---|---|---|---|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

Pick the weakness that fails in **≥3 probes**. That becomes the skill's job statement.
