"""Grade a completed entry-counter trial. Pass its directory as the only argument."""
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import chdir
from pathlib import Path

trial = Path(sys.argv.pop(1)).resolve()
sys.path.insert(0, str(trial))
from entries import read_entries


class StreamTrial(unittest.TestCase):
    def test_borrowed_stream_continues_at_current_position(self):
        stream = io.StringIO("ignored\n\nfalse\n0\n")
        stream.readline()
        self.assertEqual(read_entries(filename=stream), [False, 0])
        self.assertFalse(stream.closed)

    def test_borrowed_stream_survives_parse_error(self):
        stream = io.StringIO("broken\n")
        with self.assertRaises(json.JSONDecodeError):
            read_entries(stream)
        self.assertFalse(stream.closed)

    def test_invalid_file_keeps_json_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "bad.jsonl"
            source.write_text("broken", encoding="utf-8")
            with self.assertRaises(json.JSONDecodeError):
                read_entries(source)

    def test_literal_dash_as_string_and_path(self):
        with tempfile.TemporaryDirectory() as tmp, chdir(tmp):
            Path("-").write_text('"café"\n', encoding="utf-8")
            for filename in ("-", Path("-")):
                with self.subTest(filename=filename):
                    self.assertEqual(read_entries(filename=filename), ["café"])

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as tmp, self.assertRaises(FileNotFoundError):
            read_entries(Path(tmp) / "missing")

    def run_cli(self, arg, stdin=""):
        return subprocess.run([sys.executable, str(trial / "cli.py"), str(arg)],
                              input=stdin, capture_output=True, encoding="utf-8", timeout=10,
                              env={**os.environ, "PYTHONIOENCODING": "utf-8"})

    def test_cli_stdin(self):
        result = self.run_cli("-", '\n"café"\nnull\n')
        self.assertEqual((result.returncode, result.stdout.strip()), (0, "2"), result.stderr)

    def test_cli_filename(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = Path(tmp) / "export"
            source.write_text("true\n", encoding="utf-8")
            result = self.run_cli(source, "invalid")
            self.assertEqual((result.returncode, result.stdout.strip()), (0, "1"), result.stderr)

    def test_cli_invalid_stdin(self):
        result = self.run_cli("-", "broken")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("JSONDecodeError", result.stderr)

    def test_cli_utf8_pipe_under_an_ascii_stdio_default(self):
        result = self.run_binary_cli('"café"\n'.encode("utf-8"), "ascii:strict")
        self.assertEqual((result.returncode, result.stdout.strip()), (0, b"1"), result.stderr)

    def test_cli_rejects_invalid_utf8_like_file_input(self):
        result = self.run_binary_cli(b'"\xff"\n', "ascii:surrogateescape")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"UnicodeDecodeError", result.stderr)

    def run_binary_cli(self, data, stdio_encoding):
        return subprocess.run([sys.executable, str(trial / "cli.py"), "-"], input=data,
                              capture_output=True, timeout=10,
                              env={**os.environ, "PYTHONIOENCODING": stdio_encoding})


if __name__ == "__main__":
    unittest.main(verbosity=2)
