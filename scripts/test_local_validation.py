"""Exercise runner reporting without invoking compilers or changing repo reports."""
import contextlib
import io
import json
import runpy
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class LocalValidationTests(unittest.TestCase):
    def run_with_first_result(self, first):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / 'scripts/run_local_validation.py'
            script.parent.mkdir()
            shutil.copy2(Path(__file__).with_name('run_local_validation.py'), script)
            success = subprocess.CompletedProcess([], 0, 'ok', '')
            with patch('subprocess.run', side_effect=[first] + [success] * 6):
                with contextlib.redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as exit:
                    runpy.run_path(str(script), run_name='__main__')
            report = json.loads((Path(tmp) / '.artifacts/local-validation.json').read_text())
            return exit.exception.code, report

    def test_timeout_is_a_failure_not_an_unrun_check(self):
        code, report = self.run_with_first_result(subprocess.TimeoutExpired('compiler', 45))
        self.assertEqual(code, 1)
        self.assertEqual(report['failed'], 1)
        self.assertEqual(report['not_run'], 0)

    def test_missing_executable_is_reported_not_run(self):
        code, report = self.run_with_first_result(FileNotFoundError('compiler missing'))
        self.assertEqual(code, 1)
        self.assertEqual(report['not_run'], 1)
        self.assertEqual(report['failed'], 0)


if __name__ == '__main__':
    unittest.main()
