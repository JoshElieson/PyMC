# CLAUDE.md — PyMC project (Daimon hackathon)

This repo is a hackathon project built on **PyMC**, the Python probabilistic
programming library for Bayesian modeling. This file gives Claude the context
it needs to write correct, modern PyMC code. Keep it updated as the project
takes shape.

## Project status

- Started 2026-10-10 for the Daimon hackathon (see next section).
- Empty repo so far. Python 3.13 is installed locally; PyMC is **not** yet installed.
- Not a git repo yet (run `git init` before the first commit).
- **Track chosen: Track 03 — Extend Daimon** (full brief below). **Team name:** TBD.
- Central repo: https://github.com/JoshElieson/PyMC (branch `main`).

## Daimon hackathon instructions

Source: https://oct-hackathon-landing.pages.dev/ (chapters I–IV). Summarized here so
Claude can act on them without re-fetching.

### Event

- **Daimon Hackathon**, presented by PyMC Labs (Decision AI), part of #AIWeekNY.
- **Saturday, October 10, 2026, 11:00 AM–4:00 PM EDT**, 307 West 38th Street, 17th Floor, New York, NY.
- **Submissions close at 2:00 PM EDT.** Post in `#hackathon-team-submissions` on the Decision AI Discord.

### Schedule

| Time | What |
|---|---|
| 11:00–11:30 | Doors open, registration, team formation |
| 11:30–12:00 | Kick-off |
| 12:00–2:00 | Building session (lunch at 1:30) |
| **2:00** | **Submissions close** |
| 2:00–3:30 | Judges review presentations and walk the tables |
| 3:30–4:00 | Three finalists present (5 min each), winners announced |

### What Daimon is

Daimon is PyMC Labs' open-source Bayesian data science agent that lives in Discord
(Slack/Teams coming). You @mention it with data or a question; it replies in a thread,
writes and runs code, fits PyMC models, and posts charts and **Marimo notebooks**.
It can search Discord history, pull from Google Drive/Notion/YouTube, work against a
bound GitHub repo, attach skills, connect MCP servers, and run scheduled routines.
Built-in skills cover MMM (PyMC-Marketing), GLMs, hierarchical models, A/B tests,
causal inference, and CLV. Chat slash commands: `/agent-setup`, `/routines`,
`/billing`, `/privacy`, `/help`.

- Hosted: https://daimon.pymc-labs.com (redirect from daimon.decision.ai)
- Source: https://github.com/pymc-labs/daimon (Docker Compose, Postgres metadata,
  Anthropic Managed Agents under the hood; skills seeded from a `defaults/` YAML dir)
- Decision Hub (skill marketplace, check before building a skill): https://hub.decision.ai

### Setup options (all require joining Discord and registering a team)

1. **Use the organizers' server** — no setup.
2. **Your own Discord server** — one-click install from daimon.decision.ai, then request the $25 coupon in `#hackathon-support`.
3. **Self-host** — clone the repo, set `DAIMON_ANTHROPIC__API_KEY`, `DAIMON_MCP__JWT_SECRET`, `DAIMON_MCP__PUBLIC_URL`, `POSTGRES_PASSWORD`, `DAIMON_CRYPTO__KEYS`, `DAIMON_DISCORD__BOT_TOKEN`; run `docker compose up --build -d`. The $25 coupon does not cover this.

Registration: RSVP on Gomry, join Discord (https://discord.gg/umy5TWRTQ), post team
name, members, and track in `#hackathon-team-registration`.

### The six build steps

1. Pick a track and form a team (2–6 people; roles Driver / Analyst / Writer / Reviewer are suggestions).
2. Set up Daimon.
3. Frame the project in one paragraph.
4. Build with Daimon.
5. Make a short presentation (5-slide PDF or short video; example at `/tracks/example-presentation.pdf`).
6. Submit in Discord by 2:00 PM.

### Tracks (one per team)

**Track 01 — Data Analysis (Meridian Supply Co.)**
- Fictional company selling dive gear, oyster sauce, and car oil across Europe. Management thinks it's a great year; the board meets Monday.
- Dataset: `https://oct-hackathon-landing.pages.dev/tracks/meridian_data.zip`. 18 months of messy data: orders, customers, products, costs, returns, ad spend, the finance report the board sees, a warehouse export, company chat and support emails, a board memo, seven meeting transcripts. **Start with `DATA_DICTIONARY.md`.**
- Deliverable (5 slides + link to notebook/code):
  1. What's really going on, in three sentences.
  2. What you found, with numbers and one chart.
  3. What Daimon got wrong at first, and how you caught it.
  4. What the board should do next quarter.
  5. Q3 revenue forecast: a point estimate with a low and a high. Judges compare it with actual Q3.
- Suggested process: @Daimon with the zip, split questions across team members in separate threads, verify answers, then ask Daimon to turn findings into the presentation.
- Bonus: a skill that teaches Daimon what to check on a company like this.

**Track 02 — A Data Blog Post**
- Answer a public-data question in marketing/retail, finance, healthcare, or operations/logistics. Publish as a Marimo notebook (Daimon builds and publishes it). No code needed.
- Suggested questions: e-commerce share of US retail post-pandemic; lag from Fed moves to mortgage rates and housing starts; Medicare GLP-1 spending growth (patients vs cost per patient); effect of Manhattan congestion pricing on taxi trips.
- Data sources: FRED (`ECOMPCTSA`, `ECOMSA`, `RSXFS`, `FEDFUNDS`, `DGS10`, `MORTGAGE30US`, `HOUST`, `PERMIT`), US Census `mrtssales92-present.xlsx`, CMS Part D spending/prescriber APIs (query one drug, don't download full-year files), NYC TLC monthly yellow-taxi Parquet + zone lookup CSV, MTA congestion-zone entries.
- **Public, downloadable data only. No scraping.** Tell Daimon to send a User-Agent naming the team and a contact when hitting FRED/government sites.
- Deliverable: link to published Marimo notebook + 4 slides (question; answer with chart; confidence and what you checked; what Daimon got wrong at first) including a notebook screenshot.

**Track 03 — Extend Daimon**
- Teach Daimon a job it currently does badly via a **skill** (short instruction file: steps, what to check, what good output looks like), optionally with an **MCP server** (existing online one like DeepWiki, or your own). A good skill alone can win.
- Template: `https://oct-hackathon-landing.pages.dev/tracks/daimon-track3-template.zip` (starter skill + MCP server). Install uv, run `uv run serve.py` in the folder; it prints a public URL and a message to paste: `@Daimon attach the MCP server at https://<addr>/mcp to our agent as <team>-tools`.
- No-code alternative: `/agent-setup` in the team channel to add a skill or already-online server.
- Deliverable (5 slides + link to skill/code): the job in one sentence; "before" screenshot; what you built; "after" screenshot; link.
- Example jobs: explaining a GitHub project to a newcomer (skill + DeepWiki), monthly company-data check, public-economic-data helper, web info collection/summarization.

### Track 03 brief (our track, verbatim from the event page)

> **Teach Daimon a job it can't do yet.**
> Every new Daimon thread starts from zero. Give it a capability for a job it does
> badly today, and show the difference.
>
> **The goal.** Pick a concrete job, extend Daimon so it does it well, and show Daimon
> before and after.
>
> **What you build.** A skill: a short file of written instructions that tells Daimon
> how to do a job: the steps, what to check, what good output looks like.
> Optionally, an MCP server: tools Daimon can call, so the heavy, repeatable part is
> done the same way every time. Use one that's already online (like DeepWiki, which
> answers questions about GitHub projects) or run your own.
> A good skill on its own can win: you're judged on the idea and the difference it
> makes, not on the code.
> Examples: explain a GitHub project to a newcomer (a skill plus DeepWiki); a monthly
> check on a company's data; a helper for public economic data; collecting and
> summarising information from the web.
> Adding them: run `/agent-setup` in your team's channel to add your skill or a server
> to your team's agent. No code needed unless you build your own server.
>
> **What you hand in, by 2:00 PM.** Posted in #hackathon-team-submissions: a 5-slide
> PDF or a short video, plus a link to your notebook or code. Cover:
> 1. The job, in one sentence.
> 2. Before: Daimon doing the job without your extension (a screenshot).
> 3. What you built.
> 4. After: Daimon doing the job with it (a screenshot).
> 5. A link to your skill or code.
>
> **Optional: your own server in one command.** Download the template (a starter
> skill and MCP server), unzip it, install uv, then in the folder run `uv run serve.py`.
> It starts your server, gives it a public address, and prints the message to paste in
> your team's channel:
> `@Daimon attach the MCP server at https://<your-address>/mcp to our agent as <team>-tools`
>
> **No code needed.** Adding a skill, or a server that's already online, needs no code.
>
> **Example presentation.** A finished 5-slide presentation Daimon made from a single
> message, with made-up figures. A video covers the same points as the slide list above.
>
> **Judging.** Five criteria, weighed together, no points: novelty; a concrete use
> case; technical depth; communication; reproducibility. Teams are 2 to 6 people.
> `/billing` in Discord shows your team's budget.

### Our project direction: brand-matched slide decks (decided 2026-10-10 ~12:25)

**Finding from probes (see `probes/PROBES.md`):** Daimon's charts are already good
(uncertainty shown, finding in the title, labelled units). Its slide decks are structurally
good too, but **every deck is rendered in PyMC Labs' own brand**: PyMC Labs logo, Inter
font, navy/teal/orange palette, white background, footer saying the recommendations are
"PyMC Labs' proposals". There is no way to give Daimon the user's own brand.

**Job statement (revised 12:55 after probes):** "Give Daimon our company's brand permanently,
so every deck in every thread comes out in our template without anyone attaching it."
Probes showed Daimon already matches a template *within* a thread (prompted or not); the gap
is that nothing carries across threads. The skill therefore ships the brand profile
(`brand.json` + `logo.png`, generated once from the company PDF with `extract_brand.py`).

**Why this wins on the judging criteria:** the before/after contrast is stark and visual
(PyMC-branded vs client-branded, same content); the use case is concrete (every analyst
who has to put Daimon's output in front of their own exec); technical depth comes from
brand extraction (PDF/PPTX parsing, font + colour detection, logo cropping); reproducible
because the skill + a sample "brand source" deck can be re-run by the judges.

**Build plan:**
1. Before shots: done. `probes/before/slide_before_1..5.png` + the PDF.
2. Create a sample "company" deck with a distinct brand (dark background, serif display
   font, different accent colours, a fake logo) to act as the brand source. Put it in
   `brand_sources/`.
3. Write the skill `skills/brand-matched-slides/SKILL.md`: when asked for slides, look for
   an attached or previously shared deck; extract brand tokens (primary/secondary/accent
   colours as hex, background colour, heading + body fonts, logo image + position, footer
   pattern, slide size); write them to `brand.json`; render the deck with those tokens
   (Typst or python-pptx); show a one-slide swatch for confirmation if anything is ambiguous.
4. **Review skill (teammate-owned):** a second skill reviews the rendered deck against
   `brand.json` and the source PDF and returns pass/fail per check. The hand-off contract
   (file names it expects) is in `skills/brand-matched-slides/SKILL.md`. Keep that
   section in sync if the reviewer's inputs change.
5. Optional MCP server: `extract_brand(pdf_or_pptx) -> brand.json` tool so the heavy
   parsing is deterministic (PyMuPDF for fonts/colours/images, python-pptx for theme XML).
   Only build if the skill alone can't get Daimon to extract reliably.
6. After shots: attach via `/agent-setup`, re-run the same "5-slide presentation for the
   CMO" prompt with the brand-source deck attached, render pages, compare side by side.
7. Slides for submission: job sentence, before (PyMC-branded slide 1), what we built,
   after (client-branded slide 1), repo link.

**Working plan for Track 03 (update as decisions are made):**
- [ ] Choose the job. Must be concrete, something Daimon visibly does badly today, and demoable in a screenshot. **Current candidate: chart communication (above).**
- [ ] Capture the **before** screenshot early, before any skill is attached.
- [ ] Write the skill file: steps, what to check, what good output looks like. Keep it short.
- [ ] Decide whether an MCP server adds real value. If yes, start from the template in `track3-template/` and run `uv run serve.py`.
- [ ] Attach via `/agent-setup` (skill) or the `@Daimon attach the MCP server ...` message.
- [ ] Capture the **after** screenshot.
- [ ] Build the 5 slides (ask Daimon to generate them from one message) and post with the repo link by 2:00 PM.

### Rules

- R01: Must use Daimon (managed or self-hosted).
- R02: Teams of 2–6, no solo entries, Discord membership required, one track per team.
- R03–R05: Track-specific deliverables above.
- R06: **Every finding must include the code and data that produced it.**
- R07: One submission per team in `#hackathon-team-submissions`.
- R08: Submit by 2:00 PM.

### Judging and prizes

Criteria, weighed together: **novelty, concrete use case, technical depth, communication, reproducibility.**

- 1st: PyMC Labs data science/analytics course seat per team member (~$1,900 each).
- 2nd: $50 Amazon gift card per member.
- All teams: $25 Daimon credit. Standout work may be featured by PyMC Labs.

### Implications for how Claude should work here

- Everything must be reproducible: keep data, code, and outputs together; prefer Marimo notebooks or plain scripts with pinned deps.
- "What Daimon got wrong" is a required slide in every track. Log Daimon's first answers and the checks that caught errors.
- Bayesian forecasts need a credible interval (Track 01 asks for low/high explicitly). Use PyMC and report uncertainty honestly.
- Time budget is 2 hours of build. Favor simple, correct models over ambitious ones.

## Environment setup

```bash
# Recommended: includes nutpie, the fast Rust NUTS sampler (auto-selected when present)
pip install "pymc[nutpie]" arviz

# Optional JAX backends
pip install numpyro      # pm.sample(nuts_sampler="numpyro")
pip install blackjax     # pm.sample(nuts_sampler="blackjax")

# Optional ecosystem
pip install bambi        # formula-based GLMs on top of PyMC
pip install pymc-extras  # experimental distributions / inference (formerly pymc-experimental)
pip install graphviz     # for pm.model_to_graphviz
```

Conda alternative: `conda create -c conda-forge -n pymc_env "pymc>=6"`. Use conda
if you need the legacy C backend or BLAS control.

## Current version: PyMC 6.x (6.3.2 as of Sept 2026)

PyMC 6.0 (May 2026) was a **breaking major release**. Most tutorials and LLM
training data describe PyMC 5. Watch for these differences:

| Area | PyMC 5 (old) | PyMC 6 (current) |
|---|---|---|
| Compute backend | PyTensor C backend | **PyTensor 3.x, numba default** (`pytensor.config.linker = "cvm"` restores old) |
| Default NUTS | PyMC's own Python NUTS | **nutpie** if installed (400 tune steps default; PyMC NUTS uses 1000). Set `tune=` explicitly. |
| Return type of `pm.sample` | `arviz.InferenceData` | **`xarray.DataTree`** (ArviZ 1.0) |
| Extending results | `idata.extend(...)` | `idata.update(...)` |
| Trace plot | `az.plot_trace` | **`az.plot_trace_dist`** (or `az.plot_rank_dist`) |
| Default credible interval | 94% HDI | **89% equal-tailed** |
| Custom densities | `pm.DensityDist` | **`pm.CustomDist`** (DensityDist deprecated in 6.1) |
| Posterior predictive | `var_names` controlled resampling | `var_names` only controls what is *saved*; use **`sample_vars=`** (resample) and **`freeze_vars=`** (reuse from trace). Volatile vars now warn instead of silently resampling. |
| `sample_prior_predictive` | `samples=` kwarg | `draws=` (`samples` removed) |
| `pm.dims` module | experimental warning | warning removed, still evolving |
| `SumTo1` transform | available | deprecated (6.2) |

Other 6.x additions: `Model.table()` summary, `FrozenModel` with cached compiled
functions (6.3), `compute_deterministics` accepts a DataTree (6.3), `dims.DiracDelta`,
`TruncatedNormal.icdf`, Mermaid model diagrams via `pm.model_to_mermaid`.

## Core API cheat sheet

### Model building

```python
import numpy as np, pymc as pm, arviz as az

coords = {"obs_id": np.arange(100), "group": ["a", "b", "c"]}
with pm.Model(coords=coords) as model:
    x = pm.Data("x", x_np, dims="obs_id")            # swappable data container
    alpha = pm.Normal("alpha", 0, 10)
    beta = pm.Normal("beta", 0, 10, dims="group")
    sigma = pm.HalfNormal("sigma", 1)
    mu = pm.Deterministic("mu", alpha + beta[g_idx] * x, dims="obs_id")
    pm.Normal("y", mu=mu, sigma=sigma, observed=y_np, dims="obs_id")
    pm.Potential("penalty", -0.5 * pm.math.sqr(alpha))  # arbitrary log-prob term

    idata = pm.sample(random_seed=42)                  # NUTS; returns xarray.DataTree
    idata.update(pm.sample_posterior_predictive(idata, random_seed=42))

az.summary(idata, var_names=["alpha", "beta", "sigma"])
```

- `with pm.Model() as model:` context; first arg of every RV is its **name**.
- `coords`/`dims` label dimensions. Prefer them over raw `shape=`.
- `pm.Data` + `pm.set_data({...})` for out-of-sample prediction.
- `pm.Deterministic` stores derived quantities in the trace.
- `pm.Potential` adds arbitrary terms to the log-probability (constraints, soft penalties).
- NaNs in `observed=` are automatically imputed.
- `pm.CustomDist(name, *params, logp=fn, random=fn, dist=fn)` for custom likelihoods.
- `pm.Truncated(dist, lower, upper)`, `pm.Censored(dist, lower, upper)` wrappers.
- `pm.do(model, {...})` / `pm.observe(model, {...})` for causal interventions and conditioning.
- Debugging: `model.debug()`, `model.point_logps()`, `model.compile_logp()`, `pm.draw(var, draws=n)`.
- Visualize: `pm.model_to_graphviz(model)`, `pm.model_to_mermaid(model)`, `model.table()`.

### Sampling

| Function | Purpose |
|---|---|
| `pm.sample(draws=1000, tune=1000, chains=4, target_accept=0.8, nuts_sampler="nutpie"/"pymc"/"numpyro"/"blackjax")` | MCMC. NUTS for continuous, Metropolis-family for discrete, auto-assigned. |
| `pm.sample_prior_predictive(draws=500)` | Prior predictive checks. |
| `pm.sample_posterior_predictive(idata, sample_vars=[...], freeze_vars=[...])` | Posterior predictive / forecasting. |
| `pm.sample_smc()` | Sequential Monte Carlo (multimodal posteriors, ABC with `pm.Simulator`). |
| `pm.fit(n=10000, method="advi"/"fullrank_advi"/"svgd")` | Variational inference; `.sample(1000)` for draws. |
| `pm.find_MAP()` | Point estimate (debugging / init only). |
| `pm.compute_deterministics(idata)` | Compute Deterministics post hoc. |

Step methods (pass via `step=`): `NUTS`, `HamiltonianMC`, `Metropolis`, `Slice`,
`DEMetropolis`, `DEMetropolisZ`, `BinaryGibbsMetropolis`, `CategoricalGibbsMetropolis`,
`CompoundStep`.

Diagnostics to check after every `pm.sample`: divergences, `r_hat` ≈ 1.00,
`ess_bulk`/`ess_tail` > ~400, `az.plot_energy`, `az.plot_rank_dist`. Raise
`target_accept` (0.9–0.99) or reparameterize (non-centered) on divergences.

### Distributions (all under `pm.`)

- **Continuous:** Normal, HalfNormal, StudentT, HalfStudentT, Cauchy, HalfCauchy,
  Beta, Gamma, InverseGamma, Exponential, LogNormal, Uniform, Flat, HalfFlat,
  TruncatedNormal, Laplace, AsymmetricLaplace, SkewNormal, SkewStudentT, Weibull,
  Gumbel, Logistic, LogitNormal, Pareto, ChiSquared, ExGaussian, Kumaraswamy,
  Moyal, Rice, VonMises, Wald, Triangular, Interpolated, PolyaGamma.
- **Discrete:** Bernoulli, Binomial, BetaBinomial, Poisson, NegativeBinomial,
  Geometric, HyperGeometric, DiscreteUniform, DiscreteWeibull, Categorical,
  OrderedLogistic, OrderedProbit.
- **Multivariate:** MvNormal, MvStudentT, Dirichlet, Multinomial, DirichletMultinomial,
  OrderedMultinomial, LKJCorr, LKJCholeskyCov, Wishart, WishartBartlett, MatrixNormal,
  KroneckerNormal, CAR, ICAR, ZeroSumNormal, StickBreakingWeights.
- **Mixtures:** Mixture, NormalMixture, ZeroInflated{Poisson,Binomial,NegativeBinomial},
  Hurdle{Poisson,NegativeBinomial,Gamma,LogNormal}.
- **Time series:** AR, GaussianRandomWalk, MvGaussianRandomWalk, MvStudentTRandomWalk,
  GARCH11, EulerMaruyama.
- **Wrappers/other:** Truncated, Censored, CustomDist, Simulator (ABC), DiracDelta.

### Gaussian processes (`pm.gp`)

- Implementations: `Latent`, `Marginal`, `MarginalApprox` (sparse), `HSGP` /
  `HSGPPeriodic` (fast low-rank approximation, best default for 1–3D inputs), `LatentKron`,
  `MarginalKron`, `TP` (Student-t process).
- Covariance: `ExpQuad`, `Matern32`, `Matern52`, `RatQuad`, `Exponential`, `Periodic`,
  `Cosine`, `Linear`, `Polynomial`, `WhiteNoise`, `Constant`, `Gibbs`, `WarpedInput`,
  `Coregion`, `ScaledCov`, `Kron`. Combine with `+` and `*`.
- Mean: `Zero`, `Constant`, `Linear`.
- Pattern: `gp = pm.gp.Marginal(cov_func=cov); gp.marginal_likelihood("y", X, y, sigma)`;
  predict with `gp.conditional("f_new", X_new)`.

### Other modules

- `pm.math`: `dot`, `sigmoid`/`invlogit`, `logit`, `exp`, `log`, `sqr`, `switch`,
  `clip`, `logsumexp`, `softmax`, `cumsum`, etc. Use these (or `pytensor.tensor`),
  **not numpy**, inside models.
- `pm.ode.DifferentialEquation`: ODE models (slow; consider sunode or `pytensor` scan).
- `pm.dims`: explicit-dimension API (xarray-style broadcasting by name). Still evolving.
- `pm.stats` / `pm.plots` re-export ArviZ.
- `pm.model.fgraph`: model ↔ PyTensor graph conversion for model transformations.

## Ecosystem

- **ArviZ 1.0** — diagnostics and plotting (`az.summary`, `az.plot_posterior`,
  `az.plot_forest`, `az.plot_ppc`, `az.loo`, `az.compare`, `az.hdi`, `az.extract`).
- **nutpie** — default fast NUTS. **NumPyro / BlackJAX** — JAX GPU sampling.
- **Bambi** — R-style formula GLMs/mixed models (`bmb.Model("y ~ x + (1|group)", df)`).
- **pymc-extras** — experimental: marginalized models, pathfinder, Laplace, state-space models, prior-from-idata.
- **PyMC-Marketing** — MMM and CLV models. **CausalPy** — causal inference.
- **PyTensor** — the tensor/graph backend under everything.

## Conventions for this project

- Always use `coords`/`dims`; name every variable descriptively.
- Set `random_seed=` on all sampling calls for reproducibility.
- Run prior predictive checks before fitting; posterior predictive checks after.
- Report convergence diagnostics with every model fit.
- Keep notebooks in `notebooks/`, reusable model code in `src/`, data in `data/`.
- Pin dependencies in `requirements.txt` (`pymc>=6.3,<7`).

## Reference links

- Docs: https://www.pymc.io/projects/docs/en/stable/
- Example gallery: https://www.pymc.io/projects/examples/en/latest/gallery.html
- API: https://www.pymc.io/projects/docs/en/stable/api.html
- Releases: https://github.com/pymc-devs/pymc/releases
- Discourse: https://discourse.pymc.io/
