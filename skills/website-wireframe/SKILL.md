---
name: website-wireframe
description: "This skill should be used when the user asks to \"rewrite our homepage\", \"wireframe the website\", \"build a landing page\", \"what should go above the fold\", \"StoryBrand website\", or \"fix our landing page\", or wants a page outline built from a BrandScript. Produces the StoryBrand 2.0 eight-section landing page wireframe with copy, checked against the five website best practices. Campaign step three."
argument-hint: "--slug brandscript-slug"
allowed-tools: Bash(python3:*) Read Write
---

# Website wireframe

Sources: Miller, *Building a StoryBrand 2.0* (2025), chapters 14 and 15 (step three). First edition, chapter 12. The BrandScript is the drum kit. The website is the drum solo. No word on the page comes from outside the BrandScript.

Wireframing is also how the brand clarifies its own offer: putting the sound bites in order shows where the offer is still vague.

## Precondition and input

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" check --slug <slug>
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" show --slug <slug>
```

The check exits 0. The controlling idea must be set: it is the line above the fold.

## The five best practices (2.0, chapter 14)

1. **An offer above the fold.** Short, bold, customer-centred. It promises an aspirational identity, promises to solve a problem, or states exactly what the business does. The controlling idea belongs here.
2. **Obvious calls to action.** The direct call to action top right and in the centre of the header. Same wording, same brighter colour, repeated down the page. It leads to a transaction ("buy now", "schedule a call", "add to bag"). The transitional call to action sits beside it, quieter.
3. **Images of success.** People enjoying the result, and products in the hands of happy customers. Not the building.
4. **A menu of products, all solving one umbrella problem.** List what people can buy. A service business packages its services into named products. A complex business finds one umbrella message, then gives each product or division its own page and BrandScript.
5. **Very few words.** People scan. Aim for about ten sentences of visible copy. Long text goes behind "read more".

## The eight sections (2.0, chapter 15)

Produce the wireframe in this order. For each section give the copy, the image brief and the BrandScript field it comes from.

| Section | Content | Field |
|---|---|---|
| 1. Header | Large-text offer (controlling idea), direct CTA, transitional CTA, optional value stack of a few bullets | `controlling_idea`, `cta`, `success` |
| 2. Stakes | Negative consequences of not acting. Near the top: the problem is the hook | `failure`, `problem` |
| 3. Value proposition | Swing back to positive. A fuller version of the header offer, bullets or a testimonial | `success`, `identity.to` |
| 4. Guide | Empathy, then competence | `guide` |
| 5. Plan | Three steps that clear the last confusion before ordering | `plan.process` |
| 6. Explanatory paragraph | A few paragraphs for due diligence, behind "read more" if long | `one_liner`, all fields |
| 7. Lead generator ad | The lead generator again, in the body as well as the pop-up | `cta.transitional` |
| 8. Junk drawer | Links, history, careers, legal: everything once thought important | none |

Add or remove sections only with a reason the user accepts.

## Page record (implementation workbook)

Start the wireframe file with: page name and URL, audience and traffic source, primary action, secondary action, and the main message to remember (the controlling idea). In the lead generator section, list the form fields, button wording, delivery confirmation and the privacy link. In the guide section, note each proof item's verification and permission status.

## Pre-launch check (implementation workbook)

- A new visitor can name the offer, the benefit and the next action.
- The primary action wording is the same everywhere.
- Copy is short and scannable, and the detail stays available below the fold.
- Images show the customer outcome.
- Multiple offers have clear labels and routes.
- Forms, links, mobile layouts and confirmation steps work.
- Claims and permissions have been checked.

## Output

Write the wireframe to `website-wireframe-<slug>.md` in the project. Run `[[grunt-test]]` on the result, then the pre-launch check, before handing it over.
