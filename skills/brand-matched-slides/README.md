# brand-matched-slides (Track 03 skill)

**Job:** give Daimon the company's brand once, from Discord, so every deck in every thread
comes out in the company's template instead of PyMC Labs house style.

The whole workflow is in Discord. Nobody runs a script, edits a file, or connects anything:

```
A: @Daimon this is our brand template          (company PDF/PPTX attached)
D: extracts the brand in its sandbox (scripts/extract_brand.py), posts a swatch + 5-line
   summary, and stores the profile as a pinned BRAND PROFILE message with five files
   (brand.json, style.json, logo.png, brand_swatch.png, brand_source.pdf).
   "Brand stored. Every deck from now on uses it."
A (any later thread, nothing attached): @Daimon 5-slide deck for the CMO from this CSV
D: finds the BRAND PROFILE message, renders the deck in that brand, hands off to slide-review.
A: @Daimon this is our new template            -> same as step 1, replaces the profile
```

## Contents

- `SKILL.md`: the instructions Daimon follows (Flow A: set/refresh brand; Flow B: make deck).
- `scripts/extract_brand.py`: PyMuPDF-only extractor. Writes `brand.json`, `logo.png`,
  `brand_swatch.png` and, with `--style`, `style.json` in the `slide-review` schema;
  `--summary` prints the five chat lines Daimon posts.

The skill ships **no brand**. The profile is created from the user's own deck and stored in
the repo, so the same skill works for any company.

## Setup: one install, one attachment

**Step 1 (the installer, once per server).** Hosted Daimon's built-in agent is read-only, so
skills always go on an editable copy. One message does the fork, the skill adds and the channel
routing; the installer only clicks Approve on the two skill cards:

```
@Daimon fork Daimon into an editable copy named brand-agent, add both skills from the latest main of https://github.com/JoshElieson/PyMC (folders skills/brand-matched-slides and skills/slide-review), and point this channel at the copy. Yes to all approvals.
```

To update later, repeat the message with "re-add both skills, replacing the versions you have".
Zips in `dist/` exist for `/agent-setup` uploads, but adding from the repo URL is simpler.

**Step 2 (anyone, in chat).** Attach the company deck (PDF or PPTX) and say:

```
@Daimon this is our brand template
```

Daimon extracts the brand, posts a swatch and a five-line summary, and stores the profile as a
`BRAND PROFILE` message in a `Brand profile` thread. Pin it when asked. That is the whole setup.
`@Daimon set up branded slides` shows a two-line checklist and asks for the deck if none is
stored; `@Daimon brand status` shows the checklist and swatch any time.

**Why not GitHub.** The hosted Daimon GitHub App is read-only for repository contents (its own
description: "read and open issues and PRs"), so a `brand/` commit fails with a 403 no matter
how the Connect GitHub page is set. Tested 2026-10-10. Self-hosted Daimon with a write-capable
app could store the profile in a repo instead; the extractor output is the same five files.

## Demo script

Run the "after" in a server or channel where the company deck has **never** been posted,
otherwise Daimon's Discord search confounds the result.

1. Fresh thread: attach `brand_sources/meridian_board_deck.pdf`,
   `@Daimon this is our brand template`.
   Expect: swatch, five-line summary, a `BRAND PROFILE` message with the five files.
2. New thread, nothing attached: the before-video prompt with `channel_spend.csv`:
   `@Daimon Using channel_spend.csv, which marketing channels drove revenue? Make a 2-slide
   presentation for our CMO: slide 1 the key chart with the finding as the title, slide 2
   the recommendation. Post the PDF and also a PNG image of each slide here in the thread.`
   Expect: Meridian-branded slides (dark #1F1B24, Georgia titles, Calibri body, coral accent,
   logo top-left, footer verbatim, `n / N` bottom-right).
3. Optional refresh: attach a different deck, `@Daimon update our brand to this`. The next
   deck uses the new look.

## Pass criteria

- Step 1 is one user message and one Daimon reply; no questions unless a field was not found.
- The `BRAND PROFILE` message carries all five files.
- Running `scripts/extract_brand.py` on Daimon's output PDF gives the same background, fonts,
  logo corner and footer as `brand_sources/meridian_brand_truth.json` (judging evidence only;
  not part of the user workflow). Verified on the source deck: all six colours, both fonts,
  logo corner and footer match (`probes/brand_extract_test/`).
- Footer text is verbatim; no template content appears in the new deck.
- Hand-off files for `slide-review` are present with the exact names in `SKILL.md`.
