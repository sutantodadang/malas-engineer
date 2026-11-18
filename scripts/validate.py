#!/usr/bin/env python3
"""Validate package inputs and links; this does not measure agent behavior."""
import json
import os
import re
import sys
from pathlib import Path

from validate_skill import parse_frontmatter

REQUIRED = (
    'README.md', 'AGENTS.md', 'CLAUDE.md', 'LICENSE',
    'install/installer.py', 'install/malas-engineer.pyz',
    'evals/cases.json', 'evals/rubric.json',
    'skills/malas-engineer/references/decision-cards.md', 'references/research-synthesis.md',
    'references/activation-and-evals.md', 'skills/malas-engineer/references/universal-application.md',
    'examples/go-contract/app/service.go', 'examples/go-contract/app/service_test.go',
    'examples/python-contract/catalog/service.py',
    'examples/python-contract/tests/test_service.py',
    'examples/typescript-contract/service.ts', 'examples/typescript-contract/service.test.ts',
    'examples/typescript-contract/package.json', 'examples/typescript-contract/package-lock.json',
    'scripts/architecture_audit.py', 'scripts/test_architecture_audit.py',
)
SKIP = {'.git', '.venv', 'venv', 'node_modules', '__pycache__'}


def require(condition, message):
    # Validation must also run under python -O / PYTHONOPTIMIZE.
    if not condition:
        raise ValueError(message)


def validate(root):
    for rel in ('skills/malas-engineer/SKILL.md', *REQUIRED):
        require((root / rel).is_file(), f'missing {rel}')
    text = (root / 'skills/malas-engineer/SKILL.md').read_text(encoding='utf-8')
    header, _ = parse_frontmatter(text)
    require(header.get('name') == 'malas-engineer', 'invalid skill name')
    require(0 < len(header.get('description', '')) <= 1024, 'invalid description')
    require(len(text.splitlines()) <= 500, 'skill too long')
    for directory, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP]
        for filename in files:
            if not filename.endswith('.md'):
                continue
            path = Path(directory) / filename
            for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                if re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', link) or link.startswith('#'):
                    continue
                candidate = path.parent / link.split('#')[0]
                require(candidate.exists(), f'broken link {link} from {path.relative_to(root)}')
    cases = json.loads((root / 'evals/cases.json').read_text(encoding='utf-8'))
    require(isinstance(cases, list) and bool(cases), 'empty eval cases')
    ids = set()
    for case in cases:
        require(isinstance(case, dict), 'eval case must be an object')
        for key in ('id', 'prompt'):
            require(isinstance(case.get(key), str) and bool(case[key].strip()), f'invalid case {key}')
        require(case['id'] not in ids, f'duplicate case ID: {case["id"]}')
        ids.add(case['id'])
        critical = case.get('critical')
        require(isinstance(critical, list) and bool(critical) and
                all(isinstance(item, str) and item.strip() for item in critical),
                f'invalid critical criteria: {case["id"]}')
    rubric = json.loads((root / 'evals/rubric.json').read_text(encoding='utf-8'))
    require(isinstance(rubric, dict) and isinstance(rubric.get('dimensions'), list)
            and bool(rubric['dimensions']), 'missing rubric dimensions')
    return len(cases)


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    try:
        count = validate(root)
    except (ValueError, OSError) as exc:
        print(f'FAIL: {exc}')
        return 1
    print(f'STATIC PACKAGE VALIDATION PASSED: {count} scenario definitions; package inputs and links present')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
