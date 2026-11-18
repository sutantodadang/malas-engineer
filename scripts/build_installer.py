"""Build the offline installer from the same directory used by skill managers."""
import argparse
import io
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/malas-engineer"
OUTPUT = ROOT / "install/malas-engineer.pyz"


def build():
    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    refs = set(re.findall(r"\]\((references/[a-z0-9-]+\.md)\)", text))
    allowed = {"SKILL.md", "LICENSE", *refs}
    actual = {p.relative_to(SKILL).as_posix() for p in SKILL.rglob("*") if p.is_file()}
    if not refs or actual != allowed or any(p.is_symlink() for p in SKILL.rglob("*")):
        raise ValueError(f"Unexpected skill contents: {actual ^ allowed}")
    if (SKILL / "LICENSE").read_bytes() != (ROOT / "LICENSE").read_bytes():
        raise ValueError("Skill license differs from repository license")
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        files = {"__main__.py": ROOT / "install/installer.py"}
        files.update({f"malas-engineer/{name}": SKILL / name for name in allowed})
        for name, path in sorted(files.items()):
            entry = zipfile.ZipInfo(name)
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes().replace(b"\r\n", b"\n"))
    return buffer.getvalue()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    data = build()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_bytes() != data:
            raise SystemExit("Stale installer. Run python scripts/build_installer.py")
    else:
        OUTPUT.write_bytes(data)
    print(f"{OUTPUT.name}: {len(data):,} bytes")
