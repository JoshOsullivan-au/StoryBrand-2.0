---
name: email-nurture
description: "This skill should be used when the user asks for a \"nurture sequence\", \"drip campaign\", \"email sequence\", \"text message campaign\", \"SMS sequence\", \"autoresponder\", \"welcome emails\", \"what do we send after someone downloads\", or \"sales email\". Writes an automated email or text nurture campaign from a BrandScript, with three nurture messages to one offer message, repeating. Campaign step five."
argument-hint: "--slug brandscript-slug [--channel email|text|both]"
allowed-tools: Bash(python3:*) Read Write
---

# Email and text nurture

Sources: Miller, *Building a StoryBrand 2.0* (2025), chapter 15, step five. First edition, Marketing Roadmap, task three. Regular messages remind people the brand exists, even when they delete them unread. The goal of a nurture message is trust, reciprocity and staying familiar, not the sale.

## Input

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" show --slug <slug>
```

## Delivery message first (implementation workbook)

Before the cycle, send the resource the customer asked for. Include: subject and preview text, a thank-you for the request, the resource link, one useful first action, what messages to expect next, sender and contact details, and the unsubscribe or preferences link. This message is not in the books. It closes the loop the lead generator opened.

## Cadence

Weekly. Repeat the cycle:

1. Nurture
2. Nurture
3. Nurture
4. Offer with call to action

Write a few months of messages, let them run, add more later. 2.0 notes some brands never stop the cycle, because no one knows when the customer will have the problem.

## Nurture email formula (2.0)

1. Paragraph 1: talk about a problem.
2. Paragraph 2: offer a plan, idea, recipe or formula that solves it.
3. Paragraph 3: describe life after the problem is solved.
4. Paragraph 4: if possible, sum the advice up as a three-step plan.
5. A PS. Often the only line people read.

Footer: logo, one-liner, direct CTA.

## Offer email formula (2.0)

1. Paragraph 1: the customer's problem.
2. Paragraph 2: the product that solves it.
3. Paragraph 3: life after the problem is solved.
4. Paragraph 4: affirm that buying is the right decision, state the price, name any discount or bonus, and ask for the order. Be direct. A passive offer reads as weak.
5. A PS that repeats the call to action.

## Text messages (2.0)

Keep them short. Send links to useful tools, or limit texts to sale announcements and special offers. Frequent texts keep the brand front of mind long before and after a purchase. Every text sequence needs the customer's consent and an opt-out in each message; confirm the rules for the user's market before sending.

## Automation safeguards (implementation workbook)

Write these down before the sequence goes live:

- Entry condition and audience segment.
- Conditions that stop or change the sequence, for example a purchase or a reply.
- Who handles replies and sales enquiries.
- The post-purchase route, so buyers stop getting the offer.
- Consent and messaging rules to check for the market.
- Unsubscribe and suppression handling.
- The owner.

In the offer email, state the exact price and terms. Use a deadline only if it is real, and say why it exists.

## Procedure

1. Take problems from `problem` and `failure`, plans from `plan`, outcomes from `success`, and repeat the `controlling_idea` in each message.
2. Draft the delivery email, then the first cycle of four emails: subject line, body, PS. Then the safeguards list. For `--channel text` or `both`, draft one short text per email.
3. Each nurture message gives one useful idea the reader can act on today, unrelated to buying.
4. The offer message uses `cta.direct` word for word.
5. Write to `email-nurture-<slug>.md`.

## Notes

- A 20 percent open rate is normal. Unsubscribes clean the list.
