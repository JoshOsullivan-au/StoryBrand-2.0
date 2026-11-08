---
name: referral-system
description: "This skill should be used when the user asks for a \"referral program\", \"word of mouth system\", \"affiliate program\", \"friends and family discount\", \"how do we get more referrals\", \"customer evangelists\", or \"refer a friend\". Designs a referral system from a BrandScript covering who to ask, what they share, the reward and the automation. Campaign step seven."
argument-hint: "--slug brandscript-slug"
allowed-tools: Bash(python3:*) Read Write
---

# Referral system

Sources: Miller, *Building a StoryBrand 2.0* (2025), chapter 15, step seven. First edition, Marketing Roadmap, task five. Most businesses say word of mouth brings their customers, yet few have a system that creates it.

## Input

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" show --slug <slug>
```

## Steps

1. **Identify the ideal existing customers.** Repeat buyers and the customers with the best results. Keep them in their own list.
2. **Make sharing easy (2.0).** Email or text that list with a bonus for telling friends: a month free, or a discount code. Give each customer their own link, or a "friends and family" coupon code they can pass on. For a high-ticket product, a landing page per referrer.
3. **Give them a useful tool to share.** A short video or PDF that solves the friend's problem. Asking for friends' email addresses makes customers feel used.
4. **Offer a reward.** A gift or credit per sign-up, or an affiliate commission (the book uses 10 percent as an example).
5. **Automate it.** Add a customer to the referral campaign after one or two orders, through the CRM. Take them out after a few sends so the brand does not nag.

## Procedure

1. Read `problem`, `success`, `controlling_idea` and `cta.transitional`.
2. Propose the shareable asset. It can reuse the lead generator from `[[lead-generator]]`.
3. Draft the referral email: thanks, the asset, a line on helping their friends and giving them the credit, and a PS offering an in-person introduction.
4. Propose one reward model with numbers the user confirms.
5. Write the automation rules: entry trigger, number of sends, exit rule.
6. Write the design record (from the implementation workbook): who is eligible to refer, what evidence of a good experience comes before the ask, the moment to ask, the benefit for the referred person, the reward terms and how it is fulfilled, any disclosure or policy review needed, and the programme owner.
7. Write the follow-through: how referrals are recorded, who answers introductions, how rewards are checked and paid, and how the referrer is thanked.
8. Write to `referral-system-<slug>.md`.

## Patterns from the book

Refund after three referrals in a term. Invite-a-friend coupons. An open-house party at a finished job. A free follow-up session in exchange for referrals.
