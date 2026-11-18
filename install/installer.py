"""Install Malas Engineer from a self-contained Python zipapp."""
import argparse
import codecs
import os
import re
import shutil
import stat
import sys
import tempfile
import zipfile
from contextlib import ExitStack
from pathlib import Path

NAME = "malas-engineer"
BEGIN = b"<!-- malas-engineer:begin -->"
END = b"<!-- malas-engineer:end -->"
RULE = """For coding and code-review tasks, read and apply Malas Engineer at `{entry}`.
Inspect the affected callers, preserve their contracts, and verify the changed behavior.
Keep review-only tasks read-only. Report the checks that actually ran."""


def plain_path(path):
    # Moving a link or writing through one can change a shared dotfiles checkout.
    if path.is_symlink() or (path.exists() and
            getattr(path.lstat(), "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT):
        raise ValueError(f"Linked path needs manual installation: {path}")


def instructions(original, rule, remove):
    bom = codecs.BOM_UTF8 if original.startswith(codecs.BOM_UTF8) else b""
    body = original[len(bom):]
    body.decode("utf-8")
    if b"\0" in body:
        raise ValueError("Instruction file must be UTF-8 text")
    newline = b"\r\n" if b"\r\n" in body else b"\n"
    match = re.search(rb"(?ms)^" + BEGIN + rb"\r?\n.*?^" + END + rb"(?=\r?$)(?:\r?\n){0,2}", body)
    if body.count(BEGIN) != bool(match) or body.count(END) != bool(match):
        raise ValueError("Ambiguous malas-engineer markers; check the instruction file")
    block = b"" if remove else newline.join([BEGIN, *rule.splitlines(), END, b"", b""])
    if match:
        return bom + body[:match.start()] + block + body[match.end():]
    return bom + block + body


def write_atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as tmp:
        staged = Path(tmp.name)
    try:
        staged.write_bytes(data)
        if path.exists():
            shutil.copymode(path, staged)
        os.replace(staged, path)
    finally:
        staged.unlink(missing_ok=True)


def payload():
    with zipfile.ZipFile(sys.argv[0]) as archive:
        return {n.split("/", 1)[1]: archive.read(n) for n in archive.namelist()
                if re.fullmatch(r"malas-engineer/(?:SKILL\.md|LICENSE|references/[a-z0-9-]+\.md)", n)}


def matches(target, files):
    if not target.is_dir():
        return False
    if {p.name for p in target.iterdir()} != {"SKILL.md", "LICENSE", "references"}:
        return False
    refs = target / "references"
    plain_path(refs)
    if not refs.is_dir() or {p.name for p in refs.iterdir()} != {
            name.split("/")[1] for name in files if name.startswith("references/")}:
        return False
    for name, data in files.items():
        path = target / name
        plain_path(path)
        if not path.is_file() or path.read_bytes() != data:
            return False
    return True


def install(agent, remove):
    home = Path.home()
    if agent == "codex":
        config = Path(os.environ.get("CODEX_HOME") or home / ".codex").expanduser()
        target = home / ".agents/skills" / NAME
        docs = [config / "AGENTS.md"]
        override = config / "AGENTS.override.md"
        plain_path(override)
        if override.is_file() and override.read_bytes().strip():
            docs.append(override)
    else:
        config = Path(os.environ.get("CLAUDE_CONFIG_DIR") or home / ".claude").expanduser()
        target = config / "skills" / NAME
        docs = [config / "CLAUDE.md"]
    if not config.is_absolute():
        raise ValueError("Custom configuration directory must be absolute")
    if remove and not target.exists() and not any(p.exists() for p in docs):
        return
    files = payload()
    if not {"SKILL.md", "LICENSE"}.issubset(files):
        raise ValueError("Incomplete installer")
    base = target.parent.parent
    base.mkdir(parents=True, exist_ok=True)
    lock = base / ".malas-engineer-install.lock"
    with ExitStack() as cleanup:
        lock.mkdir()
        cleanup.callback(lock.rmdir)
        edits = []
        for path in docs:
            plain_path(path)
            original = path.read_bytes() if path.exists() else None
            rule = RULE.format(entry=(target / "SKILL.md").as_posix()).encode("utf-8")
            updated = instructions(original or b"", rule, remove)
            if updated != (original or b""):
                edits.append((path, original, updated))
        plain_path(target)
        same = matches(target, files)
        replace = target.exists() and (remove or not same)
        if replace and not same:
            entry = target / "SKILL.md"
            plain_path(entry)
            if not entry.is_file() or not re.match(
                    rb"^---\r?\nname: malas-engineer\r?\n", entry.read_bytes()):
                raise ValueError(f"Unrecognized directory. Move it aside and retry: {target}")
        scratch = Path(cleanup.enter_context(tempfile.TemporaryDirectory(dir=base)))
        prepared = scratch / NAME
        if not remove and not same:
            for name, data in files.items():
                path = prepared / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(data)
        with ExitStack() as rollback:
            if replace:
                # An older package or a local edit may contain the user's only copy.
                backup = Path(tempfile.mkdtemp(prefix=".malas-engineer-backup-", dir=base))
                previous = backup / NAME
                rollback.callback(backup.rmdir)
                target.rename(previous)
                rollback.callback(previous.rename, target)
            if prepared.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                prepared.rename(target)
                rollback.callback(target.rename, prepared)
            for path, original, updated in edits:
                if (path.read_bytes() if path.exists() else None) != original:
                    raise ValueError(f"Instruction file changed during installation: {path}")
                write_atomic(path, updated)
                if original is None:
                    rollback.callback(path.unlink)
                else:
                    rollback.callback(write_atomic, path, original)
            rollback.pop_all()
        if replace:
            if same and matches(previous, files):
                # Only files already verified against the archive are discarded.
                shutil.rmtree(previous)
                backup.rmdir()
            else:
                print(f"Previous files preserved at {previous}")
    print(f"{'Removed' if remove else 'Installed'} {target}. Start a new {agent} session.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("agent", choices=("codex", "claude"))
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args()
    try:
        install(args.agent, args.uninstall)
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        parser.exit(1, f"Installation error: {error}\n")
