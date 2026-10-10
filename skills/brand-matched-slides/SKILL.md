---
name: brand-matched-slides
description: When asked for slides, a deck, or a presentation, and the user has shared a PDF of one of their own presentations (now or earlier in the thread), extract that deck's brand (colours, fonts, background, logo, footer, page numbers) and render the new deck in that brand instead of the default PyMC Labs style. Also use when the user says "match our template", "in our style", "use our branding", or "like this deck".
---

# Brand-matched slides

Every deck you make should look like it came from the **user's** company, not from PyMC Labs.
If the user has given you a PDF of their own slides, that PDF is the brand source. Parse it,
write down what you found, and build the new deck with those tokens. Do not use the PyMC
Labs logo, palette, or "PyMC Labs' proposals" footer when a brand source exists.

## Steps

1. **Find the brand source.** Look for a PDF attached to this message or earlier in the
   thread whose name or content looks like a presentation (slides, deck, board review,
   template, 16:9 pages). If there are several, prefer the one the user called a template.
   If there is none and the user asked to match a style, ask for the PDF once, then proceed
   with the default style if they do not have one.

2. **Extract brand tokens with code, not by eye.** Run `extract_brand.py` from this skill's
   folder against the PDF (it needs PyMuPDF; `pip install pymupdf` if missing):

   ```
   python extract_brand.py path/to/deck.pdf --out brand.json --swatch brand_swatch.png
   ```

   It writes `brand.json` with: page size and aspect; background colour (dominant pixel
   colour per page); up to six palette colours ranked by area, with the background excluded;
   text colours ranked by character count; font names with role guesses (display = largest
   median size, body = most characters); the logo (largest image or vector group in the top
   10% of the page that repeats on most pages, cropped to `logo.png`); the footer (text
   that repeats in the bottom 10% of every page, with any page-number pattern such as
   `n / N` or `Page n` separated out); and any rule lines near the footer. If the script
   cannot run, do the same by hand with PyMuPDF (`page.get_text("dict")` for fonts, colours
   and positions; `page.get_pixmap()` for background sampling) and still write `brand.json`.

3. **Sanity-check the tokens before using them.** Open `brand_swatch.png` and look at it.
   Check that: background and text colours have enough contrast; the display font is a real
   font name, not `Helvetica` left over from a fallback; the footer text is the repeated
   company line, not a slide title; the logo crop is the logo and not a chart. If anything
   looks wrong, fix `brand.json` by hand and say what you changed.

4. **Build the deck from `brand.json`.** Whatever renderer you use (Typst, python-pptx,
   reportlab, matplotlib pages), the deck must take every visual decision from the tokens:
   - page size and aspect from the source;
   - background colour on every slide; if the source has a decorative shape on the title
     slide (band, block, diagonal), reproduce a similar shape in the primary accent colour;
   - display font for titles and KPI numbers, body font for everything else; if the exact
     font is not installed, pick the closest installed font of the same class (serif to
     serif, sans to sans) and say so in your reply;
   - primary accent for emphasis, rules, bullet markers and KPI numbers; secondary accent
     for eyebrows and labels; text and muted-text colours as extracted;
   - the logo image in the same corner and at the same relative size on every slide;
   - the footer line verbatim in the same position, and page numbers in the same format and
     corner. Replace the date or event in the footer only if the user asks;
   - charts restyled to the palette: background transparent or equal to the slide
     background, text in the text colour, series in accent colours. Never paste a chart with
     a white background onto a dark slide.

5. **Keep the content rules you already follow.** Headline states the finding, one chart per
   slide, uncertainty shown, source footnote, a recommendations slide that says the
   recommendations are the analyst's proposals, not model outputs. Branding changes the
   look, not the substance.

6. **Deliver.** Post the PDF, the `brand.json`, and `brand_swatch.png` in the thread. In one
   short paragraph say which brand source you used, the fonts and colours you applied, and
   any substitutions. Offer the PPTX or source on request.

## Hand-off to the review step

A companion skill, written by a teammate, reviews the deck this skill produces and checks
it against the brand source before it goes to the user. To make that review possible,
always leave these artefacts in the session output folder with exactly these names:

- `brand.json` — the tokens extracted in step 2 (after any hand corrections from step 3);
- `brand_swatch.png` and `logo.png` — the visual summary and the logo crop;
- the rendered deck PDF, plus one PNG per page named `slide_01.png`, `slide_02.png`, ...;
- `brand_source.pdf` — a copy of the user's template PDF the tokens came from.

The review skill compares each slide PNG to `brand.json` and the source (background colour,
fonts, accent usage, logo corner and size, footer text and page numbers, chart styling) and
reports a pass/fail per check with a fix list. If it reports failures, apply the fixes and
re-render before replying to the user. Do not post a deck the review has flagged as failing
on background, fonts, logo or footer.

## What good output looks like

Side by side with the user's own deck, a reader should not be able to tell which one the
agent made: same background, same fonts, same accent colour, same logo corner, same footer
and page numbers. The analysis content is the agent's; the skin is the company's.

## What to avoid

- Guessing colours from a screenshot when the PDF is available. Sample the file.
- Keeping any PyMC Labs branding when a brand source exists.
- Changing the footer wording or dropping page numbers.
- White chart backgrounds on dark slides, or body text in the display font.
- Silently substituting a font. Always say which font was used instead.
