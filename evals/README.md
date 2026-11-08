# Evals

One case per folder. `prompt.md` is the user turn. Each file in `graders/` is one pass or fail rule for an LLM judge.

| Case | Skill under test | What it catches |
|---|---|---|
| `brand-as-hero-homepage` | `grunt-test` | Copy that makes the company the hero, a missing direct CTA, and numeric scores |
| `missing-controlling-idea` | `grunt-test` | A differentiator buried mid-page instead of stated above the fold (2.0 ch. 12), and a CTA whose wording changes |

Cases to add before 1.0.0: a BrandScript run with two desires in the want, a one-liner that does not open with the problem, and a nurture sequence that sells in every email.

The deterministic rules have unit tests instead: `uv run --python 3.12 --with pytest pytest -p no:cacheprovider scripts/`.
