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

## Scoring the before (run 2026-10-10 12:03-12:08 in the Tester server, #daimon)

Screenshots in `probes/before/`. Daimon's own cost/time footer is included in each.

| Probe | Chart type Daimon chose | Uncertainty shown? | Labels/units/title | Readable in Discord? | Model used | Time / cost |
|---|---|---|---|---|---|---|
| 1 channels | Two horizontal bar panels (revenue driven, return per $1) with error bars and break-even line | Yes, 95% intervals as bars | Title states the finding, $ units, source footnote | Chart is small; tick labels and footnote unreadable without clicking | **Linear regression (OLS), not Bayesian** | 1m12s, $0.20 |
| 2 forecast | Line + fan chart with 80% and 95% bands, forecast split marked | Yes | Title states the finding, $k axis, legend | Fine at thumbnail; axis labels small | **Log-linear trend + seasonality, not Bayesian** | 1m40s, $0.19 |
| 3 A/B | Posterior density of B minus A, shaded by sign, interval bar | Yes, P(B>A)=95% and 95% interval | Title states the verdict, units in pct points | Good | Beta-Binomial, flat priors (Bayesian) | 46s, $0.06 |
| 4 regions | Forest plot sorted by estimate, raw vs shrunk means, small-n highlighted, overall mean line | Yes, 90% credible intervals | Title states the finding, $ axis, legend, footnote | Chart is dense; 12 rows of labels small at Discord size | Hierarchical PyMC model, convergence reported | 2m51s, $0.17 |
| 5 board redo | not run yet | | | | | |

**Verdict:** the hypothesis that Daimon's charts communicate badly is **not supported**.
All four charts show uncertainty, state the finding in the title, label units, and pick a
sensible chart type. The weaknesses that actually showed up:

1. **Not Bayesian by default.** Probes 1 and 2 used OLS / log-linear fits with frequentist
   intervals even though Daimon is sold as a Bayesian agent and PyMC was available. It
   only reached for PyMC when the prompt hinted at it ("accounting for the small regions").
2. **Discord legibility.** Every chart is rendered small; tick labels, legends and footnotes
   need a click to read. No chart used a size/font tuned for an inline Discord preview.
3. **Inconsistent output format.** Probe 2 attached a CSV next to the PNG, probe 4 a PDF,
   probes 1 and 3 only the PNG. Probe 2's "Files are in /mnt/session/outputs" line is
   meaningless to a Discord user.
4. **Slow and variable.** 46s to nearly 3 min per chart, with no interim result.

Candidate pivots for the skill: (a) "always fit the Bayesian version and show it" for
anything with a point estimate, (b) a Discord-first chart style guide, or (c) a
"decision brief" output format that is consistent across questions.

## Slide probe (before) — run 2026-10-10 12:19 in the probe 1 thread

Prompt: `@Daimon Turn this analysis into a 5-slide presentation for the CMO and post it here as a PDF.`

Output: `probes/before/slides_before_cmo_deck.pdf`, rendered pages `slide_before_1..5.png`.
Took 3m40s, $0.45, ~25 tool steps. Typeset with Typst ("PyMC style"); Daimon offered PPTX or Typst source on request.

What Daimon's default deck looks like:
- **PyMC Labs branding on every deck**: PyMC Labs logo top-left of the title slide, Inter font,
  navy (#0d1b3e-ish) headlines, teal (#1a9e8a-ish) accent/eyebrow, orange for "uncertain",
  lavender for baseline, white background, 16:9, footer with source + page number.
- Slide 5 footer even says "Recommendations are PyMC Labs' proposals", i.e. it assumes the
  presenter is PyMC Labs, not the user's company.
- Structure is good: headline-as-finding, 3 KPI tiles, two chart slides with bullets,
  a solid/uncertain/not-tested slide, a numbered recommendations slide.
- Charts are re-rendered in the deck palette and match the Discord chart.
- No way to supply a brand: there is no prompt hint, no template upload path, nothing
  reads the user's existing slides.

**This is the job for Track 03.** Content and layout are fine; the deck is always *PyMC Labs'*
deck. A CMO at Meridian Supply Co. would never present it as-is. The skill: given an
existing deck (PDF/PPTX) from the user's company, extract its brand (fonts, colours,
background, logo placement, footer conventions) and have Daimon render its deck in that
brand. Before = PyMC-branded default; after = same content in the client's own look.

## Brand-match probe (before, no skill) — run 2026-10-10 12:39, fresh thread

Prompt (with `meridian_board_deck.pdf` + `channel_spend.csv` attached):
`@Daimon Using channel_spend.csv, which marketing channels drove revenue? Put the answer in a
5-slide PDF deck for our CMO that matches the look of the attached meridian_board_deck.pdf,
which is our company's presentation template.`

Result: 3m34s, $0.45. Daimon **claims** it matched the template unaided: "I read the exact
colours, shapes, sizes and layout out of meridian_board_deck.pdf, and the Georgia and Calibri
fonts are the ones embedded in it. That gives the dark background, coral and yellow accents,
logo lockup, footer rule, slanted cover stripe, bullet style and figures card."
Output: `probes/before/brandmatch_before_deck.pdf`, pages `brandmatch_before_1..5.png`.
**Verified: the claim is true.** Running `extract_brand.py` on Daimon's deck gives background
#1F1B24, Georgia-Bold / Calibri, logo top-left at 0.117 width, coral rule at y=496, `n / N`
bottom-right, i.e. identical tokens to the Meridian source. Visually it is a convincing
Meridian deck: coral band on the title, KPI panel, coral bullet dots, charts on the dark
background in palette colours. Only the footer text differs (rewritten) and one bullet
leaked template content ("geo-holdout design proposed for search").

Deviations it admitted to on its own:
- changed the footer wording ("Board use only" -> "CMO review");
- dropped currency entirely because the CSV has none;
- carried a "geo-holdout design proposed for search" reference over from the *board deck content*
  into the new deck (template content leaked into analysis content).

Implication: when explicitly told "match this template", Daimon may already do a decent job.
The skill's measurable value then has to come from (a) doing it **without being told**, i.e.
any deck request after a template has been shared in the thread; (b) fidelity scored against
`brand_sources/meridian_brand_truth.json` rather than eyeballing; (c) not editing footer text
and not leaking template content. Verify against the actual PDF before deciding.

**Conclusion for the before/after:** an explicit "match this template" prompt is NOT a usable
before. Next probe = the realistic workflow: share the template in a thread with a neutral
message, then ask for the deck in a later message without mentioning style. If Daimon
reverts to PyMC branding there, that is the before, and the skill's job is "apply the
company brand every time a template has been shared, without being told".

## Workflow probe (before, no skill) — 2026-10-10 12:48-12:52, thread "Meridian board deck template"

Step 1: template PDF shared with "for reference, just confirm you have it". Daimon: confirmed,
12s, $0.08, said it would study layout/colours/fonts/logo once the data arrived.
Step 2 (same thread): CSV + "which channels drove revenue? 5-slide PDF deck for our CMO", no
mention of style. Daimon: 2m36s, $0.32, "I matched the template by reading its exact colours,
fonts and layout" (dark background, coral/yellow logo bars, Georgia titles, Calibri body,
stat card, footer). Output `meridian_cmo_channel_deck.pdf` (not downloaded; same claim as the
verified 12:39 run).

**Conclusion: within a thread, Daimon already brand-matches, prompted or not.** The gap is
across threads: a template shared in one thread does not exist in the next. That is exactly
the brief's framing ("every new Daimon thread starts from zero").

**Final job statement:** "Give Daimon our company's brand permanently, so every deck in every
thread comes out in our template without anyone attaching it." The skill carries
`brand.json` + `logo.png` (generated once from the company's PDF with `extract_brand.py`) and
instructs Daimon to render all decks with them.
- **Before:** fresh thread, no attachment, "make a 5-slide deck" -> PyMC Labs-branded
  (`probes/before/slide_before_*.png`, already captured 12:19).
- **After:** fresh thread, no attachment, skill attached, same ask -> Meridian-branded.

## Cross-thread probe (before, no skill) — 2026-10-10 12:55, fresh thread, nothing attached

Prompt: `@Daimon Do you have our company's presentation template on file? If so, describe its
background colour, fonts, logo and footer. If not, say so.`

Result (1m44s, $0.06): **"Yes. I have it. This thread's workspace was empty, so I re-fetched
meridian_board_deck.pdf from the Discord attachment link and read it directly. My notes from
an earlier session agree with what I found."** It then listed every token correctly:
#1F1B24 background, #2B2633 panels, coral #FF6B4A band, Georgia Bold 26/40/24 pt, Calibri
14 pt body, #DCE6F2 text, #8C8A94 muted, #F2C14E yellow, logo bars 30x6 and 22x6 pt at
top-left, coral rule at y=496 from x=36 to 924, footer text verbatim, "n / N" on the right.

**So "every thread starts from zero" is not literally true for Daimon**: it searches the
server's Discord history and its own session notes, and will re-fetch an attachment from
another thread. Within one Discord server where the template was shared once, Daimon can
brand-match prompted, unprompted, and across threads.

### What is actually left for a skill to fix (evidence-based)

1. **Template never shared in this server.** The 12:19 deck (`slides_before_*.png`,
   PyMC-branded) is the honest before: a company whose template has never been posted in
   the server. The skill ships the brand profile so that case is covered. Any after run must
   happen in a server/channel where the template was never posted (e.g. our hackathon team
   channel on the Decision AI server), otherwise Discord search confounds it.
2. **Fidelity slips**: footer rewording ("Board use only" -> "CMO review"), template content
   leaking into the analysis deck, currency dropped. Fixable by instruction + review step.
3. **Cost/time**: it re-reads the PDF and re-derives the brand every time (2m36s-3m40s,
   $0.32-0.45 per deck). A precomputed `brand.json` should cut that; measure it.
4. **No deterministic contract**: the brand is re-derived by the model each time, so two decks
   may drift. `brand.json` + the review skill make it checkable.
