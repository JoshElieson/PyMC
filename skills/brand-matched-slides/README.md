# brand-matched-slides (Track 03 skill)

**Job:** give Daimon the company's brand once, from Discord, so every deck in every thread
comes out in the company's template instead of PyMC Labs house style.

The whole workflow is in Discord. Nobody runs a script or edits a file:

```
A: @Daimon this is our brand template          (company PDF/PPTX attached)
D: extracts the brand in its sandbox (scripts/extract_brand.py), posts a swatch + 5-line
   summary, commits brand/brand.json, style.json, logo.png, brand_swatch.png, brand_source.pdf to the
   bound GitHub repo. "Brand stored. Every deck from now on uses it."
A (any later thread, nothing attached): @Daimon 5-slide deck for the CMO from this CSV
D: reads brand/ from the repo, renders the deck in that brand, hands off to slide-review.
A: @Daimon this is our new template            -> same as step 1, replaces the profile
```

## Contents

- `SKILL.md`: the instructions Daimon follows (Flow A: set/refresh brand; Flow B: make deck).
- `scripts/extract_brand.py`: PyMuPDF-only extractor. Writes `brand.json`, `logo.png`,
  `brand_swatch.png` and, with `--style`, `style.json` in the `slide-review` schema;
  `--summary` prints the five chat lines Daimon posts.

The skill ships **no brand**. The profile is created from the user's own deck and stored in
the repo, so the same skill works for any company.

## Attach (once, in Discord)

1. Zip this folder (`SKILL.md` + `scripts/`; `dist/brand-matched-slides.zip` is prebuilt) and add it
   with `/agent-setup` in the team channel.
2. Ask Daimon to connect GitHub and bind the team repo (`JoshElieson/PyMC`). If GitHub is not
   connected, the skill falls back to posting the profile files in Discord and finding them
   again by search.

## Demo script

Run the "after" in a server or channel where the company deck has **never** been posted,
otherwise Daimon's Discord search confounds the result.

1. Fresh thread: attach `brand_sources/meridian_board_deck.pdf`,
   `@Daimon this is our brand template`.
   Expect: swatch, five-line summary, a commit adding the five files under `brand/`.
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
- The commit exists in `brand/` on the bound repo.
- Running `scripts/extract_brand.py` on Daimon's output PDF gives the same background, fonts,
  logo corner and footer as `brand_sources/meridian_brand_truth.json` (judging evidence only;
  not part of the user workflow). Verified on the source deck: all six colours, both fonts,
  logo corner and footer match (`probes/brand_extract_test/`).
- Footer text is verbatim; no template content appears in the new deck.
- Hand-off files for `slide-review` are present with the exact names in `SKILL.md`.
