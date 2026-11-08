---
name: transformation-stories
description: "This skill should be used when the user asks for \"testimonials\", \"case studies\", \"customer stories\", \"a testimonial form\", \"video testimonial questions\", \"social proof\", or \"our testimonials are weak\". Builds a five-question interview that produces transformation stories, then turns the answers into short testimonials and case studies. Campaign step six."
argument-hint: "--slug brandscript-slug"
allowed-tools: Bash(python3:*) Read Write
---

# Transformation stories

Sources: Miller, *Building a StoryBrand 2.0* (2025), chapter 15, step six. First edition, Marketing Roadmap, task four. Asking for a testimonial gets praise about the person ("Nancy is great"). Asking the right questions gets a story of change, with specifics. A good testimonial gives future customers the gift of going second.

## Input

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" show --slug <slug>
```

## The five questions

Use them as a form or as a recorded interview. They follow a story arc.

1. What problem did you have before you found us?
2. What did the frustration feel like while you tried to solve it?
3. What was different about our product or service?
4. Take us to the moment you realised it was working.
5. What is life like now the problem is solved, or being solved?

## Follow-up prompts (implementation workbook)

Not from the books. Use them when an answer is thin, or to keep the story honest:

- What made you hesitate before deciding, and what helped you decide?
- Which specific change can you point to?
- What else may have contributed to that result?
- Who would you say this suits?

## Approval record (implementation workbook)

Before any story is used, record:

- The exact wording the customer approved.
- Results checked where possible.
- Permission for name, image and organisation.
- Any incentive or other connection that must be disclosed.
- Approved channels, and an expiry date if there is one.
- The approval date.

## Procedure

1. Write the form with the brand's product name in each question. Add an interview record: customer name and role, offer used, dates, interviewer, where the recording lives.
2. When answers arrive, cut each into:
   - one short testimonial (one or two sentences, a specific result),
   - one case study (before, struggle, guide, turning point, after).
3. Map each story to the BrandScript: question 1 to `problem.external`, 2 to `problem.internal`, 5 to `success` and `identity.to`.
4. Add the best short testimonial as authority:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" set --slug <slug> guide.authority "testimonial: <text>" --append`
5. Use only real answers. Never write a testimonial for a customer. Do not use a story until its approval record is complete.

## Where they go

Website guide and value sections, nurture emails, sales pages, keynotes, events, podcast or video close.
