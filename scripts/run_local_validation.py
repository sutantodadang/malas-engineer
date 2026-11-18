#!/usr/bin/env python3
"""Execute local code, type-check, diagnostic tests, and package checks.

IMPORTANT: this is NOT a Claude/Codex behavior benchmark.
"""
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
STEPS=[
 ('package', [sys.executable, 'scripts/validate.py', '.'], ROOT),
 ('go_unit_and_handler', ['go','test','-count=1','./...'], ROOT/'examples/go-contract'),
 ('python_service_and_wiring', [sys.executable,'-m','unittest','discover','-s','tests','-v'], ROOT/'examples/python-contract'),
 ('typescript_typecheck', ['node','node_modules/typescript/bin/tsc','-p','tsconfig.json'], ROOT/'examples/typescript-contract'),
 ('typescript_service_and_wiring', ['node','--experimental-strip-types','--test','service.test.ts'], ROOT/'examples/typescript-contract'),
 ('tooling_regressions', [sys.executable,'-m','unittest','discover','-s','scripts','-p','test_*.py','-v'], ROOT),
 ('architecture_scan_examples', [sys.executable, 'scripts/architecture_audit.py', 'examples', '--json'], ROOT),
]
results=[]
for name,cmd,cwd in STEPS:
    command = ' '.join('python' if part == sys.executable else part for part in cmd)
    try:
        cp=subprocess.run(cmd,cwd=cwd,capture_output=True, encoding='utf-8', errors='replace', timeout=180)
        status='PASS' if cp.returncode==0 else 'FAIL'
        row={'name':name,'status':status,'command':command,'working_directory':str(cwd.relative_to(ROOT)) if cwd!=ROOT else '.', 'exit_code':cp.returncode, 'stdout':cp.stdout[-5000:],'stderr':cp.stderr[-5000:]}
    except FileNotFoundError as err:
        row={'name':name,'status':'NOT RUN','command':command,'reason':str(err)}
    except subprocess.TimeoutExpired as err:
        row={'name':name,'status':'FAIL','command':command,'reason':str(err)}
    print(f"{row['status']:7} {name}")
    results.append(row)
summary={'check_type':'Local reproducible contract tests, not coding-agent behavioral evaluation',
         'timestamp_utc':datetime.now(timezone.utc).isoformat(),
         'python':sys.version.split()[0],
         'environment_note':'Examples use stand-in adapters; no SQLC generation, external DB or full user project build',
         'model_behavior_eval':'NOT RUN by this script: agent trials are recorded separately; runtime availability is not probed',
         'checks':results,
         'passed':sum(r['status']=='PASS' for r in results),
         'failed':sum(r['status']=='FAIL' for r in results),
         'not_run':sum(r['status']=='NOT RUN' for r in results)}
output=ROOT/'evals/reports/local-validation.json'
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8')
print(f'Results recorded to {output.relative_to(ROOT)}')
raise SystemExit(0 if summary['passed']==len(STEPS) else 1)
