---
name: brandscript
description: "This skill should be used when the user asks to \"build a BrandScript\", \"clarify our message\", \"do StoryBrand for\", \"run SB7 on\", \"position the customer as the hero\", \"find our controlling idea\", \"our messaging is confusing\", \"what should our website say\", or needs one core message for a brand, division, product, customer segment or internal team. Orchestrates the seven SB7 sections, the identity transformation and the controlling idea in strict order, one decision per section, stored and checked by a deterministic script. Every other skill in this plugin reads the BrandScript it produces."
argument-hint: "[brand] [--scope brand|division|product|segment|team] [--subject name]"
allowed-tools: Bash(python3:*) Read Grep Glob
---

# BrandScript: orchestrator

Build one BrandScript for one brand and one scope. The rules for each section are in `references/sb7-rules.md`. The client worksheet and combined narrative are in `assets/brandscript-template.md`. The full blank workshop workbook is in `assets/implementation-workbook.md`. A worked example is in `examples/worked-example.md`.

Sources: Miller, *Building a StoryBrand* (HarperCollins, 2017), chapters 3 to 11, and *Building a StoryBrand 2.0* (HarperCollins Leadership, 2025), chapters 3 to 12. Where the editions differ, follow 2.0.

The core rule: the customer is the hero. The brand is the guide. Each section becomes a sound bite the brand repeats. Every line that does not serve a section is noise and gets cut.

## The sections, in order

1. **Character.** The customer and the one thing they want, tied to survival (save money, save time, gain status, belong, be generous, find meaning).
2. **Problem.** One villain. Then the external problem it causes, the internal frustration that causes, and the philosophical reason it is wrong.
3. **Guide.** One empathy statement. Then authority: testimonials, statistics, awards or logos. The guide stays confident and does not change. The spotlight stays on the hero.
4. **Plan.** A process plan of 3 to 6 baby steps with a name. An agreement plan only if a fear stops the sale.
5. **Call to action.** One direct call to action. One transitional call to action.
6. **Failure.** At least three things the customer avoids: practical consequences, emotional consequences, opportunities they could miss. A pinch, not a pile.
7. **Success.** Practical results and how they feel.
8. **Identity.** "We help our customers go from X to Y."
9. **Controlling idea.** What the whole story is about, in one simple line the customer can repeat. Added in 2.0, chapter 12. If the brand keeps only one sound bite, it keeps this one.

## Procedure

### 0. Name the brand and the scope

Take `$ARGUMENTS`. If empty, ask for the brand name and what the script covers. Start with the whole brand. Division, product and segment scripts come after the brand script. Use `--scope team` only through `[[on-mission]]`.

### 1. Initialise the store

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" init --brand "<brand>" --scope <scope> [--subject "<name>"]
```

The command prints a slug. The script lives at `.sb7/<slug>.json` under the project root. If it exists, run `show` and continue from the first empty section. Ask before `--force`. A first-edition file (schema 1) loads with an empty controlling idea.

### 2. Gather the raw material

Read what the user supplies: current website copy, pitch decks, sales call notes, reviews, client context packs. Do not invent facts about the customer. Where a section needs a fact you do not have (a statistic, an award, a real testimonial), mark it `[NEEDS SOURCE]` or `[INPUT NEEDED]` and ask. `check` fails while either marker is stored, so no unverified claim reaches copy.

For a workshop, or when the raw material is thin, work through `assets/implementation-workbook.md` with the user. Start with its message clarity worksheet: the plain-language explanation, the customer relevance table (money, time, safety, belonging, status, capability, meaning), and what belongs in the first impression versus later. Its field map shows which answers go into the store. Collect the customer's own words where you can: they make the best sound bites.

### 3. Work each section in order

For each section:

1. Brainstorm 3 to 5 candidates from the raw material, using the prompts in `references/sb7-rules.md`.
2. Show them to the user with one recommended pick and the rule it best satisfies.
3. Record the decision:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" set --slug <slug> <field> "<value>" [--append]
```

Fields: `character.customer`, `character.want`, `problem.villain`, `problem.external`, `problem.internal`, `problem.philosophical`, `guide.empathy`, `guide.authority` (append, `testimonial|statistic|award|logo: text`), `plan.process.title`, `plan.process.steps` (append), `plan.agreement.title`, `plan.agreement.items` (append), `cta.direct`, `cta.transitional`, `failure` (append, `practical|emotional|opportunity: text`), `success` (append, `practical|feeling: text`), `identity.from`, `identity.to`, `controlling_idea`, `one_liner`.

Write each value in the shape the combined narrative needs. The shapes are in the table at the end of `assets/brandscript-template.md`.

Do not skip ahead. Each section depends on the one before it. Find the controlling idea last: read the finished script and ask "what is this story about?" or "what is the moral of the story we invite the customer into?".

### 4. Check

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" check --slug <slug>
```

Exit 1 means a hard rule failed. Fix every error before any copy is written from the script. Read each warning to the user and let them decide.

### 5. Hand off

Print the client worksheet. It follows `assets/brandscript-template.md` and ends with the combined narrative:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" show --slug <slug> --format template
```

`--format narrative` prints the combined narrative alone. `--format sections` (the default) prints the review layout. The narrative is a first draft built by fixed rules. Edit it for grammar and voice before a client sees it, and keep every claim in it traceable to a stored field.

Treat the BrandScript as a rough draft. 2.0 says the most common fault is sound bites that are too vague: be clear, not clever. Then hand off to `[[messaging-campaign]]`, which tests the sound bites and runs the seven campaign pieces in order. Use `[[grunt-test]]` at any point to audit existing copy against the script.

## Guardrails

- One desire, one villain, one controlling idea. Extra desires belong in division or product scripts.
- The brand never appears as the hero. Rewrite any line where the company is the subject of an achievement the customer wants.
- Authority claims need a source. No invented numbers, awards or quotes. Record verification and permission for each item, as in the workbook's authority table.
- Stakes are credible and proportionate. They do not shame the customer, and conditional outcomes are not stated as certain.
- The identity "from" line describes a starting point without demeaning it.
- Agreement plan promises match real policy and delivery capability, with their real terms.
- Client deliverables follow the Praxis voice. Compose with `praxis-brand-voice` when that plugin is installed.
