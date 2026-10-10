---
name: slide-review
description: Use right after a slide deck has been rendered in the thread, or when the user asks to review, edit, restyle or publish slides (font, font size, colours, style, slide text, order, logo, footer). Runs a numbered-menu review loop in Discord, applies edits across the whole deck, and publishes the final PDF/PPTX.
---

# Slide review: edit with menus, then publish

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

## Step 1: Post the review message

Always post one message, in this order:
1. One contact-sheet PNG of all slides in a grid, numbered, sized for an inline Discord
   preview (about 1600 px wide). Don't post one image per slide.
2. The current-style line, e.g.
   `Font: Playfair / Inter · Size: M · Colours: Navy & Coral · Style: Corporate`
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
2. Attach `<Company>_<topic>_<YYYY-MM-DD>.pdf` (or `.pptx`) and `style.json` so the same
   look can be reused in a later thread ("use this style.json").
3. One closing line: slide count plus a summary of the edits made, e.g.
   `Published 5 slides · Serif, L, Dark, Corporate · 2 text edits`.
Never mention sandbox paths like `/mnt/session/outputs`. The attachments are the output.

## What good output looks like

- One compact review message per round, not a wall of text.
- The user can finish a full restyle with two or three short replies.
- Global edits are applied to every slide the same way.
- Wording and numbers stay identical unless the user used option 5 or 6.
- Undo always works, back to the first version.
- The published file matches the last preview the user approved.
