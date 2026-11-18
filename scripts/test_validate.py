"""Exercise the package validator as users and CI invoke it."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PackageValidationTests(unittest.TestCase):
    def test_optimized_python_does_not_disable_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / 'malas-engineer'
            # Copy only package inputs, never installed dependencies or output evidence.
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns(
                '.git', 'node_modules', '__pycache__', 'reports'))
            (target / 'install/global-AGENTS.md').unlink()
            result = subprocess.run(
                [sys.executable, '-O', str(ROOT / 'scripts/validate.py'), str(target)],
                capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0, result.stdout)
            self.assertIn('missing install/global-AGENTS.md', result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
