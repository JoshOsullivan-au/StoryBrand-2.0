# Worked example: Tide Books (fictional)

A fictional bookkeeping firm for Australian sole-trader tradies. Every fact is invented to show the shape. Do not reuse it as client evidence.

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py" init --brand "Tide Books"
# prints: tide-books-brand
```

| Section | Decision | Rule it serves |
|---|---|---|
| Section | Field and value | Rule it serves |
|---|---|---|
| Character | `character.customer`: sole-trader tradies. `character.want`: books that are always BAS-ready | One desire, tied to conserving money and time |
| Villain | `problem.villain`: the shoebox of receipts | Root cause, relatable, singular, real |
| External | `problem.external`: receipts and invoices never get reconciled | Tangible problem |
| Internal | `problem.internal`: behind and anxious about every BAS deadline | The frustration that makes them call |
| Philosophical | `problem.philosophical`: a good tradie should not lose weekends to paperwork | Uses "should" |
| Empathy | `guide.empathy`: We know the dread of a BAS letter on a Friday afternoon | Speaks to the internal problem |
| Authority | `guide.authority`: `statistic: 1,200 tradies kept BAS-ready since 2019 [NEEDS SOURCE]` | Competence. `check` fails while the marker is stored. Remove it only once the number is verified. |
| Plan | `plan.process.title`: The Clean Books Plan. Steps: book a 15-minute call; snap receipts in the app; we lodge on time | 3 steps, named |
| Direct CTA | `cta.direct`: book a call | One wording, repeated |
| Transitional CTA | `cta.transitional`: download the BAS-ready checklist | Free, builds reciprocity |
| Failure | `practical: ATO penalties`. `emotional: dread every time the phone rings`. `opportunity: missed deductions` | One of each kind, a pinch |
| Success | `practical: BAS lodged early`. `practical: every deduction claimed`. `feeling: calm at tax time` | Specific, more than failure |
| Identity | `identity.from`: behind and anxious. `identity.to`: on top of the numbers | How they want mates to see them |
| Controlling idea | `controlling_idea`: Your weekends should be yours, not your receipts' | The moral of the story, under 20 words, repeatable |

`show --format narrative` then prints this first draft:

> Our customer, sole-trader tradies, wants books that are always BAS-ready. But the shoebox of receipts stands in their way, leaving them feeling behind and anxious about every BAS deadline. They believe a good tradie should not lose weekends to paperwork. We understand the dread of a BAS letter on a Friday afternoon and have demonstrated our ability to help through 1,200 tradies kept BAS-ready since 2019. Our plan is simple: book a 15-minute call, snap receipts in the app, then we lodge on time. We invite them to book a call. By acting, they can avoid ATO penalties, dread every time the phone rings and missed deductions and achieve BAS lodged early, every deduction claimed and calm at tax time, moving from behind and anxious to on top of the numbers.

The draft keeps every fact but reads stiffly in the last sentence. Edit it for voice before a client sees it.

One-liner, 2.0 form (problem, product as solution, result):

> Most tradies lose their weekends to a shoebox of receipts. That's why we created Tide Books. Your BAS goes in on time and your weekends are yours again.

One-liner, first-edition form (character, problem, plan, success):

> Tradies lose weekends to a shoebox of receipts. Tide Books reconciles them as you go and lodges your BAS on time, so your weekends are yours again.
