# brand-matched-slides

Give Daimon your company's brand once, from Discord, and every deck in every thread comes out
in your template instead of PyMC Labs house style. Nobody runs a script, edits a file, or
connects anything. This guide is written from a full run on a fresh Discord server on
2026-10-10; every step below was done that way, and the snags section lists what went wrong.

## What you need

- A Discord server where Daimon is installed (one-click install at daimon.decision.ai; you must
  be a server admin to add skills).
- Your company's deck as a PDF or PPTX. Any deck that already looks right. Four slides are enough.

## Step 1: install the skills (admin, once per server)

Hosted Daimon's built-in agent is read-only, so skills go on an editable copy. One message does
the fork, both skill adds and the channel routing. Post this in the channel Daimon should
answer in:

```
@Daimon fork Daimon into an editable copy named brand-agent, add both skills from the latest main of https://github.com/JoshElieson/PyMC (folders skills/brand-matched-slides and skills/slide-review), and point this channel at the copy. Yes to all approvals.
```

Daimon opens a thread, forks itself, shows a preview of each skill and posts two approval
cards. Click **Approve** on both. When it says the copy answers new threads in this channel,
you are done. About two minutes.

To update later, send the same message with "re-add both skills, replacing the versions you
have". Daimon refuses to import a skill that fails to parse and keeps the old one, so a bad
update never breaks the agent.

## Step 2: set the brand (anyone, once)

Post a new message in that channel with your deck attached:

```
@Daimon this is our brand template
```

In about a minute Daimon replies with a swatch image, a five-line summary (background and
accent colours, fonts, logo position, footer text, page-number style) and a two-line checklist
with both items ticked. It stores the profile as a message starting `BRAND PROFILE` in a thread
named **Brand profile**, with five files attached: `brand.json`, `style.json`, `logo.png`,
`brand_swatch.png`, `brand_source.pdf`. Pin that message when it asks.

That is the whole setup. If you prefer to be walked through it, `@Daimon set up branded slides`
posts the checklist and asks for the deck; `@Daimon brand status` shows the checklist and the
swatch from any thread, any time.

## Step 3: make decks

In any new message, in any thread, attach your data and ask as you normally would:

```
@Daimon Using channel_spend.csv, which marketing channels drove revenue? Make a 2-slide presentation for our CMO: slide 1 the key chart with the finding as the title, slide 2 the recommendation. Post the PDF and also a PNG image of each slide here in the thread.
```

Daimon finds the stored brand on its own, renders the deck in it, posts the PDF and the slide
images, and then posts a review form (buttons for font, size, colours, style, logo and footer,
a box for text edits, and Publish). Change what you want, submit, and it re-renders only what
changed. Publish PDF or Publish PPTX gives you the final file plus `style.json` for reuse.

To change the brand later, attach a new deck and say `@Daimon update our brand to this`. The
newest `BRAND PROFILE` message wins.

## Snags we hit, and what to do

- **Daimon ignores a message without `@Daimon`.** A bare "yes" or a file dropped in with no
  mention does nothing. Always mention it, including when you attach the deck.
- **A run freezes at "Working on it" for minutes.** The elapsed counter stops updating. Click
  **Stop** under the card, then send `@Daimon retry` with what you wanted. The retry took 40
  seconds in our run.
- **A thread won't load ("Messages Failed To Load").** Threads are disposable. Start again
  with the same message in the channel; nothing is lost because the brand lives in its own
  thread.
- **Posted files sometimes do not arrive** when a file with the same name was attached earlier
  in the thread. The skill now versions every re-render and checks the post. If Daimon says a
  file is attached and you cannot see it, say so and it re-posts under a new name.
- **Editing SKILL.md:** the `description` in the frontmatter must be quoted if it contains a
  colon, or Daimon's import fails with a YAML error.

## Why the brand is stored in Discord and not GitHub

We tried GitHub first. The hosted Daimon GitHub App is read-only for repository contents (its
own description says it reads repos and opens issues and PRs), so every commit to a `brand/`
folder failed with a 403 no matter what was set on the Connect GitHub page, and Daimon cannot
create repos at all. GitHub also added three user steps (install the app with the repo ticked,
connect it, mark it as the working repo). A Discord message needs none of that, works across
threads and channels in the server, and was the proven path on both servers we tested.
Self-hosted Daimon with a write-capable GitHub App could store the same five files in a repo.

## Contents of this folder

- `SKILL.md`: the instructions Daimon follows (Flow 0 setup, Flow A set/refresh brand, Flow B
  make a deck, hand-off to `slide-review`).
- `scripts/extract_brand.py`: PyMuPDF-only extractor. Writes `brand.json`, `logo.png`,
  `brand_swatch.png` and, with `--style`, `style.json` in the `slide-review` schema; `--summary`
  prints the five chat lines. No company data is baked in anywhere.

## Verifying the extraction (judging evidence, not a user step)

Running `scripts/extract_brand.py` on Daimon's output deck should give the same background,
fonts, logo corner and footer as the source deck. On `brand_sources/meridian_board_deck.pdf` it
matches `brand_sources/meridian_brand_truth.json` on all six colours, both fonts, the logo
corner and the footer (`probes/brand_extract_test/`).
