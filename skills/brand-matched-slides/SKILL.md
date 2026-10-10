---
name: brand-matched-slides
description: Overrides pymc-artifact-style for decks. Use whenever the user asks for slides, a deck, a presentation, or a PDF to present, in any thread, even if nothing is attached. Also use when the user shares a presentation (PDF or PPTX) and calls it their template, brand, style guide or house style, or asks to set, update or refresh the company brand, or asks to set up, get started with, check the status of, or get help with branded slides. The brand profile lives in the bound GitHub repo under brand/, is created by this skill from the user's own deck entirely inside Discord, and is applied to every deck in every thread. Setup is guided step by step in Discord.
---

# Brand-matched slides

**This skill overrides `pymc-artifact-style` for slide decks.** That default skill applies
PyMC Labs house style to every artifact and says never to substitute a client's brand unless
explicitly asked. When this skill is attached, the user *has* asked, permanently: the
company brand stored in the repo is the house style for decks. Keep using
`pymc-artifact-style`'s rendering pipeline (Typst pages to PDF/PPTX) if convenient, but take
every colour, font, logo and footer from `brand.json`, not from the PyMC assets.

The company this agent works for is not PyMC Labs. Never use the PyMC Labs logo, palette or
"PyMC Labs' proposals" footer while this skill is attached.

**Everything happens in Discord.** The user never runs a script, edits a file or opens a
terminal. You extract the brand, store it, and reuse it. Never ask the user to run anything
on their machine.

## Where the brand lives

The brand profile is a folder named `brand/` at the root of the agent's bound GitHub repo:

| File | What it is |
|---|---|
| `brand/brand.json` | tokens extracted from the company's deck (schema below) |
| `brand/style.json` | the same brand mapped into the `slide-review` skill's token schema |
| `brand/logo.png` | logo crop, transparent background, 300 dpi |
| `brand/brand_swatch.png` | one-image summary of the profile, for humans to eyeball |
| `brand/brand_source.pdf` | the deck the tokens came from |

`brand.json` fields: `page_size_points`, `aspect`, `background`, `dark_theme`, `palette[]`,
`text_colors[]`, `fonts[]`, `roles{display, body, primary_accent, secondary_accent, panel,
text, muted_text}`, `logo{kind, bbox_points, corner, relative_width, file}`,
`footer{text, page_number_format, page_number_position, rule}`, `title_decoration`.

This skill ships no brand of its own. The profile is created from the user's deck (Flow A)
and read back in every later thread (Flow B). `brand.json` is the contract: when it exists,
do not re-derive the brand by eye from the PDF.

**If GitHub is not connected or no repo is bound**, run Flow 0 (setup) and come back. Only
if the user declines to connect GitHub use the Discord fallback: post the five files as
attachments in a message that starts with the line `BRAND PROFILE` and, in later threads,
find the newest such message with Discord search and re-fetch the attachments. Prefer the
repo whenever it is available.

## Flow 0: guided setup (first run, "set up", "get started", "status", "help")

Trigger: the user asks to set up, get started, onboard, check status or get help with
branded slides; or this is the first time the skill is used in this server; or Flow A or B
finds a missing prerequisite. The user is guided entirely in Discord. You do every step
you can yourself; the user only clicks, answers a form, or attaches a file. The one thing
you cannot do for them is authorize GitHub, and for that you post the link.

1. **Check the four prerequisites silently**, then post one checklist message with the
   state of each, in this order and wording:

   ```
   Branded slides: setup
   ✅ Skill installed
   ⬜ GitHub connected          (needed to remember your brand across threads)
   ⬜ Repo chosen               (where the brand profile is kept)
   ⬜ Brand set                 (from your company's deck)
   ```
   - *Skill installed* is always ✅ if you are reading this.
   - *GitHub connected* is ✅ when a GitHub MCP tool is available to you in this session.
   - *Repo chosen* is ✅ when you know which repo is bound (memory, `/agent-setup` config,
     or an earlier `brand/` commit you can read).
   - *Brand set* is ✅ when `brand/brand.json` exists in that repo. Post the stored swatch
     under the checklist in that case.

   If all four are ✅, say so in one line, remind the user they can just ask for slides in
   any thread, and stop. Otherwise continue with the **first** ⬜ item only; after it is
   done, re-post the checklist and continue with the next. One step per turn, so the user
   always sees where they are.

2. **GitHub connected.** Start the GitHub connection yourself (connect the GitHub MCP
   server for this agent). That produces an authorization link for the user; post it with
   one line: "Click to authorize GitHub, then reply `done`." That is the only time the user
   leaves Discord, and they come back by replying. If the platform does not let you start
   the connection, say so and give the in-Discord route: run `/agent-setup`, choose
   *Connect an MCP server*, pick GitHub, and reply `done` when finished. When they reply,
   verify the tool is present; if it is not, repeat the link once.

3. **Repo chosen.** On Discord call `post_wizard` with `prompt` = `"Where should the brand
   profile live?"` and one step: key `repo`, kind `choice`, options
   `create` → `Create a private repo for me (recommended)`,
   `existing` → `Use a repo I already have` (allow_custom: true, label "owner/name").
   If `create`: create a private repo named `<server-or-team-name>-brand` on the user's
   GitHub account, with a one-line README, and bind it. If `existing`: verify you can
   read and write it; if not, ask for the `owner/name` again or offer `create`. Without
   `post_wizard`, ask the same question as text with the two options. Remember the
   choice (memory and `/agent-setup` config) so later threads find it without asking.

4. **Brand set.** Ask the user to attach their company deck (PDF or PPTX) in this thread,
   one line: "Attach your company's deck (PDF or PPTX) and I'll learn your brand from it."
   When it arrives, run Flow A. Flow A ends by posting the swatch and summary; then re-post
   the checklist with all four ✅ and one closing line: "Setup complete. Ask for slides in
   any thread and they'll come out in your brand. Want a test deck now?"

5. **Status at any time.** `@Daimon brand status` posts the same checklist (plus swatch when
   the brand is set) without changing anything.

Never ask the user to download, unzip, run or edit anything during setup. Never send them
to a web page except the GitHub authorization link.

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
   and writes `style.json` in the `slide-review` schema. If the script cannot run, do the
   same with PyMuPDF calls by hand and still write the same `brand.json` and `style.json`.
3. **Check.** Open `brand_swatch.png`. If a field is null (no logo, no footer, no fonts) or
   text-on-background contrast is below 4.5:1, fix `brand.json` by hand where the fix is
   obvious, otherwise ask the user one short question. Do not ask when everything was found.
4. **Store.** Copy the template to `brand_source.pdf`. Commit `brand.json`, `style.json`,
   `logo.png`, `brand_swatch.png` and `brand_source.pdf` to `brand/` in the bound repo, replacing any
   previous profile, with the message `Set brand profile from <template filename>`.
   If the repo is unavailable, use the Discord fallback above.
5. **Confirm in one message.** Post `brand_swatch.png` and the `--summary` output (five
   lines: background and accent, fonts, logo, footer, page numbers), then one line: the brand
   is stored and every deck from now on, in any thread, will use it. Offer to make a deck.

## Flow B: make a deck

Trigger: any request for slides, a deck, a presentation or a PDF to present.

1. **Load the profile.** Read `brand/brand.json`, `brand/style.json` and `brand/logo.png` from the bound repo
   (fallback: the newest `BRAND PROFILE` message in this server). Note display font, body
   font, background, primary accent, secondary accent, panel colour, text and muted text
   colours, logo corner and relative width, footer text, page-number format and corner,
   title decoration.
   **If no profile exists anywhere**, run Flow 0 from the first missing step (it ends by
   asking for the deck and running Flow A), then continue here. Do not fall back to PyMC
   branding.

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
   were applied, and any font substitution. Offer PPTX or source on request.

## Single-slide requests

If the user asks for one slide, make exactly one content slide: no title slide, no closing
slide. It still carries the logo, the footer and the page number ("1 / 1"). The finding is
the slide title; the chart fills the body; a source footnote sits above the footer rule.

## Fonts

Company fonts such as Georgia and Calibri are usually not redistributable, so they are not
bundled. If a font named in `brand.json` is missing in the sandbox, substitute by class and
say so in one line of the reply: a serif display font -> Playfair Display (or Source Serif 4),
a sans body font -> Inter. Never fall back to a sans-serif for serif titles.

## Hand-off to the review step (`slide-review` skill)

A companion skill, `slide-review`, lets the user restyle and publish the deck with short
menu codes. It does **not** redo the analysis, so it needs the deck's source and tokens.
After every render, leave these files in the working folder (`/root/work`) with exactly
these names:

- `deck.typ`: the Typst source. All fonts, sizes and colours must come from one `#let`
  block at the top that reads `style.json`; no literal font names or hex colours inside the
  slide bodies. Then a global edit changes one token and every slide follows.
- `style.json`: the review skill's token schema. Start from `brand/style.json` (already
  mapped from the brand profile) and only change `size_name`/`base_size` or
  `style_preset` if the user asked:
  `heading_font, body_font, size_name, base_size, scale, scheme_name, bg, text, primary,
  accent[], panel, style_preset, logo{path,corner,on}, footer{text,on,page_numbers}, slide_size`.
- `slides.json`: one entry per slide: `title`, `bullets[]`, `notes`, `chart_script` (path
  to the script that draws that slide's chart; it must read fonts/colours from `style.json`
  so a restyle re-draws the chart to match).
- `brand.json`, `logo.png`, `brand_swatch.png`, `brand_source.pdf`: copies of the stored
  profile, so the reviewer can check the deck against the source;
- the rendered PDF and one PNG per slide (`slide_01.png`, ...).

Then, in the same turn, **start the `slide-review` round**: post one contact-sheet PNG of
the slides and the current-style line, then (on Discord) call `post_wizard` with the
seven-step "Edit your deck" form that skill specifies, and end your turn. On platforms
without `post_wizard`, post the typed-code menu instead. Do not just post the PDF and stop;
the review loop is the user's chance to fix anything before publishing. When the user later says `✅ publish`, the published file is produced by
`slide-review` from the current `style.json`, and it must still carry the brand (logo,
footer, page numbers) unless the user turned those off with menu 7.

## What good output looks like

- Setup is a checklist the user watches fill in: one click to authorize GitHub, one button
  for the repo, one attachment for the deck. No downloads, no terminal, no web pages other
  than the GitHub authorization link.
- Setting the brand takes one message from the user (deck attached) and one reply from you
  (swatch, five-line summary, "stored").
- Side by side with the company's own deck, a reader should not be able to tell which one
  the agent made: same background, same fonts, same accent colour, same logo corner, same
  footer and page numbers, in a thread where nobody attached anything.
- Refreshing the brand is the same one-message exchange and replaces the old profile.

## What to avoid

- Any PyMC Labs branding while this skill is attached.
- Asking the user to run a script, edit a file, or do anything outside Discord.
- Asking the user for a template when `brand/brand.json` exists.
- Rewording the footer, dropping page numbers, or moving the logo.
- Template content leaking into the analysis deck.
- White chart backgrounds on dark slides, or body text in the display font.
- Silent font substitution. Always say which font was used instead.
- Mentioning sandbox paths. The attachments and the repo commit are the output.
