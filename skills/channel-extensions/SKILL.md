---
name: channel-extensions
description: "This skill should be used when the user asks for \"an ad from our BrandScript\", \"a social post\", \"a sales script\", \"discovery call questions\", \"how should sales talk about this\", \"objection handling\", or \"an AI brief for our copywriter\". Drafts ads, social posts, sales conversation guides, objection records and AI drafting briefs from a checked BrandScript. These scaffolds come from an independent implementation workbook, not from either StoryBrand book."
argument-hint: "--slug brandscript-slug --asset ad|social|sales|objections|ai-brief"
allowed-tools: Bash(python3:*) Read Write
---

# Channel extensions

Source: the "Optional channel extensions" section of the independent implementation workbook in `${CLAUDE_PLUGIN_ROOT}/skills/brandscript/assets/implementation-workbook.md`. Neither *Building a StoryBrand* (2017) nor *Building a StoryBrand 2.0* (2025) gives a method for these assets. 2.0 lists sales scripts and social posts as outputs of its own AI tool only. Tell the user these are application tools, not book method.

## Precondition and input

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" check --slug <slug>
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" show --slug <slug>
```

The check exits 0. Every line of every asset traces to a stored field. Repeat the controlling idea and the direct call to action word for word.

## Ad or social post

| Part | Field |
|---|---|
| Audience | `character.customer` |
| Opening line: the problem or desire | `problem.external` or `character.want` |
| Solution in one line | the offer, as in `one_liner` |
| Evidence or demonstration | `guide.authority` (verified only) |
| Desired outcome | `success` |
| Call to action | `cta.direct` or `cta.transitional` |
| Destination and follow-up | landing page, lead generator, nurture sequence |

Run `[[grunt-test]]` on the draft: the first five seconds still have to say what it is, why it helps, and what to do.

## Sales conversation guide

The guide asks, then listens, then follows the BrandScript order. The customer stays the hero.

1. Ask about the outcome they want. (`character.want`)
2. Ask about the practical obstacle. (`problem.external`)
3. Ask how that obstacle affects them. (`problem.internal`)
4. Answer with empathy grounded in what they said. (`guide.empathy`)
5. Give relevant evidence of fit. (`guide.authority`)
6. Propose the plan. (`plan.process`)
7. State conditions or limits honestly. (`plan.agreement`)
8. Invite the next step. (`cta.direct`, with `cta.transitional` as the fallback)

## Objection record

A table: customer concern, clear answer, evidence, person responsible. Seed it from `plan.agreement.items` and the fears behind `failure`. Every answer needs evidence or it does not go in.

## AI drafting brief

For a copywriter or another AI tool. Give it the BrandScript worksheet (`show --format template`) and these rules:

- Use only the approved message sheet.
- Draft the named asset for the named audience and objective.
- Keep the customer central, name the problem and the outcome, and end with the approved call to action.
- Use plain language.
- Do not invent testimonials, credentials, statistics, prices, guarantees or deadlines. Mark gaps `[INPUT NEEDED]`.
- Keep the controlling idea word for word. Separate supported claims from aims.

Record the human reviewer, the facts to verify before publication, and the material that must not go into the AI tool (client confidential data, personal information).

## Output

Write `channel-<asset>-<slug>.md`. Put a first line on every file: "Application scaffold, not StoryBrand book method."
