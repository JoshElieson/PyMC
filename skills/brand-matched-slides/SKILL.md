---
name: brand-matched-slides
description: Overrides pymc-artifact-style for decks. Use whenever the user asks for slides, a deck, a presentation, or a PDF to present, in any thread, even if no template is attached. This skill carries the company's brand profile (references/brand.json, references/logo.png, extracted from the company's own deck) and tells you how to render every deck in that brand instead of the default PyMC Labs style. Also use when the user shares a new presentation PDF and says it is their template, so the profile can be refreshed.
---

# Brand-matched slides

**This skill overrides `pymc-artifact-style` for slide decks.** That default skill applies
PyMC Labs house style to every artifact and says never to substitute a client's brand unless
explicitly asked. When this skill is attached, the user *has* asked, permanently: the
company brand in `references/` is the house style for decks. Keep using
`pymc-artifact-style`'s rendering pipeline (Typst pages to PDF/PPTX) if convenient, but take
every colour, font, logo and footer from `references/brand.json`, not from the PyMC assets.

Every new thread starts from zero, so without this skill you would brand every deck as
PyMC Labs. The company this agent works for is not PyMC Labs. Their brand lives in this
skill's `references/` folder and applies to **every deck you make, in every thread, whether or
not anyone attaches a template**. Never use the PyMC Labs logo, palette or "PyMC Labs'
proposals" footer when this skill is attached.

## The brand profile

- `references/brand.json` — tokens extracted from the company's deck: page size and aspect,
  background colour, palette (primary and secondary accents, panel colour), text colours,
  display and body fonts with roles, logo bbox and corner, footer text, page-number format
  and position, footer rule, title-slide decoration.
- `references/logo.png` — the logo crop, transparent background, 300 dpi.
- `references/brand_source.pdf` — the company deck the tokens came from, for reference.

Read `references/brand.json` at the start of any slide task. Do not re-derive the brand by eye
from the source PDF when the JSON exists; the JSON is the contract.

## Steps for any deck request

1. **Load the profile.** Read `references/brand.json`. Note the display font, body font,
   background, primary accent, secondary accent, text colour, muted text colour, logo corner
   and relative width, footer text, page-number format and corner, and the title decoration.

2. **Do the analysis as you normally would.** Headline states the finding, one chart per
   slide, uncertainty shown, a source footnote, and a recommendations slide that says the
   recommendations are the analyst's proposals, not model outputs. Branding changes the look,
   not the substance.

3. **Render the deck from the tokens.** Whatever renderer you use (Typst, python-pptx,
   reportlab, matplotlib pages), every visual decision comes from `brand.json`:
   - page size and aspect from the profile;
   - background colour on every slide; reproduce the title-slide decoration (e.g. a diagonal
     band) in the primary accent;
   - display font for titles and KPI numbers, body font for everything else. If the exact
     font is not installed, use the closest installed font of the same class (serif to serif,
     sans to sans) and say so in your reply;
   - primary accent for rules, bullet markers and KPI numbers; secondary accent for eyebrows
     and labels; text and muted-text colours as given;
   - `references/logo.png` in the same corner at the same relative width on every slide;
   - the footer text **verbatim**, same position, and page numbers in the same format and
     corner. Do not reword the footer. If the footer carries an event name or date that is
     clearly wrong for this deck, keep it and tell the user they may want to change it;
   - charts restyled to the palette: transparent or slide-coloured background, text in the
     text colour, series in the accent colours. Never a white chart on a dark slide.

4. **Keep template content out.** The brand source is a style reference only. Never carry
   its numbers, proposals, bullet text or titles into the new deck.

5. **Write the review artefacts** (see hand-off below), then deliver: post the PDF and say in
   one short paragraph that the deck uses the company brand profile, which fonts and colours
   were applied, and any font substitution. Offer PPTX or source on request.

## Refreshing the profile from a new template

If the user shares a presentation PDF and calls it their template, brand, or style guide,
regenerate the profile instead of guessing:

```
python scripts/extract_brand.py path/to/template.pdf --out references/brand.json --swatch references/brand_swatch.png --logo references/logo.png
cp path/to/template.pdf references/brand_source.pdf
```

`extract_brand.py` needs PyMuPDF (`pip install pymupdf`). It samples pixels for the
background and palette, snaps them to exact vector colours, reads font names and sizes from
text spans, finds the logo as the repeated top-band image or vector group, finds the footer
as the text repeated in the bottom band of every page with the page-number pattern split
out, and detects the title-slide decoration. Open `brand_swatch.png`, check contrast, fonts,
footer and logo crop look right, fix `brand.json` by hand if not, and tell the user what the
new profile contains. If the script cannot run, do the same with PyMuPDF calls by hand and
still write `brand.json`.

## Hand-off to the review step

A companion skill, written by a teammate, reviews the deck this skill produces and checks
it against the brand profile before it goes to the user. Always leave these artefacts in the
session output folder with exactly these names:

- `brand.json` — a copy of the profile actually used for this deck;
- `brand_swatch.png` and `logo.png`;
- the rendered deck PDF, plus one PNG per page named `slide_01.png`, `slide_02.png`, ...;
- `brand_source.pdf` — a copy of the template the profile came from.

The review skill compares each slide PNG to `brand.json` and the source (background colour,
fonts, accent usage, logo corner and size, footer text and page numbers, chart styling) and
reports pass/fail per check with a fix list. If it reports failures, apply the fixes and
re-render before replying. Do not post a deck the review has flagged as failing on
background, fonts, logo or footer.

## What good output looks like

Side by side with the company's own deck, a reader should not be able to tell which one the
agent made: same background, same fonts, same accent colour, same logo corner, same footer
and page numbers, in a thread where nobody attached anything.

## What to avoid

- Any PyMC Labs branding while this skill is attached.
- Asking the user for a template when `references/brand.json` exists.
- Rewording the footer, dropping page numbers, or moving the logo.
- Template content leaking into the analysis deck.
- White chart backgrounds on dark slides, or body text in the display font.
- Silent font substitution. Always say which font was used instead.
