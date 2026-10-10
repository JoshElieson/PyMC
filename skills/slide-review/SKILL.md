---
name: slide-review
description: Always use right after a slide deck has been rendered in the thread (even if the user only asked for a PDF or PNGs), or when the user asks to review, edit, restyle or publish slides (font, font size, colours, style, slide text, order, logo, footer). Runs a numbered-menu review loop in Discord, applies edits across the whole deck, and publishes the final PDF/PPTX.
---

# Slide review: edit with menus, then publish

## When this skill runs

Every time a deck has just been rendered, without exception. A request for "the PDF", "a
PNG per slide", a fixed slide count, or "fixed deliverables" is a description of the
output, not an instruction to skip review. Post what was asked for, then post the review
round in the same turn. Skip only if the user said "no review" or "publish directly" in
this thread, and say that you skipped it because they asked.

The deck is already made (by the deck-building skill). Your job now is to let the user
review it and make easy edits with short menu codes, without redoing the analysis, then
publish. Discord has no dropdowns here, so the menus below act as dropdowns: the user
replies with a number to open a menu and a number+letter to choose (`3c`). They can
combine codes in one reply (`1b 2c 4a`).

## Inputs (from the deck-building step)

- `deck.typ`: Typst source of the deck
- `style.json`: every visual token: `heading_font, body_font, base_size, scale, bg, text,
  primary, accent[], style_preset, logo{path,corner,on}, footer{text,on,page_numbers},
  slide_size`
- `slides.json` (optional): per-slide title, bullets, notes, chart script

If `style.json` is missing, first create it by moving every hard-coded font, size and
colour in `deck.typ` into one `#let` block that reads `style.json`. After that, each global
edit changes exactly one token and applies to every slide.

## On Discord: use the `post_wizard` tool, not typed codes

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

## Step 1: Post the review message (typed-code fallback)

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

## Step 2: Sub-menus

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

## Step 3: Apply edits

1. Parse every code in the reply. Before rendering, echo what you understood on one line:
   `✔ Font → Serif · ✔ Colours → Dark · ✔ Slide 1 title updated`.
   If one code is unclear, apply the clear ones and ask about that code only.
2. Save the current `style.json` (and `slides.json` / `deck.typ` if text or order changes)
   as version `v<n>` before changing anything. `↩ undo` restores the previous version.
3. Change only the tokens or slide text that were asked for. Never regenerate the
   content, re-run the model, or rewrite slides the user didn't touch.
4. Run the checks below, re-render, then post Step 1 again (contact sheet, current-style
   line, main menu). `👀 preview <n>` posts slide n at full size only.

## Step 4: Checks before every render

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

## Step 5: Publish

On `✅ publish` (PDF) or `📎 publish pptx`:
1. Final render from the current version. It must match the last preview exactly.
2. Attach `<Company>_<topic>_<YYYY-MM-DD>_final.pdf` (or `.pptx`) and
   `<Company>_style_<YYYY-MM-DD>.json` so the same look can be reused in a later thread
   ("use this style.json").
3. One closing line: slide count plus a summary of the edits made, e.g.
   `Published 5 slides · Serif, L, Dark, Corporate · 2 text edits`.
Never mention sandbox paths like `/mnt/session/outputs`. The attachments are the output.

## Attachments: new names every round, and check they arrived

Discord silently drops a file that is re-sent under a name already attached earlier in the
thread; the message then claims an attachment that nobody can see. So:

- Every re-render writes new file names with a round number: `contact_sheet_r2.png`,
  `slide_01_r2.png`, `deck_r2.pdf`, `style_r2.json`. Never reuse `slide_01.png` or the
  first deck's PDF name for a later round. The published file uses the `_final` names above.
- After posting, confirm the reply actually carries the files. If a post comes back with no
  attachments, copy the files to fresh names and post them again before saying anything
  else. Do not tell the user a file is attached unless it is.

## What good output looks like

- One compact review message per round, not a wall of text.
- The user can finish a full restyle with two or three short replies.
- Global edits are applied to every slide the same way.
- Wording and numbers stay identical unless the user used option 5 or 6.
- Undo always works, back to the first version.
- The published file matches the last preview the user approved.
