#!/usr/bin/env python3
"""Validate a Malas Engineer skill directory.

Checks:
  - SKILL.md frontmatter: name, description, license
  - name format and directory match
  - SKILL.md line count (<= 500)
  - every reference linked from SKILL.md exists
  - no orphan reference files
  - reference links are one level deep

Usage:
  python3 scripts/validate_skill.py [skill_dir]

Exit codes:
  0  all checks pass
  1  one or more checks fail
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

MAX_LINES = 500
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    block = text[4:end]
    body = text[end + 4 :]
    data: dict[str, str] = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data, body


def main() -> int:
    skill_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    skill_md = skill_dir / "SKILL.md"
    errors: list[str] = []
    warnings: list[str] = []

    if not skill_md.exists():
        print(f"FAIL: SKILL.md not found in {skill_dir}")
        return 1

    text = skill_md.read_text(encoding="utf-8")
    fm, _ = parse_frontmatter(text)

    name = fm.get("name", "")
    description = fm.get("description", "")
    license_name = fm.get("license", "")

    if not name:
        errors.append("frontmatter: missing 'name'")
    elif not NAME_RE.match(name):
        errors.append(f"frontmatter: invalid name '{name}' (lowercase letters, digits, hyphens)")
    elif name != skill_dir.name:
        errors.append(f"frontmatter: name '{name}' does not match directory '{skill_dir.name}'")

    if not description:
        errors.append("frontmatter: missing 'description'")
    elif len(description) > 1024:
        errors.append(f"frontmatter: description is {len(description)} chars, max 1024")

    if not license_name:
        warnings.append("frontmatter: no 'license' field")

    lines = text.count("\n") + 1
    if lines > MAX_LINES:
        errors.append(f"SKILL.md has {lines} lines, max {MAX_LINES}")

    linked = set(re.findall(r"\((references/[^)]+)\)", text))
    ref_dir = skill_dir / "references"
    existing = {f"references/{p.name}" for p in ref_dir.glob("*.md")} if ref_dir.exists() else set()

    for link in sorted(linked):
        if not (skill_dir / link).exists():
            errors.append(f"SKILL.md links missing file: {link}")

    for orphan in sorted(existing - linked):
        warnings.append(f"reference not linked from SKILL.md: {orphan}")

    for link in sorted(linked):
        depth = link.count("/")
        if depth > 1:
            errors.append(f"reference is nested too deep: {link}")

    print(f"Skill: {skill_dir}")
    print(f"Name: {name or '(missing)'}")
    print(f"Lines: {lines}/{MAX_LINES}")
    print(f"References linked: {len(linked)}")

    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"FAIL: {error}")

    if errors:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"\nPASS ({len(warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
