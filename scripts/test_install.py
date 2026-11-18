import codecs
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "install/malas-engineer.pyz"


class InstallTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.home = Path(tmp.name)
        self.codex = self.home / "codex profile"
        self.claude = self.home / "claude profile"
        self.env = dict(os.environ, HOME=tmp.name, USERPROFILE=tmp.name,
                        CODEX_HOME=str(self.codex), CLAUDE_CONFIG_DIR=str(self.claude))

    def invoke(self, *args, ok=True):
        run = subprocess.run([sys.executable, str(APP), *args], cwd=self.home,
                             capture_output=True, text=True, env=self.env)
        self.assertEqual(run.returncode == 0, ok, run.stdout + run.stderr)
        return run.stdout + run.stderr

    def test_cross_agent_install_repeat_and_uninstall(self):
        for agent, config, skills in [
            ("codex", self.codex / "AGENTS.md", self.home / ".agents/skills"),
            ("claude", self.claude / "CLAUDE.md", self.claude / "skills"),
        ]:
            with self.subTest(agent=agent):
                config.parent.mkdir()
                original = codecs.BOM_UTF8 + "My rules\r\nCafé".encode()
                config.write_bytes(original)
                self.invoke(agent)
                target = skills / "malas-engineer"
                names = {p.relative_to(target).as_posix() for p in target.rglob("*") if p.is_file()}
                self.assertEqual(names, {p.relative_to(ROOT / "skills/malas-engineer").as_posix()
                                        for p in (ROOT / "skills/malas-engineer").rglob("*") if p.is_file()})
                self.assertIn(b"coding", config.read_bytes())
                self.assertIn((target / "SKILL.md").as_posix().encode(), config.read_bytes())
                first = config.read_bytes()
                self.invoke(agent)
                self.assertEqual(config.read_bytes(), first)
                self.invoke(agent, "--uninstall")
                self.assertEqual(config.read_bytes(), original)
                self.assertFalse(target.exists())
                self.invoke(agent, "--uninstall")

    def test_override_and_preexisting_custom_install(self):
        self.codex.mkdir()
        override = self.codex / "AGENTS.override.md"
        override.write_bytes(b"Work rules\n")
        old = self.home / ".agents/skills/malas-engineer"
        old.mkdir(parents=True)
        (old / "my-notes").write_text("keep")
        self.invoke("codex", ok=False)
        self.assertFalse((self.codex / "AGENTS.md").exists())
        self.assertEqual(override.read_bytes(), b"Work rules\n")
        (old / "SKILL.md").write_text("---\nname: malas-engineer\n---\nold")
        self.invoke("codex")
        self.assertFalse((old / "my-notes").exists())
        self.assertEqual(len(list((self.home / ".agents").rglob("my-notes"))), 1)
        self.assertIn(b"coding", override.read_bytes())
        (old / "personal.txt").write_text("keep")
        self.invoke("codex", "--uninstall")
        self.assertEqual(override.read_bytes(), b"Work rules\n")
        self.assertEqual(len(list((self.home / ".agents").rglob("personal.txt"))), 1)

    def test_incomplete_marker_leaves_profile_and_skill_untouched(self):
        self.codex.mkdir()
        doc = self.codex / "AGENTS.md"
        original = b"Personal notes\n<!-- malas-engineer:begin -->\n"
        doc.write_bytes(original)
        self.invoke("codex", ok=False)
        self.assertEqual(doc.read_bytes(), original)
        self.assertFalse((self.home / ".agents/skills/malas-engineer").exists())

    def test_failed_override_update_rolls_back_existing_install(self):
        spec = importlib.util.spec_from_file_location("installer", ROOT / "install/installer.py")
        installer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(installer)
        self.codex.mkdir()
        doc = self.codex / "AGENTS.md"
        override = self.codex / "AGENTS.override.md"
        doc.write_text("personal")
        override.write_text("override")
        target = self.home / ".agents/skills/malas-engineer"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("---\nname: malas-engineer\n---\nold")
        original_write = installer.write_atomic

        def fail_override(path, data):
            if path == override:
                raise PermissionError("fixture")
            original_write(path, data)

        with patch.dict(os.environ, self.env), patch.object(sys, "argv", [str(APP)]), \
                patch.object(installer, "write_atomic", fail_override), self.assertRaises(PermissionError):
            installer.install("codex", False)
        self.assertEqual(doc.read_text(), "personal")
        self.assertEqual(override.read_text(), "override")
        self.assertEqual([p.name for p in target.iterdir()], ["SKILL.md"])
        self.assertTrue((target / "SKILL.md").read_text().endswith("old"))
