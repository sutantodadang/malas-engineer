# Malas Engineer

Malas Engineer helps a coding agent decide where a change belongs, which callers it affects, and how to demonstrate that it works. It covers implementation, debugging, refactoring, tests and read-only review. [Apache-2.0 license](LICENSE)

## Quick start

**[Download malas-engineer.pyz](https://raw.githubusercontent.com/sutantodadang/malas-engineer/main/install/malas-engineer.pyz)** and open a terminal in the download directory. With Python 3.11 or newer, run one command for the agent you use.

| Agent | Windows | macOS or Linux |
| --- | --- | --- |
| Codex | `python malas-engineer.pyz codex` | `python3 malas-engineer.pyz codex` |
| Claude Code | `python malas-engineer.pyz claude` | `python3 malas-engineer.pyz claude` |

Start a **new agent session** in any project and ask an ordinary coding question. For example, “Review the callers of this function before we change its return type.” You can also invoke the skill explicitly with `$malas-engineer` in Codex or `/malas-engineer` in Claude Code.

The installer runs offline using the Python standard library. It installs 21 files comprising the skill, its license and 19 on-demand engineering references. Python is needed only to run the installer. Inspect the [installer source](install/installer.py) or [portable skill](skills/malas-engineer).

<details>
<summary>Download and install from the terminal in one command</summary>

Windows PowerShell 7, for Codex:

```powershell
curl.exe -fLO https://raw.githubusercontent.com/sutantodadang/malas-engineer/main/install/malas-engineer.pyz && python malas-engineer.pyz codex
```

macOS or Linux, for Claude Code:

```sh
curl -fLO https://raw.githubusercontent.com/sutantodadang/malas-engineer/main/install/malas-engineer.pyz && python3 malas-engineer.pyz claude
```

Change the final argument to choose the other agent. Both commands save the installer in the current directory.

</details>

## How it stays active

The installer adds a short, marked instruction to the selected agent’s personal startup file. It tells the agent which local skill file to read for coding tasks and includes the core review and verification rules. Each agent loads this through its built-in startup mechanism. No hook or background service is required.

| Agent | Skill directory | Personal startup instructions |
| --- | --- | --- |
| Codex | `~/.agents/skills/malas-engineer/` | `$CODEX_HOME/AGENTS.md` (default `~/.codex/AGENTS.md`) and an existing active `AGENTS.override.md` |
| Claude Code | `$CLAUDE_CONFIG_DIR/skills/malas-engineer/` | `$CLAUDE_CONFIG_DIR/CLAUDE.md` (default `~/.claude/CLAUDE.md`) |

Startup instructions make the rule available in each normal session. The model decides how to act, subject to the host’s instruction precedence and context limits. Use your project’s tests and CI for checks that must block a merge. [Codex instructions](https://developers.openai.com/codex/guides/agents-md/) · [Claude Code memory](https://code.claude.com/docs/en/memory)

## Update or remove

Download the current installer and run the same command to update. Running it twice leaves a single instruction block. A recognized older installation, including the old full-repository ZIP, or one with personal edits is moved to a backup outside the skill discovery directory. The installer prints the backup path. Existing instructions outside the marked block are preserved. If you manually added activation text for an older version, review that text separately.

To uninstall, append `--uninstall` to the same command, for example `python malas-engineer.pyz codex --uninstall`. Restart the agent. A modified skill directory is backed up during removal.

For a **project-only or manual installation**, copy just [skills/malas-engineer](skills/malas-engineer) into the agent’s skills directory. For Codex in a project use `.agents/skills/`. For Claude Code use `.claude/skills/`. This option uses normal skill discovery. Teams can add a project rule in their own instruction file.

## Evidence and contributions

The [agent trial report](evals/reports/v5-trials.md) includes the prompts, independent checks and replayable outputs for 16 earlier runs. It records both an improvement on a Python CLI task and a tie on a JavaScript concurrency task. The [runnable examples](examples/README.md), [evaluation protocol](evals/README.md) and [research notes](references/research-synthesis.md) are maintainer resources.

CI checks the skill metadata, rebuilds the downloadable installer, tests installation in temporary homes, and runs the example and tooling suites. See [contributing](CONTRIBUTING.md) and [security reporting](SECURITY.md).
