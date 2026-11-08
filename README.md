# sb7-brandscript

Donald Miller's SB7 messaging framework as a working sequence for Claude Code. Sources: *Building a StoryBrand* (HarperCollins, 2017) and *Building a StoryBrand 2.0* (HarperCollins Leadership, 2025). Where the editions differ, the plugin follows 2.0 and says so.

The customer is the hero. The brand is the guide. Every line of copy comes from one stored, checked BrandScript, and every BrandScript has one controlling idea.

A third source adds workshop and launch tools: an independent StoryBrand 2.0 implementation workbook supplied by Praxis. It is an original template, not book text. The plugin labels every piece it takes from the workbook, and keeps the book rule where the two differ.

The plugin paraphrases the method and cites chapters. It does not reproduce either book. "StoryBrand" is a trademark of StoryBrand. This plugin is not affiliated with or endorsed by StoryBrand or Donald Miller.

## Sequence

The order follows the 2.0 messaging and marketing campaign (chapters 13 and 15).

| Step | Skill | Source | Output |
|---|---|---|---|
| 1 | `brandscript` | 2.0 ch. 3 to 12 | `.sb7/<slug>.json`, client worksheet, combined narrative |
| 1a | `messaging-campaign` | 2.0 ch. 13, 15 | Sound-bite test loop and campaign tracker |
| 2 | `one-liner` | 2.0 ch. 15 | One-liner stored in the BrandScript |
| 3 | `website-wireframe` | 2.0 ch. 14, 15 | `website-wireframe-<slug>.md` (eight sections) |
| 4 | `lead-generator` | 2.0 ch. 15 | Lead generator collecting email and phone |
| 5 | `email-nurture` | 2.0 ch. 15 | `email-nurture-<slug>.md` (email or text) |
| 6 | `transformation-stories` | 2.0 ch. 15 | Testimonial form and case studies |
| 7 | `referral-system` | 2.0 ch. 15 | `referral-system-<slug>.md` |
| Any | `grunt-test` | 1e ch. 2, 12; 2.0 ch. 2, 12, 14 | Pass or fail audit with quoted evidence |
| Any | `on-mission` | 1e ch. 13 only | Team BrandScript and rollout plan |
| Any | `channel-extensions` | Workbook only | Ad, social post, sales conversation guide, objection record, AI brief |

## What the implementation workbook adds

| Addition | Where |
|---|---|
| Blank workshop workbook with a field map to the store | `skills/brandscript/assets/implementation-workbook.md` |
| `[NEEDS SOURCE]` and `[INPUT NEEDED]` block the check | `brandscript.py` |
| Message clarity prep, evidence and permission records, non-shaming stakes | `brandscript`, `references/sb7-rules.md` |
| Sound-bite bank, comprehension test, consistency and placement records | `messaging-campaign` |
| Asset tracker, measurement plan, change log, final review | `messaging-campaign` |
| Spoken, written and short one-liner cuts | `one-liner` |
| Page record and pre-launch check | `website-wireframe` |
| Capture and delivery copy, scope limit | `lead-generator` |
| Delivery email and automation safeguards | `email-nurture` |
| Follow-up prompts and approval record with disclosure | `transformation-stories` |
| Referral design record and follow-through | `referral-system` |
| Ads, social, sales conversation, objections, AI brief | `channel-extensions` |

Agent: `sb7-auditor` runs the grunt test over more than three assets and returns one ranked table.

## What 2.0 changed, and where the plugin carries it

| 2.0 change | Where |
|---|---|
| Controlling idea added to the BrandScript (ch. 12) | `brandscript.py` field and hard rule, worksheet section 8, `brandscript`, `grunt-test` |
| Communication campaign: create, edit until people react, repeat until memorised (ch. 13) | `messaging-campaign` |
| Seven-step campaign across curiosity, enlightenment, commitment (ch. 15) | `messaging-campaign` |
| One-liner in three parts: problem, product as solution, result | `one-liner` |
| Website rule 4: a menu of products under one umbrella problem | `website-wireframe` |
| Eight landing page sections with a value stack in the header | `website-wireframe` |
| Lead generators collect phone numbers too | `lead-generator` |
| Email or text drip, four-paragraph nurture and offer formulas | `email-nurture` |
| Referral bonuses through personal links and codes | `referral-system` |
| Guide does not transform, playful villains, baby-step plans, before and after grid, "X to Y" identity | `references/sb7-rules.md` |
| Company culture chapter removed | `on-mission` marked first edition only |

## BrandScript store

`scripts/brandscript.py` is stdlib-only Python 3.12. It stores one JSON file per BrandScript under `.sb7/` in the project root and enforces the rules the books state as hard limits. Schema 2 adds the controlling idea. A schema 1 file loads and gains an empty controlling idea.

```bash
python3 scripts/brandscript.py init --brand "Tide Books"
python3 scripts/brandscript.py set --slug tide-books-brand character.want "books that are always BAS-ready"
python3 scripts/brandscript.py set --slug tide-books-brand failure "emotional: dread every time the phone rings" --append
python3 scripts/brandscript.py set --slug tide-books-brand controlling_idea "Your weekends should be yours, not your receipts'"
python3 scripts/brandscript.py check --slug tide-books-brand
python3 scripts/brandscript.py show --slug tide-books-brand --format template
```

`show` formats:

| Format | Prints |
|---|---|
| `sections` (default) | Review layout, one heading per section |
| `template` | The client worksheet in `skills/brandscript/assets/brandscript-template.md`, ending with the combined narrative |
| `narrative` | The combined narrative paragraph alone |

Hard rules (exit 1): customer and one want named; villain, external, internal and philosophical problems defined; an empathy statement and at least one authority item; a process plan of 3 to 6 steps; a direct call to action; at least three failure items; at least one success item; identity from and to lines; a controlling idea; no stored `[NEEDS SOURCE]` or `[INPUT NEEDED]` marker.

Warnings: more than one desire or villain, a philosophical problem without should or deserve, more than three testimonials, more than four plan steps, untitled plans, no transitional call to action, a missing failure kind (practical, emotional, opportunity), a missing success kind (practical, feeling), more failure items than success items, and a controlling idea over 20 words.

## Development

```bash
uv run --python 3.12 --with pytest pytest -p no:cacheprovider scripts/
uvx ruff format scripts/ && uvx ruff check scripts/
uv run --python 3.12 --with mypy mypy --strict --cache-dir=/dev/null scripts/brandscript.py
```

## Install

This repo is its own one-plugin marketplace. In Claude Code:

```
/plugin marketplace add JoshOsullivan-au/StoryBrand-2.0
/plugin install sb7-brandscript@sb7-brandscript
```

Python 3.12 or newer must be on the path as `python3`. The script uses the standard library only.

## Not in 0.3.0

No hooks. Two eval cases. No tagline, video, podcast or upsell skill: 2.0 lists these as outputs of its own AI tool but gives no method for them. Ads, social posts and sales conversations are covered only by the workbook scaffolds in `channel-extensions`.
