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
- `references/style.json` — the same brand mapped into the `slide-review` skill's token
  schema. Copy it to the working folder as `style.json` when you build a deck.
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

## Single-slide requests

If the user asks for one slide, make exactly one content slide: no title slide, no closing
slide. It still carries the logo, the footer and the page number ("1 / 1"). The finding is
the slide title; the chart fills the body; a source footnote sits above the footer rule.

## Fonts

Georgia and Calibri are not redistributable, so they are not bundled. If either is missing
in the sandbox, substitute by class and say so in one line of the reply: Georgia -> Playfair
Display (or Source Serif 4), Calibri -> Inter. Never fall back to a sans-serif for titles.

## Hand-off to the review step (`slide-review` skill)

A companion skill, `slide-review`, lets the user restyle and publish the deck with short
menu codes. It does **not** redo the analysis, so it needs the deck's source and tokens.
After every render, leave these files in the working folder (`/root/work`) with exactly
these names:

- `deck.typ` — the Typst source. All fonts, sizes and colours must come from one `#let`
  block at the top that reads `style.json`; no literal font names or hex colours inside the
  slide bodies. Then a global edit changes one token and every slide follows.
- `style.json` — the review skill's token schema. Start from `references/style.json`
  (already mapped from the brand profile) and only change `size_name`/`base_size` or
  `style_preset` if the user asked:
  `heading_font, body_font, size_name, base_size, scale, scheme_name, bg, text, primary,
  accent[], style_preset, logo{path,corner,on}, footer{text,on,page_numbers}, slide_size`.
- `slides.json` — one entry per slide: `title`, `bullets[]`, `notes`, `chart_script` (path
  to the script that draws that slide's chart; it must read fonts/colours from `style.json`
  so a restyle re-draws the chart to match).
- the rendered PDF and one PNG per slide (`slide_01.png`, ...).

Then, in the same turn, **run `slide-review` Step 1**: post one contact-sheet PNG of the
slides, the current-style line, and the main edit menu exactly as that skill specifies. Do
not just post the PDF and stop; the review loop is the user's chance to fix anything before
publishing. When the user later says `✅ publish`, the published file is produced by
`slide-review` from the current `style.json`, and it must still carry the brand (logo,
footer, page numbers) unless the user turned those off with menu 7.

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
