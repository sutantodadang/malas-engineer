#!/usr/bin/env python3
"""Conservative diagnostic architecture scan. Not a proof of correctness.

The scan catches some clear mistakes, not all DI/layering failures. It avoids
checking generated code, vendored dependencies, and tests. False positives are
possible; interpret findings manually and use runtime tests for proof.
"""
import argparse
import ast
import json
import os
import re
from pathlib import Path

SKIP = {'node_modules', 'vendor', 'dist', 'build', '.git', '__pycache__', '.venv', 'venv', 'generated', 'migrations', 'test', 'tests'}
SERVICE_MARKERS = {'service', 'services', 'usecase', 'usecases'}
HANDLER_MARKERS = {'handler', 'handlers', 'controller', 'controllers', 'views', 'routes', 'router'}
ASSEMBLY_MARKERS = {'container', 'bootstrap', 'main', 'composition', 'wire', 'app'}

def role(path: Path):
    parts = {p.lower() for p in path.parts}
    stem = path.stem.lower()
    if any(p in ASSEMBLY_MARKERS for p in parts) and stem in ASSEMBLY_MARKERS:
        return 'assembly'
    if any(p in SERVICE_MARKERS for p in parts) or stem.endswith(('_service', 'service', '_usecase', 'usecase')):
        return 'service'
    if any(p in HANDLER_MARKERS for p in parts) or stem.endswith(('_handler', 'handler', '_controller', 'controller', '_view', 'view')):
        return 'handler'
    return 'other'

def named_call(call: ast.Call):
    f = call.func
    if isinstance(f, ast.Name): return f.id
    if isinstance(f, ast.Attribute): return f.attr
    return ''

def python_scan(path: Path, kind=None):
    findings = []
    try:
        tree = ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
    except SyntaxError as exc:
        return [{'file': str(path), 'line': exc.lineno or 1, 'rule': 'PARSE_ERROR', 'detail': str(exc)}]
    kind = kind or role(path)
    if kind == 'service':
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = named_call(node)
                if re.search(r'(Repository|Client|SessionLocal|PrismaClient|create_engine)$', name) and name[:1].isupper() or name in {'create_engine', 'connect', 'get_db'}:
                    findings.append({'file': str(path), 'line': node.lineno, 'rule': 'SERVICE_CREATES_ADAPTER', 'detail': f'Service creates collaborator: {name}'})
        for klass in [n for n in ast.walk(tree) if isinstance(n, ast.ClassDef) and n.name.endswith(('Service','UseCase'))]:
            constructors = [n for n in klass.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == '__init__']
            if not constructors: continue
            init = constructors[0]
            injected = set()
            for n in ast.walk(init):
                if isinstance(n, (ast.Assign, ast.AnnAssign)):
                    targets = n.targets if isinstance(n, ast.Assign) else [n.target]
                    for target in targets:
                        if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name) and target.value.id == 'self' and isinstance(n.value, ast.Name):
                            if n.value.id in {a.arg for a in init.args.args if a.arg != 'self'}:
                                injected.add(target.attr)
            used = {n.attr for method in klass.body if isinstance(method, (ast.FunctionDef, ast.AsyncFunctionDef)) and method.name != '__init__' for n in ast.walk(method) if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == 'self'}
            for attr in injected-used:
                findings.append({'file': str(path), 'line': init.lineno, 'rule': 'INJECTED_BUT_UNUSED', 'detail': f'{klass.name}.{attr} is assigned from constructor but never read in methods'})
    if kind == 'handler':
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                f = node.func
                if isinstance(f, ast.Attribute) and (f.attr in {'execute','executemany','raw','cursor'} or f.attr in {'filter','get','create'} and isinstance(f.value, ast.Attribute) and f.value.attr == 'objects'):
                    findings.append({'file': str(path), 'line': node.lineno, 'rule': 'HANDLER_PERSISTENCE_IO', 'detail': 'Potential direct DB/ORM operation in handler'})
    return findings

def strip_comments(text: str, lang: str):
    # Best-effort comment removal, not a parser; only highlights likely issues.
    text = re.sub(r'/\*[\s\S]*?\*/', lambda m: '\n' * m.group().count('\n'), text)
    text = re.sub(r'(?m)^[ \t]*//[^\n]*$', '', text)
    return text

def other_scan(path: Path, kind=None):
    kind = kind or role(path)
    if kind not in {'service','handler'}: return []
    text = strip_comments(path.read_text(encoding='utf-8'), path.suffix)
    rules = []
    if kind == 'service':
        if path.suffix == '.go': rules = [('SERVICE_CREATES_ADAPTER', r'\bNew\w*(?:Repo|Repository|Client|Pool|DB)\s*\('), ('SERVICE_CREATES_ADAPTER', r'\b(?:sql|pgx)\.Open\s*\(')]
        else: rules = [('SERVICE_CREATES_ADAPTER', r'\bnew\s+\w*(?:Repository|PrismaClient|HttpClient)\s*\('), ('SERVICE_CREATES_ADAPTER', r'\b(?:getRepository|createConnection)\s*\(')]
    if kind == 'handler':
        if path.suffix == '.go': rules = [('HANDLER_PERSISTENCE_IO', r'\b(?:db|pool|conn)\.(?:Query|Exec|QueryRow)\s*\(')]
        else: rules = [('HANDLER_PERSISTENCE_IO', r'\b(?:prisma\.[a-zA-Z]+\.(?:find|create|update|delete)|db\.query|repository\.query)')]
    issues=[]
    for code, regex in rules:
        for match in re.finditer(regex, text):
            issues.append({'file': str(path), 'line': text.count('\n', 0, match.start())+1, 'rule': code, 'detail': 'Potential layer boundary violation (heuristic)'})
    return issues

def scan(root: Path):
    if not root.is_dir():
        raise ValueError(f'Scan root is not a directory: {root}')
    result = []
    root_name = Path(root.resolve().name)
    for directory, dirs, files in os.walk(root):
        dirs[:] = [name for name in dirs if name not in SKIP and not name.startswith('.')]
        for name in files:
            if name.startswith(('.', 'test_')) or name.endswith(('_test.go', '.test.ts', '.test.tsx', '.spec.ts', '.spec.tsx', '_test.py')):
                continue
            path = Path(directory) / name
            if path.suffix in {'.py', '.go', '.ts', '.tsx'} and path.is_file():
                kind = role(root_name / path.relative_to(root))
                scanner = python_scan if path.suffix == '.py' else other_scan
                result.extend(scanner(path, kind))
    return sorted(result, key=lambda x: (x['file'], x['line'], x['rule']))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('root', type=Path)
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--fail-on-findings', action='store_true', help='Opt-in fail gate; review false positives before using in CI')
    args = ap.parse_args()
    try:
        issues=scan(args.root)
    except (ValueError, OSError, UnicodeError) as exc:
        ap.error(str(exc))
    if args.json: print(json.dumps({'count':len(issues),'findings':issues},indent=2))
    else:
        for x in issues: print(f"{x['file']}:{x['line']} {x['rule']} {x['detail']}")
        print(f'{len(issues)} potential architecture findings (heuristic, manual review needed)')
    raise SystemExit(1 if issues and args.fail_on_findings else 0)
