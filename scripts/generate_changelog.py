#!/usr/bin/env python3
"""Generate docs/changelog.md from git tags and commit messages.

Commit message convention
-------------------------
Commits are expected to start with one of the following prefixes:

  ADD   → Added
  FIX   → Fixed
  CNG   → Changed
  RMV   → Removed

Commits without a recognised prefix (e.g. "Merge …", "Minor change") are
silently skipped.

Usage
-----
    python scripts/generate_changelog.py          # writes docs/changelog.md
    python scripts/generate_changelog.py --dry-run # prints to stdout
"""

from __future__ import annotations

import argparse
import re
import subprocess
from pathlib import Path

REPO_URL = "https://github.com/dongyeoplee2/Malet"

# Map commit‑message prefix → Keep-a-Changelog section header
PREFIX_MAP = {
    "ADD": "Added",
    "FIX": "Fixed",
    "CNG": "Changed",
    "RMV": "Removed",
}

PREFIX_ORDER = ["Added", "Changed", "Fixed", "Removed"]

# Emoji prefixes for section headers (matches GitHub Releases style)
SECTION_EMOJI = {
    "Added": "\u2728",      # ✨
    "Changed": "\U0001f680", # 🚀
    "Fixed": "\U0001fa79",   # 🩹
    "Removed": "\U0001f5d1\ufe0f",  # 🗑️
}


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def get_tags() -> list[tuple[str, str]]:
    """Return ``[(tag, date), …]`` sorted newest-first by date."""
    raw = git(
        "tag", "-l", "--format=%(refname:short) %(creatordate:short)",
        "--sort=-creatordate",
    )
    tags = []
    for line in raw.splitlines():
        parts = line.split(None, 1)
        if len(parts) == 2:
            tags.append((parts[0], parts[1]))
    return tags


def _rev_range(older: str | None, newer: str | None) -> str:
    if older and newer:
        return f"{older}..{newer}"
    if newer:
        return newer
    if older:
        return f"{older}..HEAD"
    return "HEAD"


def commits_between(older: str | None, newer: str | None) -> list[str]:
    """Return one-line commit messages between two refs."""
    raw = git("log", "--oneline", "--format=%s", _rev_range(older, newer))
    return raw.splitlines() if raw else []


def dated_commits_between(
    older: str | None, newer: str | None,
) -> list[tuple[str, str]]:
    """Return ``[(YYYY-MM, message), …]`` between two refs, newest-first."""
    raw = git("log", "--format=%as %s", _rev_range(older, newer))
    results = []
    for line in raw.splitlines():
        if not line:
            continue
        date_str, msg = line.split(None, 1)
        year = date_str[:4]  # YYYY
        results.append((year, msg))
    return results


def classify(messages: list[str]) -> dict[str, list[str]]:
    """Group commit messages by changelog section."""
    sections: dict[str, list[str]] = {s: [] for s in PREFIX_ORDER}
    prefix_re = re.compile(r"^(ADD|FIX|CNG|RMV)\b\s*(.*)", re.IGNORECASE)
    for msg in messages:
        m = prefix_re.match(msg)
        if not m:
            continue
        prefix = m.group(1).upper()
        body = m.group(2).strip()
        # Strip leading punctuation/whitespace
        body = body.lstrip(":- ")
        if not body:
            continue
        section = PREFIX_MAP[prefix]
        sections[section].append(_add_code_backticks(body))
    return sections


def _add_code_backticks(text: str) -> str:
    """Wrap code-like identifiers in backticks for markdown rendering.

    Matches patterns like: ClassName.method, module_name.func, df.applymap,
    __dunder__, -flag_name, `already_backticked`.
    """
    # Don't touch text that already has backticks
    if "`" in text:
        return text
    # Dotted identifiers: ExperimentLog.grid_dict, df.applymap, etc.
    text = re.sub(
        r"(?<![`\w])([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)+)(?![`\w])",
        r"`\1`",
        text,
    )
    # Dunder names: __getitem__, __init__, __future__
    text = re.sub(
        r"(?<![`\w])(__\w+__)(?![`\w])",
        r"`\1`",
        text,
    )
    # CLI tool names: malet-plot, malet-merge
    text = re.sub(
        r"(?<![`\w])(malet-\w+)(?![`\w])",
        r"`\1`",
        text,
    )
    return text


def normalize_tag(tag: str) -> str:
    """Strip tag prefix to get bare version: ``malet-v0.2.1`` → ``0.2.1``."""
    for prefix in ("malet-v", "malt-v"):
        if tag.startswith(prefix):
            return tag[len(prefix):]
    return tag


def render(tags: list[tuple[str, str]]) -> str:
    lines: list[str] = []

    lines.append("# Changelog\n")
    lines.append(
        "Malet currently uses [**Effort-based Versioning (EffVer)**]"
        "(https://jacobtomlinson.dev/effver/): "
        "minor bumps reflect the scope of changes rather than strict API "
        "compatibility guarantees. "
        "We plan to migrate to [Semantic Versioning](https://semver.org/) "
        "once the API stabilises.\n"
    )
    lines.append(
        "Each release is published on "
        f"[GitHub Releases]({REPO_URL}/releases) "
        "with downloadable assets and full commit diffs.\n"
    )
    lines.append("---\n")

    # --- Unreleased ---------------------------------------------------------
    latest_tag = tags[0][0] if tags else None
    dated = dated_commits_between(latest_tag, "HEAD")

    if dated:
        # Group by year-month, preserving order (newest-first)
        from collections import OrderedDict
        months: OrderedDict[str, list[str]] = OrderedDict()
        for ym, msg in dated:
            months.setdefault(ym, []).append(msg)

        lines.append("## Unreleased\n")
        for ym, msgs in months.items():
            sections = classify(msgs)
            if not any(sections.values()):
                continue
            lines.append(f"#### {ym}\n")
            for header in PREFIX_ORDER:
                items = sections[header]
                if items:
                    emoji = SECTION_EMOJI.get(header, "")
                    lines.append(f"**{emoji} {header}**\n")
                    for item in items:
                        lines.append(f"- {item}")
                    lines.append("")
        lines.append("---\n")

    # --- Tagged releases ----------------------------------------------------
    for i, (tag, date) in enumerate(tags):
        version = normalize_tag(tag)
        older_tag = tags[i + 1][0] if i + 1 < len(tags) else None

        msgs = commits_between(older_tag, tag)
        sections = classify(msgs)

        heading = f"## [{version}]({REPO_URL}/releases/tag/{tag}) — {date}\n"
        lines.append(heading)

        has_content = False
        for header in PREFIX_ORDER:
            items = sections[header]
            if items:
                has_content = True
                emoji = SECTION_EMOJI.get(header, "")
                lines.append(f"### {emoji} {header}\n")
                for item in items:
                    lines.append(f"- {item}")
                lines.append("")

        if not has_content:
            lines.append("*No categorised changes.*\n")

        if i < len(tags) - 1:
            lines.append("---\n")

    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate changelog from git tags")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print to stdout instead of writing file",
    )
    parser.add_argument(
        "-o", "--output",
        default=None,
        help="Output path (default: docs/changelog.md)",
    )
    args = parser.parse_args()

    tags = get_tags()
    content = render(tags)

    if args.dry_run:
        print(content)
        return

    out = Path(args.output) if args.output else Path(__file__).resolve().parent.parent / "docs" / "changelog.md"
    out.write_text(content, encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
