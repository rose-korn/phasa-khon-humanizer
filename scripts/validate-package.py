#!/usr/bin/env python3
"""Check the package files of Phasa Khon Humanizer. Uses only the standard library."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Pattern files, the prefix of their pattern IDs, and a size cap.
# Thai has no spaces between words, so every cap is in characters, not words.
PATTERN_FILES = {
    "references/patterns-th.md": ("TH", 40_000),
    "references/patterns-en.md": ("EN", 15_000),
    "references/mixed-th-en.md": ("MX", 6_000),
}
SKILL_MAX_CHARS = 12_000

errors: list[str] = []


def read(relative: str) -> str:
    path = ROOT / relative
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        sys.exit(f"Cannot read {relative}: {error}")


def read_json(relative: str) -> dict:
    try:
        return json.loads(read(relative))
    except json.JSONDecodeError as error:
        sys.exit(f"Fix the JSON in {relative}: {error}")


SKILL = read("SKILL.md")
README = read("README.md")
CHANGELOG = read("CHANGELOG.md")
PLUGIN = read_json(".claude-plugin/plugin.json")
MARKETPLACE = read_json(".claude-plugin/marketplace.json")
CURSOR_PLUGIN = read_json(".cursor-plugin/plugin.json")

# Metadata
metadata = re.match(r"\A---\n(.*?)\n---\n", SKILL, re.DOTALL)
if not metadata:
    sys.exit("SKILL.md must begin with YAML metadata")
yaml = metadata.group(1)

name = re.search(r"(?m)^name:\s*(\S+)\s*$", yaml)
if not name or name.group(1) != PLUGIN.get("name"):
    errors.append("SKILL.md name must match the Claude plugin name")
for manifest, label in ((CURSOR_PLUGIN, "Cursor plugin"),):
    if manifest.get("name") != PLUGIN.get("name"):
        errors.append(f"{label} name must match the Claude plugin name")
if "skills" in CURSOR_PLUGIN:
    errors.append("Omit skills from the Cursor plugin so it loads the root SKILL.md")
if PLUGIN.get("skills") != ["./"]:
    errors.append("Point the Claude plugin skill loader at the repo root")

# Version
skill_version = re.search(r'(?m)^\s+version:\s*["\']?([0-9]+\.[0-9]+\.[0-9]+)', yaml)
changelog_version = re.search(r"(?m)^## ([0-9]+\.[0-9]+\.[0-9]+)$", CHANGELOG)
versions = {
    skill_version.group(1) if skill_version else "missing in SKILL.md",
    changelog_version.group(1) if changelog_version else "missing in CHANGELOG.md",
    str(PLUGIN.get("version")),
    str(CURSOR_PLUGIN.get("version")),
}
if len(versions) != 1:
    errors.append(f"Use one version in SKILL.md, CHANGELOG.md, and both plugins: {sorted(versions)}")

# Description: every manifest uses the first sentence of the SKILL.md description.
description = re.search(r"(?m)^description: \|\n((?:  .*\n)+)", yaml + "\n")
if not description:
    errors.append("Write the SKILL.md description as an indented block")
else:
    full = " ".join(description.group(1).split())
    manifest_descriptions = {
        PLUGIN.get("description", ""),
        CURSOR_PLUGIN.get("description", ""),
        *(p.get("description", "") for p in MARKETPLACE.get("plugins", [])),
    }
    if len(manifest_descriptions) != 1 or not full.startswith(next(iter(manifest_descriptions))):
        errors.append("Use the first sentence of the SKILL.md description in every manifest")

# Every file SKILL.md points to must exist.
for referenced in sorted(set(re.findall(r"`(references/[^`]+)`", SKILL))):
    if not (ROOT / referenced).is_file():
        errors.append(f"SKILL.md points to a missing file: {referenced}")

# Patterns: numbered from 1 without gaps, listed in the README with the same names.
known_ids: set[str] = set()
for relative, (prefix, max_chars) in PATTERN_FILES.items():
    text = read(relative)
    found = [(int(n), title.strip()) for n, title in re.findall(rf"(?m)^### {prefix}-([0-9]+)\. (.+)$", text)]
    numbers = [n for n, _ in found]
    if not numbers or numbers != list(range(1, len(numbers) + 1)):
        errors.append(f"Number {prefix} patterns in {relative} from 1 without gaps: {numbers}")
    known_ids.update(f"{prefix}-{n}" for n in numbers)
    if len(text) > max_chars:
        errors.append(f"Keep {relative} at {max_chars:,} characters or fewer; it has {len(text):,}")

    readme_rows = dict(re.findall(rf"(?m)^\| ({prefix}-[0-9]+) \| (.+?) \|", README))
    for n, title in found:
        pattern_id = f"{prefix}-{n}"
        # Titles may end with a weak-signal marker; the README lists the bare title.
        bare = re.sub(r"\s*\*\((?:weak alone|อ่อน)\)\*$", "", title)
        if pattern_id not in readme_rows:
            errors.append(f"List {pattern_id} in the README pattern table")
        elif readme_rows[pattern_id].strip() != bare:
            errors.append(f"README name for {pattern_id} should be {bare!r}, not {readme_rows[pattern_id]!r}")
    for pattern_id in readme_rows:
        if pattern_id not in known_ids:
            errors.append(f"README lists {pattern_id}, which no pattern file defines")

# Every pattern ID mentioned anywhere must exist.
mentioned_in = {"SKILL.md": SKILL, "README.md": README}
for relative in PATTERN_FILES:
    mentioned_in[relative] = read(relative)
for example in sorted((ROOT / "examples").glob("*.md")):
    mentioned_in[str(example.relative_to(ROOT))] = example.read_text(encoding="utf-8")
for relative, text in mentioned_in.items():
    for pattern_id in sorted(set(re.findall(r"\b(TH|EN|MX)-([0-9]+)\b", text))):
        joined = "-".join(pattern_id)
        if joined not in known_ids:
            errors.append(f"{relative} mentions {joined}, which no pattern file defines")

if len(SKILL) > SKILL_MAX_CHARS:
    errors.append(f"Keep SKILL.md at {SKILL_MAX_CHARS:,} characters or fewer; it has {len(SKILL):,}")

if errors:
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)

print(f"Phasa Khon Humanizer v{next(iter(versions))} is valid ({len(known_ids)} patterns)")
