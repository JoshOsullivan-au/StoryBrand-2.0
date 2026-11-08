---
name: messaging-campaign
description: "This skill should be used when the user asks to \"roll out our message\", \"build a marketing campaign from our BrandScript\", \"what do we do after the BrandScript\", \"StoryBrand marketing campaign\", \"messaging and marketing campaign\", \"test our sound bites\", \"get people to remember our message\", or wants the full implementation plan for a brand. Runs the StoryBrand 2.0 communication campaign: test and refine the sound bites, then build the seven campaign pieces in order across curiosity, enlightenment and commitment."
argument-hint: "--slug brandscript-slug"
allowed-tools: Bash(python3:*) Read Write
---

# Messaging campaign

Source: Miller, *Building a StoryBrand 2.0* (2025), chapters 13 and 15. The first edition calls the same idea the Marketing Roadmap, with five tasks. 2.0 has seven steps.

A clear message is clear to the brand. It is not clear to anyone else until the brand says it again and again. Run the brand as if its product were running for office.

## Precondition

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" check --slug <slug>
```

Exit 0. If not, run `[[brandscript]]` first.

## Part A: the communication campaign (chapter 13)

1. **Create the BrandScript.** Done in the precondition.
2. **Edit the sound bites until they get the reaction.** Ask the user to say the one-liner and the controlling idea to real people. The right reaction: people ask how to buy, ask for a card, or name someone who should buy. The wrong reaction: people ask what it means. Then the sound bite is too vague. Rewrite it, record it with `set`, and test again. Judge only by whether customers lean in and order, not by how much the team likes the line.
3. **Repeat the sound bites until the public has them memorised.** Use the same words every time. The book's estimate: a person needs to hear a message about eight times, and most commercial messages are ignored, so plan for far more repetitions than feels natural. Put the sound bites in pitches, the website, lead generators, videos, signage, email, sales calls, ads and podcast openings.

## Part B: the seven campaign pieces (chapter 15)

Build them in this order. Each one adds to the last. The campaign moves people through three stages:

| Stage | What the customer does | Collateral |
|---|---|---|
| Curiosity | Suspects the brand can help | One-liner, landing page header, ads |
| Enlightenment | Checks whether it is right for them | Lead generator, nurture emails or texts, videos, testimonials |
| Commitment | Places an order | Sales emails, offers, clear direct calls to action |

| Step | Piece | Skill |
|---|---|---|
| 1 | BrandScript | `[[brandscript]]` |
| 2 | One-liner | `[[one-liner]]` |
| 3 | Landing page wireframe | `[[website-wireframe]]` |
| 4 | Lead generator that collects email addresses and phone numbers | `[[lead-generator]]` |
| 5 | Automated email or text drip campaign | `[[email-nurture]]` |
| 6 | Transformation stories | `[[transformation-stories]]` |
| 7 | Referral system | `[[referral-system]]` |

## Part C: test, track and measure (implementation workbook)

These tools come from the independent implementation workbook in `${CLAUDE_PLUGIN_ROOT}/skills/brandscript/assets/implementation-workbook.md` ("Refine and repeat", "Relationship stages" and "Optional launch controls"). They are not from either book. They make Part A step 2 and the campaign trackable.

**Sound-bite bank.** One row per purpose: identify the customer, name the problem, express empathy, convey the solution, establish credibility, explain the plan, show success, state the stakes, invite action. Columns: draft phrase, audience reaction, approved phrase.

**Comprehension test.** After each test, record: who reviewed it and how close they are to the audience; what they thought was offered; who they thought it was for; what benefit they remembered; what they thought to do next; the first question they asked; what confused them; the revision to test next.

**Consistency record.** Owner of the approved message, where the current sheet lives, channels to update, old wording to retire, team briefing date, review date and the criteria for a change.

**Placement record.** For each touchpoint (website, email, sales conversation, ads and social, print and events): the direct call to action, the transitional call to action, and the owner.

**Stage questions.** Curiosity answers "is this relevant?". Enlightenment answers "how does it work, and can it help?". Commitment answers "what will it take to proceed?". Name the route for someone ready to buy now and for someone who needs more time.

**Asset tracker.** For each piece: owner, status, approval date, launch location.

**Measurement plan.** For each question, a metric, baseline, target, data source and review date: do people understand the offer, do visitors act, are leads suitable, does follow-up engage, do prospects proceed, does delivery keep the promise, do customers refer.

**Change log.** Observed problem, evidence, proposed change, what was held constant, result and limits, decision (keep, revise, remove), next review. Change one thing at a time.

## Procedure

1. Run Part A step 2 with the user, using the sound-bite bank and comprehension test. Record any changed sound bites with `set`.
2. Write `messaging-campaign-<slug>.md`: the sound bites to memorise (controlling idea, one-liner, direct and transitional calls to action), the placement record, the stage questions, and the asset tracker with the seven pieces at status `todo`, `drafted` or `live`. Owners and dates are names and dates the user supplies. Do not invent them.
3. Run each piece's skill in order. Update the tracker as each one lands.
4. Before launch, run the final review below. After launch, fill the measurement plan and keep the change log.
5. When the campaign is live, build the next one. 2.0 recommends one campaign per major product or division.

## Final review (workbook)

- One main customer and desire are clear.
- The central obstacle and the three problem levels fit together.
- The brand acts as a credible guide.
- The plan is understandable and the commitments are deliverable.
- Direct and transitional calls to action are specific.
- Failure stakes are credible and proportionate.
- Success is concrete and fairly qualified.
- The identity shift does not demean the starting point.
- The controlling idea is clear and repeatable.
- The one-liner gives problem, solution and result.
- Sound bites have been tested for comprehension.
- Every asset uses the approved message.
- Lead capture and follow-up work end to end.
- Customer stories are accurate and approved.
- Referral terms and owners are clear.
- Owners, review dates and evidence standards are recorded.

## Not covered

The StoryBrand.AI tool also produces taglines, sales scripts, video and social scripts, podcast prompts, urgency ideas and upsell ideas. The book names these outputs but gives no method for them, so this plugin does not claim one. `[[channel-extensions]]` offers non-book scaffolds for ads, social posts and sales conversations, labelled as such.
