# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Deterministic store, checker and renderer for an SB7 BrandScript.

The BrandScript lives at `.sb7/<slug>.json` under the project root
(`CLAUDE_PROJECT_DIR`, else the working directory). Skills write one
decision per section with `set`, then run `check` before any copy is
drafted from the script.

Commands:
    init    Create a blank BrandScript for a brand and a scope.
    set     Write one field by dotted path. `--append` adds to a list.
    show    Print the BrandScript as Markdown. `--format template` prints the
            client worksheet. `--format narrative` prints the combined
            narrative paragraph.
    check   Apply the SB7 rules. Exit 1 when any hard rule fails.
    list    List BrandScripts in the store.

Rules come from Miller, *Building a StoryBrand* (2017), chapters 4 to 11,
and *Building a StoryBrand 2.0* (2025), chapters 4 to 12, which adds the
controlling idea. See `skills/brandscript/references/sb7-rules.md`.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 2
CONTROLLING_IDEA_SOFT_MAX_WORDS = 20
UNVERIFIED_MARKERS = ("[NEEDS SOURCE]", "[INPUT NEEDED]")
STORE_DIR_NAME = ".sb7"
SCOPES = ("brand", "division", "product", "segment", "team")
AUTHORITY_TYPES = ("testimonial", "statistic", "award", "logo")
FAILURE_KINDS = ("practical", "emotional", "opportunity")
SUCCESS_KINDS = ("practical", "feeling")
TYPED_FIELDS: dict[str, tuple[str, ...]] = {
    "guide.authority": AUTHORITY_TYPES,
    "failure": FAILURE_KINDS,
    "success": SUCCESS_KINDS,
}
FORMATS = ("sections", "template", "narrative")
EMPATHY_LEAD = re.compile(r"^\s*we\s+(understand|know|get)\s+(that\s+|how\s+)?", re.IGNORECASE)
PLAN_MIN_STEPS = 3
PLAN_MAX_STEPS = 6
PLAN_SOFT_MAX_STEPS = 4
FAILURE_MIN_ITEMS = 3
TESTIMONIAL_SOFT_MAX = 3
PHILOSOPHICAL_MARKERS = ("should", "shouldn't", "should not", "deserve", "deserves", "ought")
MULTI_DESIRE_PATTERN = re.compile(r"\b(and|or|plus|as well as)\b|[;,/&]", re.IGNORECASE)

LIST_FIELDS = {
    "guide.authority",
    "plan.process.steps",
    "plan.agreement.items",
    "failure",
    "success",
}


@dataclass(frozen=True)
class Finding:
    """One rule result from `check`.

    Attributes:
        level: "error" fails the check. "warn" is advisory.
        section: The BrandScript section the rule covers.
        rule: Short rule id.
        message: Plain statement of what is wrong.
    """

    level: str
    section: str
    rule: str
    message: str


def project_root() -> Path:
    """Return the project root used for the store."""
    return Path(os.environ.get("CLAUDE_PROJECT_DIR") or Path.cwd())


def slugify(text: str) -> str:
    """Convert a brand name and scope into a file-safe slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "brandscript"


def store_path(slug: str, root: Path | None = None) -> Path:
    """Return the JSON path for a BrandScript slug."""
    return (root or project_root()) / STORE_DIR_NAME / f"{slug}.json"


def blank_script(brand: str, scope: str, subject: str) -> dict[str, Any]:
    """Build an empty BrandScript with every section present."""
    return {
        "schema": SCHEMA_VERSION,
        "brand": brand,
        "scope": scope,
        "subject": subject,
        "character": {"customer": "", "want": ""},
        "problem": {"villain": "", "external": "", "internal": "", "philosophical": ""},
        "guide": {"empathy": "", "authority": []},
        "plan": {
            "process": {"title": "", "steps": []},
            "agreement": {"title": "", "items": []},
        },
        "cta": {"direct": "", "transitional": ""},
        "failure": [],
        "success": [],
        "identity": {"from": "", "to": ""},
        "controlling_idea": "",
        "one_liner": "",
    }


def migrate(data: dict[str, Any]) -> dict[str, Any]:
    """Bring an older BrandScript up to SCHEMA_VERSION in place.

    Schema 1 (first edition) had no controlling idea.
    """
    if data.get("schema", 1) < 2:
        data.setdefault("controlling_idea", "")
        data["schema"] = 2
    return data


def load(path: Path) -> dict[str, Any]:
    """Read a BrandScript from disk.

    Raises:
        SystemExit: If the file does not exist.
    """
    if not path.exists():
        raise SystemExit(f"No BrandScript at {path}. Run `init` first.")
    data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return migrate(data)


def save(path: Path, data: dict[str, Any]) -> None:
    """Write a BrandScript to disk as indented JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def set_field(data: dict[str, Any], dotted: str, value: str, append: bool) -> None:
    """Write one value into the BrandScript by dotted path.

    Typed list entries take the form `type: text`, for example
    `statistic: 400 villas managed since 2019` for `guide.authority`,
    `emotional: Dread every BAS letter` for `failure`, or
    `feeling: Calm at tax time` for `success`.

    Args:
        data: The BrandScript to change in place.
        dotted: Path such as `problem.internal` or `plan.process.steps`.
        value: The text to write.
        append: Add to a list field instead of replacing it.

    Raises:
        SystemExit: If the path is unknown or the list rules are broken.
    """
    keys = dotted.split(".")
    node: Any = data
    for key in keys[:-1]:
        if not isinstance(node, dict) or key not in node:
            raise SystemExit(f"Unknown field: {dotted}")
        node = node[key]
    leaf = keys[-1]
    if not isinstance(node, dict) or leaf not in node:
        raise SystemExit(f"Unknown field: {dotted}")
    if isinstance(node[leaf], dict):
        fields = ", ".join(f"{dotted}.{key}" for key in node[leaf])
        raise SystemExit(f"{dotted} is a section, not a field. Set one of: {fields}")

    if dotted in LIST_FIELDS:
        item: Any = parse_typed(value, dotted) if dotted in TYPED_FIELDS else value
        if append:
            node[leaf].append(item)
        else:
            node[leaf] = [item]
        return
    if append:
        raise SystemExit(f"{dotted} holds one value. Remove --append.")
    node[leaf] = value


def parse_typed(value: str, field: str) -> dict[str, str]:
    """Split `type: text` into a typed list entry for `field`.

    Raises:
        SystemExit: If the type is not allowed for the field.
    """
    allowed = TYPED_FIELDS[field]
    kind, _, text = value.partition(":")
    kind = kind.strip().lower()
    if kind not in allowed or not text.strip():
        raise SystemExit(f"{field} entries must be `type: text` with type in: {', '.join(allowed)}")
    return {"type": kind, "text": text.strip()}


def texts(entries: list[dict[str, str]], kind: str | None = None) -> list[str]:
    """Return the text of typed entries, optionally filtered by type."""
    return [entry["text"] for entry in entries if kind is None or entry["type"] == kind]


def join_phrases(items: list[str]) -> str:
    """Join phrases as `a`, `a and b`, or `a, b and c`."""
    cleaned = [item.strip().rstrip(".") for item in items if item.strip()]
    if len(cleaned) <= 1:
        return cleaned[0] if cleaned else "[empty]"
    return f"{', '.join(cleaned[:-1])} and {cleaned[-1]}"


def check(data: dict[str, Any]) -> list[Finding]:
    """Apply the SB7 rules to a BrandScript.

    Returns:
        Findings in section order. Any "error" means the script is not
        ready to drive copy.
    """
    found: list[Finding] = []

    def add(level: str, section: str, rule: str, message: str) -> None:
        found.append(Finding(level, section, rule, message))

    character = data["character"]
    if not character["customer"].strip():
        add("error", "character", "customer-named", "Name the customer. The customer is the hero, not the brand.")
    want = character["want"].strip()
    if not want:
        add("error", "character", "want-defined", "Define one thing the customer wants. No want, no story gap.")
    elif MULTI_DESIRE_PATTERN.search(want):
        add("warn", "character", "single-desire", f"The want reads as more than one desire: '{want}'. Keep one.")

    problem = data["problem"]
    for part in ("villain", "external", "internal", "philosophical"):
        if not problem[part].strip():
            add("error", "problem", f"{part}-defined", f"Define the {part} problem.")
    if problem["villain"] and MULTI_DESIRE_PATTERN.search(problem["villain"]):
        add("warn", "problem", "single-villain", "The villain reads as more than one. One villain is enough.")
    philosophical = problem["philosophical"].lower()
    if philosophical and not any(marker in philosophical for marker in PHILOSOPHICAL_MARKERS):
        add(
            "warn",
            "problem",
            "philosophical-ought",
            "State the philosophical problem with should, shouldn't or deserve.",
        )

    guide = data["guide"]
    if not guide["empathy"].strip():
        add("error", "guide", "empathy", "Write one empathy statement about the internal problem.")
    if not guide["authority"]:
        add("error", "guide", "authority", "Add at least one testimonial, statistic, award or logo.")
    testimonials = [entry for entry in guide["authority"] if entry["type"] == "testimonial"]
    if len(testimonials) > TESTIMONIAL_SOFT_MAX:
        add("warn", "guide", "testimonial-count", f"{len(testimonials)} testimonials. Three is enough to start.")

    steps = data["plan"]["process"]["steps"]
    if len(steps) < PLAN_MIN_STEPS or len(steps) > PLAN_MAX_STEPS:
        add(
            "error",
            "plan",
            "process-steps",
            f"Process plan has {len(steps)} steps. Use 3 to 6. Group more into phases.",
        )
    elif len(steps) > PLAN_SOFT_MAX_STEPS:
        add("warn", "plan", "process-steps-soft", f"{len(steps)} steps. Three or four read faster.")
    if steps and not data["plan"]["process"]["title"].strip():
        add("warn", "plan", "plan-title", "Give the process plan a name. A name raises its value.")
    agreement = data["plan"]["agreement"]
    if agreement["items"] and not agreement["title"].strip():
        add("warn", "plan", "agreement-title", "Give the agreement plan a name.")

    cta = data["cta"]
    if not cta["direct"].strip():
        add("error", "cta", "direct", "Write one direct call to action. Customers do not act unless asked.")
    if not cta["transitional"].strip():
        add("warn", "cta", "transitional", "Add a transitional call to action for customers not ready to buy.")

    failure = data["failure"]
    success = data["success"]
    if len(failure) < FAILURE_MIN_ITEMS:
        add("error", "failure", "failure-count", f"{len(failure)} failure items. Write at least 3.")
    for kind in FAILURE_KINDS:
        if failure and not texts(failure, kind):
            add(
                "warn", "failure", f"failure-{kind}", f"No {kind} consequence. Cover practical, emotional, opportunity."
            )
    if not success:
        add("error", "success", "success-defined", "List what life looks like after the problem is solved.")
    elif len(failure) > len(success):
        add("warn", "success", "salt-ratio", "More failure than success items. Fear is salt. Use a pinch.")
    for kind in SUCCESS_KINDS:
        if success and not texts(success, kind):
            add("warn", "success", f"success-{kind}", f"No {kind} success item. Cover practical results and feelings.")

    identity = data["identity"]
    for end in ("from", "to"):
        if not identity[end].strip():
            add("error", "identity", f"identity-{end}", f"Fill the identity '{end}' line.")

    idea = data["controlling_idea"].strip()
    if not idea:
        add("error", "controlling-idea", "controlling-idea", "State the controlling idea: the one point to repeat.")
    elif len(idea.split()) > CONTROLLING_IDEA_SOFT_MAX_WORDS:
        add("warn", "controlling-idea", "controlling-idea-length", "The controlling idea is long. State it simply.")

    for path, text in iter_strings(data):
        for marker in UNVERIFIED_MARKERS:
            if marker in text:
                section = path.split(".")[0].replace("_", "-")
                add("error", section, "unverified", f"{path} still holds {marker}. Verify it or remove it.")

    return found


def iter_strings(node: Any, path: str = "") -> list[tuple[str, str]]:
    """List every string value in a BrandScript with its dotted path.

    List items use their index, for example `guide.authority.0.text`.
    """
    if isinstance(node, str):
        return [(path, node)]
    if isinstance(node, dict):
        children: list[tuple[str, Any]] = list(node.items())
    elif isinstance(node, list):
        children = [(str(index), item) for index, item in enumerate(node)]
    else:
        return []
    found: list[tuple[str, str]] = []
    for key, child in children:
        found += iter_strings(child, f"{path}.{key}" if path else key)
    return found


def render(data: dict[str, Any], fmt: str = "sections") -> str:
    """Render a BrandScript in one of FORMATS.

    Args:
        data: The BrandScript.
        fmt: "sections" for the review layout, "template" for the
            client worksheet layout, "narrative" for the combined
            narrative paragraph.
    """
    if fmt == "template":
        return render_template(data)
    if fmt == "narrative":
        return render_narrative(data)
    return render_sections(data)


def render_template(data: dict[str, Any]) -> str:
    """Render the BrandScript in the client worksheet layout (assets/brandscript-template.md)."""

    def value(text: str) -> str:
        return text.strip() or "[empty]"

    def joined(entries: list[dict[str, str]], kind: str | None = None) -> str:
        return "; ".join(texts(entries, kind)) or "[empty]"

    problem = data["problem"]
    plan = data["plan"]
    steps = plan["process"]["steps"] or ["[empty]", "[empty]", "[empty]"]
    lines = [
        f"# BrandScript worksheet: {data['brand']} ({data['scope']}: {data['subject']})",
        "",
        "## 1. A character",
        "Who is your customer, and what do they want?",
        "",
        f"* Our customer is: {value(data['character']['customer'])}",
        f"* They want: {value(data['character']['want'])}",
        "",
        "## 2. Has a problem",
        "What prevents them from getting what they want?",
        "",
        f"* Villain, the root cause: {value(problem['villain'])}",
        f"* External problem, the practical obstacle: {value(problem['external'])}",
        f"* Internal problem, how it makes them feel: {value(problem['internal'])}",
        f"* Philosophical problem, why this should not be this way: {value(problem['philosophical'])}",
        "",
        "## 3. Meets a guide",
        "Why should they trust your business to help?",
        "",
        f"* Empathy, how we demonstrate understanding: {value(data['guide']['empathy'])}",
        f"* Authority, evidence that we can help: {joined(data['guide']['authority'])}",
        "",
        "## 4. Gives them a plan",
        "What clear steps will help them move forward?",
        "",
    ]
    if plan["process"]["title"]:
        lines += [f"Plan name: {plan['process']['title']}", ""]
    lines += [f"{index}. {step}" for index, step in enumerate(steps, start=1)]
    agreement = "; ".join(plan["agreement"]["items"]) or "[empty]"
    lines += [
        "",
        f"* Agreements or commitments that reduce their concerns: {agreement}",
        "",
        "## 5. Calls them to action",
        "What should they do next?",
        "",
        f"* Direct call to action: {value(data['cta']['direct'])}",
        f"* Transitional call to action: {value(data['cta']['transitional'])}",
        "",
        "## 6. Helps them avoid failure",
        "What happens if they do not take action?",
        "",
        f"* Practical consequences: {joined(data['failure'], 'practical')}",
        f"* Emotional consequences: {joined(data['failure'], 'emotional')}",
        f"* Opportunities they could miss: {joined(data['failure'], 'opportunity')}",
        "",
        "## 7. Ends in success",
        "What does their life look like after the problem is solved?",
        "",
        f"* Practical results: {joined(data['success'], 'practical')}",
        f"* How they feel: {joined(data['success'], 'feeling')}",
        f"* Who they become: From {value(data['identity']['from'])} to {value(data['identity']['to'])}",
        "",
        "## 8. Controlling idea",
        "What is this story about? The one point to repeat everywhere.",
        "",
        f"* Controlling idea: {value(data['controlling_idea'])}",
        "",
        "## Combined narrative",
        "",
        render_narrative(data),
        "",
    ]
    return "\n".join(lines)


def render_narrative(data: dict[str, Any]) -> str:
    """Fill the six-sentence combined narrative from the BrandScript.

    The output is a first draft. The skill edits it for voice before
    any client sees it.
    """

    def value(text: str) -> str:
        return text.strip().rstrip(".") or "[empty]"

    problem = data["problem"]
    empathy = EMPATHY_LEAD.sub("", data["guide"]["empathy"]).strip().rstrip(".") or "[empty]"
    steps = data["plan"]["process"]["steps"]
    if len(steps) >= 2:
        plan = f"{', '.join(step.rstrip('.') for step in steps[:-1])}, then {steps[-1].rstrip('.')}"
    else:
        plan = join_phrases(steps)
    sentences = [
        f"Our customer, {value(data['character']['customer'])}, wants {value(data['character']['want'])}.",
        f"But {value(problem['villain'])} stands in their way, leaving them feeling {value(problem['internal'])}.",
        f"They believe {value(problem['philosophical'])}.",
        f"We understand {empathy} and have demonstrated our ability to help through "
        f"{join_phrases(texts(data['guide']['authority']))}.",
        f"Our plan is simple: {plan}.",
        f"We invite them to {value(data['cta']['direct'])}.",
        f"By acting, they can avoid {join_phrases(texts(data['failure']))} and achieve "
        f"{join_phrases(texts(data['success']))}, moving from {value(data['identity']['from'])} "
        f"to {value(data['identity']['to'])}.",
    ]
    return " ".join(sentences)


def render_sections(data: dict[str, Any]) -> str:
    """Render a BrandScript as Markdown for review or hand-off."""
    problem = data["problem"]
    plan = data["plan"]
    lines = [
        f"# BrandScript: {data['brand']} ({data['scope']}: {data['subject']})",
        "",
        "## 1. Character",
        f"- Customer: {data['character']['customer'] or '_empty_'}",
        f"- Wants: {data['character']['want'] or '_empty_'}",
        "",
        "## 2. Has a problem",
        f"- Villain: {problem['villain'] or '_empty_'}",
        f"- External: {problem['external'] or '_empty_'}",
        f"- Internal: {problem['internal'] or '_empty_'}",
        f"- Philosophical: {problem['philosophical'] or '_empty_'}",
        "",
        "## 3. Meets a guide",
        f"- Empathy: {data['guide']['empathy'] or '_empty_'}",
    ]
    lines += [f"- Authority ({entry['type']}): {entry['text']}" for entry in data["guide"]["authority"]]
    lines += ["", "## 4. Who gives them a plan", f"Process plan: {plan['process']['title'] or '_untitled_'}"]
    lines += [f"{index}. {step}" for index, step in enumerate(plan["process"]["steps"], start=1)]
    if plan["agreement"]["items"]:
        lines.append(f"Agreement plan: {plan['agreement']['title'] or '_untitled_'}")
        lines += [f"- {item}" for item in plan["agreement"]["items"]]
    lines += [
        "",
        "## 5. And calls them to action",
        f"- Direct: {data['cta']['direct'] or '_empty_'}",
        f"- Transitional: {data['cta']['transitional'] or '_empty_'}",
        "",
        "## 6. That helps them avoid failure",
    ]
    lines += [f"- ({entry['type']}) {entry['text']}" for entry in data["failure"]] or ["- _empty_"]
    lines += ["", "## 7. And ends in success"]
    lines += [f"- ({entry['type']}) {entry['text']}" for entry in data["success"]] or ["- _empty_"]
    lines += [
        "",
        "## Identity transformation",
        f"- From: {data['identity']['from'] or '_empty_'}",
        f"- To: {data['identity']['to'] or '_empty_'}",
        "",
        "## Controlling idea",
        data["controlling_idea"] or "_empty_",
        "",
        "## One-liner",
        data["one_liner"] or "_empty_",
        "",
    ]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="Create a blank BrandScript.")
    init.add_argument("--brand", required=True)
    init.add_argument("--scope", choices=SCOPES, default="brand")
    init.add_argument("--subject", default="", help="Division, product, segment or team name. Defaults to the brand.")
    init.add_argument("--force", action="store_true", help="Overwrite an existing BrandScript.")

    for name in ("set", "show", "check"):
        command = sub.add_parser(name)
        command.add_argument("--slug", required=True)
        if name == "set":
            command.add_argument("field")
            command.add_argument("value")
            command.add_argument("--append", action="store_true")
        if name == "show":
            command.add_argument("--format", choices=FORMATS, default="sections")
        if name == "check":
            command.add_argument("--json", action="store_true", help="Print findings as JSON.")

    sub.add_parser("list", help="List BrandScripts in the store.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command line. Returns the process exit code."""
    args = build_parser().parse_args(argv)

    if args.command == "list":
        store = project_root() / STORE_DIR_NAME
        for path in sorted(store.glob("*.json")) if store.exists() else []:
            print(path.stem)
        return 0

    if args.command == "init":
        subject = args.subject or args.brand
        slug = slugify(
            f"{args.brand}-{args.scope}-{subject}" if subject != args.brand else f"{args.brand}-{args.scope}"
        )
        path = store_path(slug)
        if path.exists() and not args.force:
            print(f"BrandScript exists: {slug}. Use --force to overwrite.", file=sys.stderr)
            return 1
        save(path, blank_script(args.brand, args.scope, subject))
        print(slug)
        return 0

    path = store_path(args.slug)
    data = load(path)

    if args.command == "set":
        set_field(data, args.field, args.value, args.append)
        save(path, data)
        return 0

    if args.command == "show":
        print(render(data, args.format))
        return 0

    findings = check(data)
    errors = [finding for finding in findings if finding.level == "error"]
    if args.json:
        print(json.dumps([finding.__dict__ for finding in findings], indent=2))
    else:
        for finding in findings:
            print(f"{finding.level.upper():5} {finding.section}/{finding.rule}: {finding.message}")
        print(f"{len(errors)} error(s), {len(findings) - len(errors)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
