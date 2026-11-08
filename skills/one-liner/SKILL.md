---
name: one-liner
description: "This skill should be used when the user asks for a \"one-liner\", \"elevator pitch\", \"what do you do answer\", \"logline for our business\", \"tagline that explains what we do\", or needs a short repeatable statement for a website, email signature, bio or business card. Builds a one-liner from a checked BrandScript with the StoryBrand 2.0 three-part formula (problem, product as solution, result) and a test loop. Campaign step two."
argument-hint: "--slug brandscript-slug"
allowed-tools: Bash(python3:*) Read
---

# One-liner

Sources: Miller, *Building a StoryBrand 2.0* (2025), chapter 15, step two. First edition, Marketing Roadmap, task one. It works like a film logline: it is clear and it makes a promise, so the listener understands the offer and wants more.

## Precondition

`python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" check --slug <slug>` exits 0. If it does not, run `[[brandscript]]` first.

## Formula (2.0)

Three parts, in this order:

1. **The problem.** The problem is the hook. Open with the customer's conflict so the listener thinks "yes, I struggle with that". Naming the customer inside the problem is fine: "If you're a busy mum and can't find time to train...".
2. **The product as solution.** Short. "That's why we created X", then stop. Features here dilute it. Explaining belongs to enlightenment material, not to the one-liner.
3. **The result.** A clear picture of life after the problem is solved.

The first edition used four parts (character, problem, plan, success). The 2.0 form drops the plan and leads with the problem. Use the 2.0 form unless the user asks for the older one.

Take the problem from `problem.external` or `problem.internal`, the product from the brand's offer, and the result from `success` or `identity.to`.

## Procedure

1. Draft three versions. Vary the problem: external, internal, and one in the customer's own words.
2. Check each: problem first, product part under about ten words, no jargon, no company history, under 40 words in total.
3. For the recommended draft, write three cuts (from the implementation workbook): a spoken version, a written version, and a short version for tight spaces such as a social bio. Keep the same words where the cuts overlap.
4. Recommend one. Record it:
   `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" set --slug <slug> one_liner "<text>"`
5. Give the user the test loop: say it to friends, customers and strangers. Keep editing until people ask for a card or how to buy.

## Where it goes

Memorised by the founder and every team member, so the whole team becomes a sales force. On the website, in the email signature, on business cards, in social bios and on packaging. Repeat it until it feels like overkill.
