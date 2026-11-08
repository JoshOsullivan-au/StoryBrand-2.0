# Changelog

## [0.3.0] - 08/11/2026

Adds tools from an independent StoryBrand 2.0 implementation workbook. The workbook is an original template, not book text. Every addition is labelled, and book rules win where the two differ.

### Added
- `skills/brandscript/assets/implementation-workbook.md`: the blank workshop workbook, in Australian spelling, with a field map to the store and the book counts restored.
- `brandscript.py`: a stored `[NEEDS SOURCE]` or `[INPUT NEEDED]` marker is a hard error, reported with its field path.
- `channel-extensions` skill: ad, social post, sales conversation guide, objection record and AI drafting brief, labelled as non-book scaffolds.

### Changed
- `brandscript`: message clarity prep, workshop prompts per section, and guardrails on evidence, stakes, identity wording and agreement terms.
- `messaging-campaign`: sound-bite bank, comprehension test, consistency and placement records, stage questions, asset tracker, measurement plan, change log and final review.
- `one-liner`: spoken, written and short cuts.
- `website-wireframe`: page record and pre-launch check.
- `lead-generator`: scope limit, outline shape, capture and delivery copy.
- `email-nurture`: delivery email before the cycle, and automation safeguards.
- `transformation-stories`: follow-up prompts and an approval record with disclosure.
- `referral-system`: design record and follow-through.

### Fixed
- `brandscript.py set` refuses a section path such as `plan.process`. It used to overwrite the section and make `check` crash. Present since 0.1.0.
- The workbook field map names the full plan fields instead of wildcards.
- `sb7-auditor`: the fallback search now finds installed copies inside a version folder and uses an absolute path.

## [0.2.0] - 08/11/2026

Adds *Building a StoryBrand 2.0* (2025). Where the editions differ, the plugin follows 2.0.

### Added
- Controlling idea: `controlling_idea` field, hard rule and 20-word warning in `brandscript.py`, worksheet section 8, schema 2 with migration from schema 1.
- `messaging-campaign` skill: the 2.0 sound-bite test loop and the seven-step campaign across curiosity, enlightenment and commitment.
- Eval case `missing-controlling-idea`.

### Changed
- `one-liner`: 2.0 three-part formula (problem, product as solution, result). First-edition form kept as an option.
- `website-wireframe`: 2.0 eight landing page sections and the menu-of-products rule.
- `lead-generator`: collects phone numbers as well as email addresses.
- `email-nurture`: email or text, with the 2.0 four-paragraph nurture and offer formulas.
- `referral-system`: bonus links and codes.
- `grunt-test`: covers ads, lead generators and emails; adds story clarity and controlling idea checks; delegates with the plugin root path.
- `on-mission`: marked first edition only.
- `sb7-rules.md`: 2.0 rules marked `(2.0)`.

### Fixed
- Skill frontmatter now parses as strict YAML: quoted `description` and `argument-hint` values.
- Every script call uses `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brandscript.py"`, and every skill that reads the BrandScript names the command.
- `sb7-auditor` takes the plugin root from the caller instead of relying on variable substitution in an agent prompt, and has a `color`.
- Build caches removed from the plugin root.

## [0.1.0] - 08/11/2026

### Added
- `brandscript` orchestrator skill with section rules, a client worksheet template with combined narrative, and a worked example.
- `grunt-test`, `one-liner`, `website-wireframe`, `lead-generator`, `email-nurture`, `transformation-stories`, `referral-system` and `on-mission` skills.
- `sb7-auditor` read-only agent.
- `scripts/brandscript.py` store, checker and renderer (`sections`, `template`, `narrative`), with unit tests.
- One eval case: `brand-as-hero-homepage`.
