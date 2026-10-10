---
name: branded-slides
description: "Branded slide decks in Discord, end to end. Use whenever the user asks for slides, a deck, a presentation, or a PDF to present, in any thread, even if nothing is attached; when the user shares a presentation (PDF or PPTX) and calls it their template, brand, style guide or house style, or asks to set, update or refresh the company brand; when the user asks to set up, get started with, check the status of, or get help with branded slides; and always right after a deck has been rendered or when the user asks to review, edit, restyle or publish slides. Overrides pymc-artifact-style for decks. The brand is extracted from the user's own deck and stored as a BRAND PROFILE message in Discord; setup is one step (attach the deck). After every render, a button-driven review loop (post_wizard) applies edits across the whole deck and publishes the final PDF or PPTX."
---

# Branded slides

**This skill overrides `pymc-artifact-style` for slide decks.** That default skill applies
PyMC Labs house style to every artifact and says never to substitute a client's brand unless
explicitly asked. When this skill is attached, the user *has* asked, permanently: the
company brand stored in Discord is the house style for decks. Keep using
`pymc-artifact-style`'s rendering pipeline (Typst pages to PDF/PPTX) if convenient, but take
every colour, font, logo and footer from `brand.json`, not from the PyMC assets.

The company this agent works for is not PyMC Labs. Never use the PyMC Labs logo, palette or
"PyMC Labs' proposals" footer while this skill is attached.

**Everything happens in Discord.** The user never runs a script, edits a file or opens a
terminal. You extract the brand, store it, and reuse it. Never ask the user to run anything
on their machine.

## Where the brand lives

The brand profile is a Discord message, posted by you, whose first line is exactly
`BRAND PROFILE`, with five attachments:

| File | What it is |
|---|---|
| `brand.json` | tokens extracted from the company's deck (schema below) |
| `style.json` | the same brand mapped into the review token schema (Flow C) |
| `logo.png` | logo crop, transparent background, 300 dpi |
| `brand_swatch.png` | one-image summary of the profile, for humans to eyeball |
| `brand_source.pdf` | the deck the tokens came from |

`brand.json` fields: `page_size_points`, `aspect`, `background`, `dark_theme`, `palette[]`,
`text_colors[]`, `fonts[]`, `roles{display, body, primary_accent, secondary_accent, panel,
text, muted_text}`, `logo{kind, bbox_points, corner, relative_width, file}`,
`footer{text, page_number_format, page_number_position, rule}`, `title_decoration`.

Post it in a thread named `Brand profile` in the channel where the skill was set up, and
ask the user to pin it (one line: "Pin this message so it is easy to find"). In any later
thread, find the newest `BRAND PROFILE` message in this server with Discord search and
re-fetch its attachments. This works across threads and channels; it is the only storage
this skill uses. No GitHub, no repo, no keys. The profile is replaced by posting a newer
`BRAND PROFILE` message; never edit the old one.

This skill ships no brand of its own. `brand.json` is the contract: when it exists, do not
re-derive the brand by eye from the PDF.

## Flow 0: setup ("set up", "get started", "status", "help")

Trigger: the user asks to set up, get started, onboard, check status or get help with
branded slides; or a deck is requested before any brand exists. Setup is one step and the
user never leaves Discord.

1. Search this server for a `BRAND PROFILE` message. Post one checklist message:

   ```
   Branded slides: setup
   ✅ Skill installed
   ⬜ Brand set   (attach your company's deck, PDF or PPTX, in this thread)
   ```
   If a profile exists, tick both lines, post the stored swatch under it, say in one line
   that any deck request in any thread uses this brand, and stop.

2. If none exists, the checklist is the whole ask: one line under it, "Attach your
   company's deck (PDF or PPTX) here and I'll learn your brand from it." When the deck
   arrives, run Flow A. Flow A ends by re-posting the checklist with both lines ticked and:
   "Setup complete. Ask for slides in any thread and they'll come out in your brand. Want a
   test deck now?"

3. **Status at any time.** `@Daimon brand status` posts the same checklist (plus swatch when
   the brand is set) without changing anything.

Never ask the user to install anything, connect GitHub, run a script, or open a web page.

## Flow A: set or refresh the brand

Trigger: the user attaches a PDF or PPTX and calls it their template, brand, style guide,
house style, or asks to set/update/refresh the brand. Also run this flow when Flow B finds
no profile and the user then attaches a deck.

1. **Get a PDF.** Download the attachment. If it is a PPTX, convert it:
   `soffice --headless --convert-to pdf <file>.pptx`. If no converter is available, ask the
   user to export the deck as PDF and attach that instead.
2. **Extract.** From the skill folder run
   `python scripts/extract_brand.py <template>.pdf --out brand.json --swatch brand_swatch.png --logo logo.png --style style.json --summary`
   (`pip install pymupdf` first if it is missing). It samples pixels for the background and
   palette, snaps them to exact vector colours, reads font names and sizes from text spans,
   assigns display/body roles and accent/panel/text roles, finds the logo as the repeated
   top-band image or vector group and crops it, finds the footer as the text repeated in the
   bottom band with the page-number pattern split out, detects the title-slide decoration,
   and writes `style.json` in the review schema (Flow C). If the script cannot run, do the
   same with PyMuPDF calls by hand and still write the same `brand.json` and `style.json`.
3. **Check.** Open `brand_swatch.png`. If a field is null (no logo, no footer, no fonts) or
   text-on-background contrast is below 4.5:1, fix `brand.json` by hand where the fix is
   obvious, otherwise ask the user one short question. Do not ask when everything was found.
4. **Store.** Copy the template to `brand_source.pdf`. Post one message whose first line is
   `BRAND PROFILE` with the five attachments `brand.json`, `style.json`, `logo.png`,
   `brand_swatch.png`, `brand_source.pdf`, in a thread named `Brand profile` in the setup
   channel (create it if missing). Confirm the post carries all five files; if any is
   missing, post again with fresh file names. Ask the user to pin it.
5. **Confirm in one message.** Post `brand_swatch.png` and the `--summary` output (five
   lines: background and accent, fonts, logo, footer, page numbers), then one line: the brand
   is stored and every deck from now on, in any thread, will use it. Offer to make a deck.

## Flow B: make a deck

Trigger: any request for slides, a deck, a presentation or a PDF to present.

1. **Load the profile.** Find the newest `BRAND PROFILE` message in this server with
   Discord search and download `brand.json`, `style.json` and `logo.png`. Note display font, body
   font, background, primary accent, secondary accent, panel colour, text and muted text
   colours, logo corner and relative width, footer text, page-number format and corner,
   title decoration.
   **If no profile exists**, run Flow 0 (it asks for the deck and runs Flow A), then
   continue here. Do not fall back to PyMC branding.

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
     and labels; panel colour for tiles and cards; text and muted-text colours as given;
   - `logo.png` in the same corner at the same relative width on every slide;
   - the footer text **verbatim**, same position, and page numbers in the same format and
     corner. Do not reword the footer. If the footer carries an event name or date that is
     clearly wrong for this deck, keep it and tell the user they may want to change it;
   - charts restyled to the palette: transparent or slide-coloured background, text in the
     text colour, series in the accent colours. Never a white chart on a dark slide.

4. **Keep template content out.** The brand source is a style reference only. Never carry
   its numbers, proposals, bullet text or titles into the new deck.

5. **Write the review artefacts** (see hand-off below), then deliver: post the PDF and say in
   one short paragraph that the deck uses the stored company brand, which fonts and colours
   were applied, and any font substitution. Offer PPTX or source on request. Check the post
   actually carries the attachments; Discord drops a file re-sent under a name already used
   in the thread, so later renders must use new names (`_r2`, `_final`) and a post that
   arrives without its files must be re-sent with fresh names before you claim it.

## Single-slide requests

If the user asks for one slide, make exactly one content slide: no title slide, no closing
slide. It still carries the logo, the footer and the page number ("1 / 1"). The finding is
the slide title; the chart fills the body; a source footnote sits above the footer rule.

## Fonts

Company fonts are often not redistributable, so they are not bundled. If a font named in
`brand.json` is missing in the sandbox, substitute by class and say so in one line of the
reply: a serif display font -> Playfair Display (or Source Serif 4), a sans body font ->
Inter (or Carlito for Calibri-metric decks). Never fall back to a sans-serif for serif titles.
Nothing in this skill assumes a particular company, font or palette; everything comes from
the stored profile.

## Flow C: review and publish (every time a deck is rendered)

Runs right after Flow B renders a deck, without exception, in the same turn. A request for
"the PDF", "a PNG per slide", a fixed slide count, or "fixed deliverables" describes the
output, not permission to skip review. Post what was asked for, then post the review round.
Skip only if the user said "no review" or "publish directly" in this thread, and say so.
Also runs when the user asks to review, edit, restyle or publish slides. The job is to let
the user make easy edits without redoing the analysis, then publish.

Flow B must leave these files in the working folder before Flow C starts:

- `deck.typ`, `style.json` (start from the stored `style.json`), `slides.json` (one entry
  per slide: `title`, `bullets[]`, `notes`, `chart_script` that reads fonts and colours from
  `style.json`);
- `brand.json`, `logo.png`, `brand_swatch.png`, `brand_source.pdf` (copies of the stored
  profile);
- the rendered PDF and one PNG per slide (`slide_01.png`, ...).

### Inputs (written by Flow B)

- `deck.typ`: Typst source of the deck (all fonts, sizes and colours in one `#let` block that reads `style.json`)
- `style.json`: every visual token: `heading_font, body_font, base_size, scale, bg, text,
  primary, accent[], style_preset, logo{path,corner,on}, footer{text,on,page_numbers},
  slide_size`
- `slides.json` (optional): per-slide title, bullets, notes, chart script

If `style.json` is missing, first create it by moving every hard-coded font, size and
colour in `deck.typ` into one `#let` block that reads `style.json`. After that, each global
edit changes exactly one token and applies to every slide.

### On Discord: use the `post_wizard` tool, not typed codes

Discord has real buttons and dropdowns, and the agent can post them with the `post_wizard`
tool (multi-step form; `choice` renders as buttons, `multi` as a dropdown select, `text` as a
free-text box; the user gets Back / Next / Submit and the answers come back to you as one
message). On Discord, **every review round is one wizard**, and the typed-code menus below
are the fallback for platforms without `post_wizard` (Slack) or if the tool errors.

Round shape on Discord:

1. Post the contact sheet PNG and the current-style line as a normal message (the wizard
   cannot carry an arbitrary PNG; only image-generation handles).
2. Call `post_wizard` with `prompt` = `"Edit your deck"` and these steps, in this order.
   Mark the current value in each label with `◉`; keep every label under 80 characters;
   use `allow_custom: false` except where noted. Do not add steps beyond these seven.

   | key | kind | question | options (value → label) |
   |---|---|---|---|
   | `font` | choice | Font | `keep` → `◉ Keep template (<heading_font> / <body_font> from style.json)`, `serif` → `Serif: Playfair Display / Source Serif 4`, `sans` → `Clean sans: Inter / Inter`, `modern` → `Modern: Montserrat / Open Sans`, `mono` → `Mono accents: IBM Plex Sans / Plex Mono numbers` (allow_custom: true, for "heading / body") |
   | `size` | choice | Font size | `S` → `S  body 16pt (dense)`, `M` → `◉ M  body 20pt (default)`, `L` → `L  body 24pt (on a screen)`, `XL` → `XL body 28pt (big room)` |
   | `scheme` | choice | Colour scheme | `template` → `◉ Template (extracted from your deck)`, `light` → `Light: white bg, template primary accent`, `dark` → `Dark: deep bg, light text`, `contrast` → `High-contrast: black/white + one accent`, `mono` → `Monochrome: shades of primary` (allow_custom: true, for "#bg #primary [#accent]") |
   | `style` | choice | Style | `corporate` → `◉ Corporate`, `minimal` → `Minimal`, `bold` → `Bold`, `dense` → `Data-dense`, `playful` → `Playful` |
   | `chrome` | multi | Logo & footer (tick what should be ON) | `logo` → `Logo`, `footer` → `Footer text`, `pages` → `Page numbers` (min 0, max 3; pre-select by naming the current ON ones first in the question, e.g. "currently: Logo, Footer, Pages") |
   | `text` | text | Slide text edits, one per line, or leave blank | e.g. `1 title: ...` / `2 bullet 3: ...` / `2 add bullet: ...` / `2 drop bullet 3` |
   | `action` | choice | What next? | `preview` → `Apply and preview`, `publish_pdf` → `✅ Publish PDF`, `publish_pptx` → `📎 Publish PPTX`, `undo` → `↩ Undo last round` |

3. End your turn immediately after `post_wizard` returns (it tells you to). The answers
   arrive as the next message. Parse them exactly like the typed codes: `font`, `size`,
   `scheme`, `style` map to menus 1–4; `chrome` maps to menu 7 (anything not ticked is OFF);
   each line of `text` maps to menu 5; `action` decides whether to re-render and post a new
   round (`preview`), publish (Step 5), or restore the previous version (`undo`) and post a
   new round.
4. Unchanged answers (the user just clicked Next through a step) must not count as edits.
   Compare each answer to the current `style.json` and only echo real changes:
   `✔ Size → L · ✔ Slide 1 title updated`. If nothing changed and action is `preview`,
   re-post the current sheet with "No changes" and a fresh wizard.
5. A wizard round that fails validation (label too long, too many options) is a bug in the
   labels; shorten and retry once, then fall back to the typed menu for that round.

### Step 1: Post the review message (typed-code fallback)

Always post one message, in this order:
1. One contact-sheet PNG of all slides in a grid, numbered, sized for an inline Discord
   preview (about 1600 px wide). Don't post one image per slide.
2. The current-style line, e.g.
   `Font: <heading_font> / <body_font> · Size: M · Colours: Template · Style: Corporate`
   (every value read from `style.json`; never hard-code a company's fonts or colours)
3. The main menu, exactly:

```
🎛️ Edit your deck — reply with a code (combine: 1b 3a)
 1 Font          2 Font size     3 Colour scheme   4 Style
 5 Slide text    6 Layout/order  7 Logo & footer
 ✅ publish   📎 publish pptx   ↩ undo   👀 preview <n>
```

### Step 2: Sub-menus

When the reply is just a number, post that sub-menu exactly as written below. Mark the
current option with `◉` and the others with `○`.

```
1 · Font                         (current: <heading> / <body>)
 a Keep template
 b Serif        Playfair Display / Source Serif 4
 c Clean sans   Inter / Inter
 d Modern       Montserrat / Open Sans
 e Mono accents IBM Plex Sans / IBM Plex Mono for numbers
 f Custom       1f <heading font> / <body font>
```
```
2 · Font size                    (current: <S/M/L/XL>)
 a S   body 16pt   (dense, reading deck)
 b M   body 20pt   (default)
 c L   body 24pt   (presenting on a screen)
 d XL  body 28pt   (big room, fewer words)
 e Custom  2e <body pt>
```
```
3 · Colour scheme                (current: <name>)
 a Template      colours extracted from the uploaded deck
 b Light         white bg, template primary as accent
 c Dark          deep bg (#0F172A-ish), light text, template accents
 d High-contrast black/white + one accent, for projectors
 e Monochrome    shades of the template primary
 f Custom        3f <bg #hex> <primary #hex> [accent #hex]
```
```
4 · Style                        (current: <preset>)
 a Corporate   balanced spacing, rule under titles, square KPI tiles
 b Minimal     lots of white space, no rules, thin type, light gridlines
 c Bold        heavy titles, colour-block headers, big numbers
 d Data-dense  tighter spacing, smaller margins, gridlines on
 e Playful     rounded tiles, accent shapes, softer palette
```
```
5 · Slide text
 5 <slide> title: <text>
 5 <slide> bullet <k>: <text>      (5 3 bullet 2: ...)
 5 <slide> add bullet: <text>   ·   5 <slide> drop bullet <k>
 5 <slide> note: <speaker note>
```
```
6 · Layout/order
 a Swap        6a <i> <j>
 b Drop        6b <n>
 c Duplicate   6c <n>
 d Split       6d <n>   (one idea per slide)
```
```
7 · Logo & footer
 a Logo on/off
 b Logo corner   7b tl | tr | bl | br
 c Footer text   7c <text>
 d Page numbers on/off
```

Style presets change only layout tokens (spacing, title weight, rules, tile shape,
gridlines). They never change fonts or colours. Those stay under options 1 and 3.

### Step 3: Apply edits

1. Parse every code in the reply. Before rendering, echo what you understood on one line:
   `✔ Font → Serif · ✔ Colours → Dark · ✔ Slide 1 title updated`.
   If one code is unclear, apply the clear ones and ask about that code only.
2. Save the current `style.json` (and `slides.json` / `deck.typ` if text or order changes)
   as version `v<n>` before changing anything. `↩ undo` restores the previous version.
3. Change only the tokens or slide text that were asked for. Never regenerate the
   content, re-run the model, or rewrite slides the user didn't touch.
4. Run the checks below, re-render, then post Step 1 again (contact sheet, current-style
   line, main menu). `👀 preview <n>` posts slide n at full size only.

### Step 4: Checks before every render

- **Contrast**: text vs background ≥ 4.5:1 (and ≥ 3:1 for chart marks vs background).
  If a pick fails, nudge the text/mark colour until it passes and say so in the echo line.
- **Overflow**: after a font or size change, no text runs off a slide or overlaps a
  chart. If something would, shrink that slide's body one step and offer `6d <n>` (split).
- **Charts**: re-run each chart script with the new palette and fonts so charts match
  the slides. Don't recolour or stretch the old PNGs.
- **Fonts**: if a font isn't available, use the nearest Google font and say which one you
  substituted.
- **Consistency**: a global edit must show up on every slide, including title and
  closing slides, KPI tiles, chart labels, and the footer.

### Step 5: Publish

On `✅ publish` (PDF) or `📎 publish pptx`:
1. Final render from the current version. It must match the last preview exactly.
2. Attach `<Company>_<topic>_<YYYY-MM-DD>_final.pdf` (or `.pptx`) and
   `<Company>_style_<YYYY-MM-DD>.json` so the same look can be reused in a later thread
   ("use this style.json").
3. One closing line: slide count plus a summary of the edits made, e.g.
   `Published 5 slides · Serif, L, Dark, Corporate · 2 text edits`.
Never mention sandbox paths like `/mnt/session/outputs`. The attachments are the output.

### Attachments: new names every round, and check they arrived

Discord silently drops a file that is re-sent under a name already attached earlier in the
thread; the message then claims an attachment that nobody can see. So:

- Every re-render writes new file names with a round number: `contact_sheet_r2.png`,
  `slide_01_r2.png`, `deck_r2.pdf`, `style_r2.json`. Never reuse `slide_01.png` or the
  first deck's PDF name for a later round. The published file uses the `_final` names above.
- After posting, confirm the reply actually carries the files. If a post comes back with no
  attachments, copy the files to fresh names and post them again before saying anything
  else. Do not tell the user a file is attached unless it is.


## What good output looks like


- Setup is one attachment: the user drops their deck in, and the checklist fills in. No downloads, no terminal, no web pages other
- Setting the brand takes one message from the user (deck attached) and one reply from you
  (swatch, five-line summary, "stored").
- Side by side with the company's own deck, a reader should not be able to tell which one
  the agent made: same background, same fonts, same accent colour, same logo corner, same
  footer and page numbers, in a thread where nobody attached anything.
- Refreshing the brand is the same one-message exchange and replaces the old profile.

- One compact review message per round, not a wall of text.
- The user can finish a full restyle with two or three short replies.
- Global edits are applied to every slide the same way.
- Wording and numbers stay identical unless the user used option 5 or 6.
- Undo always works, back to the first version.
- The published file matches the last preview the user approved.

## What to avoid

- Any PyMC Labs branding while this skill is attached.
- Asking the user to run a script, edit a file, or do anything outside Discord.
- Asking the user for a template when a `BRAND PROFILE` message exists.
- Rewording the footer, dropping page numbers, or moving the logo.
- Template content leaking into the analysis deck.
- White chart backgrounds on dark slides, or body text in the display font.
- Silent font substitution. Always say which font was used instead.
- Mentioning sandbox paths. The attachments are the output.
