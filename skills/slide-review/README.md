# slide-review (Track 03 skill)

**Job:** after Daimon makes a slide deck, let the user review it and restyle the whole deck
(font, size, colour scheme, style, text, order, logo and footer) with short menu codes in
Discord, then publish the final PDF/PPTX.

This is the second half of the workflow:

```
A: uploads template once ("this is our brand") → D: extracts brand, commits brand/ to the repo
A (any later thread): I want slides → D: reads brand/ from the repo, makes slides
→ [slide-review] D: sends for review → A: edits with menu codes → A: publish → D: publishes
```

## Attach

In the team channel, run `/agent-setup`, add a skill, and paste `SKILL.md`.

## Hand-off contract

The deck-building skill should leave `deck.typ` and `style.json` in the session
(see `example_style.json` for the token schema). If `style.json` is missing,
slide-review creates it from `deck.typ` first.

## Demo script (Discord, interactive)

On Discord the review round is a `post_wizard` form with buttons and a dropdown, so the demo
is click-driven:

1. Daimon posts the contact sheet + current-style line, then the "Edit your deck" form.
2. Click through: Font → Keep · Size → **L** · Colour → Template · Style → Corporate ·
   Logo & footer → all ticked · Text → `1 title: Search returns $3 per $1; display cannot be told from zero`
   · Action → **Apply and preview** → Submit.
3. Daimon echoes `✔ Size → L · ✔ Slide 1 title updated`, re-renders, posts a new sheet + form.
4. Next form: leave everything, Action → **↩ Undo last round** → Submit. Title reverts.
5. Next form: Action → **✅ Publish PDF** → Submit. Final PDF + `style.json` attached.

## Demo script (typed codes, fallback)

In a thread where Daimon just made a deck (e.g. the probe 1 thread,
`probes/before/slides_before_cmo_deck.pdf`):

1. `@Daimon review the slides` → contact sheet + main menu
2. `3` → colour sub-menu, with the current option marked
3. `3c` → dark scheme applied to every slide
4. `1b 2c` → serif fonts, large size, in one reply
5. `5 1 title: Search drives 60% of revenue`
6. `↩ undo` → title change reverted
7. `✅ publish` → final PDF + `style.json` attached

Pass criteria: each round changes only what was asked; undo works; the published PDF
matches the last preview.
