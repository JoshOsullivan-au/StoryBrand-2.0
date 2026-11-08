---
name: on-mission
description: "This skill should be used when the user asks about \"employee engagement\", \"our team doesn't know the story\", \"mission statement isn't working\", \"align the team\", \"onboarding narrative\", \"internal BrandScript\", or \"culture story\". Builds an internal BrandScript with the team as hero and leadership as guide, then a rollout plan. First edition, chapter 13."
argument-hint: "[brand]"
allowed-tools: Bash(python3:*) Read Write
---

# On-mission: internal BrandScript

Source: Miller, *Building a StoryBrand* (2017), chapter 13. *Building a StoryBrand 2.0* (2025) drops this chapter. It keeps one related point in chapter 11: an aspirational identity for customers also gives the team meaning in its work. Treat this skill as first-edition method.

Without a shared story an organisation falls into a "narrative void": each team decides alone and the small differences add up. A mission statement on a wall does not fill it. A story told again and again does.

## Two scripts

- The **customer BrandScript** comes first. Team members must be able to tell the customer story and the company's role as guide. Build it with `[[brandscript]]`.
- The **team BrandScript** puts the team member as hero and leadership as guide. Pay, development, recognition, flexibility and events are the tools the guide offers.

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" init --brand "<brand>" --scope team --subject "<team or whole company>"
```

Fill it with the same sections from the team member's side: what they want from their work, what stands in the way, how leadership shows empathy and authority, the plan, the call to action, what they avoid, what success looks like, who they become, and the controlling idea of the team story.

## Rollout

The five steps from the book:

1. Create the BrandScript with the leadership team.
2. Audit the current mindset: the beliefs that drive behaviour now.
3. Write a specific implementation plan.
4. Change internal communications to carry the story: onboarding, leader talks, meetings, recognition.
5. Name a team that owns the plan.

## Output

Write `on-mission-<slug>.md`: both BrandScripts side by side, the sound bites every team member should be able to say, and the rollout plan with owners. Owners are names the user supplies. Do not invent them.
