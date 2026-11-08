---
name: lead-generator
description: "This skill should be used when the user asks for a \"lead magnet\", \"lead generator\", \"free PDF\", \"opt-in offer\", \"how do we grow our email list\", \"collect phone numbers\", \"transitional call to action\", or \"nobody signs up for our newsletter\". Designs a lead generator from a BrandScript (type, title, outline and placement) that collects email addresses and phone numbers. Campaign step four."
argument-hint: "--slug brandscript-slug"
allowed-tools: Bash(python3:*) Read Write
---

# Lead generator

Sources: Miller, *Building a StoryBrand 2.0* (2025), chapter 15, step four. First edition, Marketing Roadmap, task two. A newsletter sign-up promises nothing. A lead generator trades real value for contact details. 2.0 adds phone numbers for text messages, because a text reaches the same screen as family and friends. It is the transitional call to action made concrete.

## Input

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" show --slug <slug>
```

## Two jobs

1. Give the customer real value.
2. Position the brand as the authority in its field.

## Five types

| Type | Best for |
|---|---|
| Downloadable guide (PDF) | Every business. The cheapest place to start. |
| Online course or webinar | Experts selling advice or services |
| Software demo or free trial | Software and subscriptions |
| Free samples | Physical products and food |
| Live events | Local businesses building a community |

## Procedure

1. Read `problem.internal`, `failure`, `plan.process` and `controlling_idea`.
2. Propose three ideas. Each one solves a slice of the problem the paid product solves in full.
3. Give each a title in a proven shape: "5 mistakes people make with...", "10 things to get right before...", "Become a...". Use the controlling idea in the title or subtitle where it fits.
4. For the recommended idea, outline about three pages of content. Be generous. Give the why and a good share of the how. State what the resource will not try to solve, so it stays a slice of the paid offer. A workable outline (from the implementation workbook): acknowledge the problem, one useful principle, three actions or tools, a practical takeaway, an optional next step with the brand.
5. Write the capture and delivery copy: the landing page promise, a contents preview, the required fields (email address and, with consent wording, mobile number), the permission and follow-up wording, the thank-you message, the delivery link and the delivery email subject. Name who owns tracking and follow-up. Add the hand-off line to the first nurture message.
6. Record the title as the transitional CTA if it changed:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" set --slug <slug> cta.transitional "<title>"`

## Placement

A pop-up after about ten seconds, not on arrival. Also in the body of the landing page (section 7 of `[[website-wireframe]]`): mentioning it twice lifts sign-ups. One lead generator per revenue stream once the first one works.

Hand off to `[[email-nurture]]`.
