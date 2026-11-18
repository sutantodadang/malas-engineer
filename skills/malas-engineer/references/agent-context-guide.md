# Agent context guide

Read this when writing `AGENTS.md`, `CLAUDE.md`, a `SKILL.md`, or any instruction file for a coding agent.

## Three formats, three jobs

| Format | Job | Loaded |
|---|---|---|
| `AGENTS.md` | Behavior: rules, constraints, commands, boundaries | Every session, layered by directory |
| `SKILL.md` | Capability: a repeatable procedure the agent can invoke | On demand, when the task matches |
| `CLAUDE.md` | Claude-specific adapter | Every Claude Code session |

`AGENTS.md` answers "how do we work here". `SKILL.md` answers "how do I do this task". Do not duplicate one in the other.

## AGENTS.md semantics

The v1.1 proposal codifies four rules:

1. **Jurisdiction.** A file applies to its directory and everything below it. A file at `frontend/AGENTS.md` does not govern `backend/`.
2. **Accumulation.** Guidance accumulates down the tree. A nested file extends its ancestors; it does not replace them.
3. **Precedence.** When guidance conflicts, the file closest to the edited file wins. User instructions override repository guidance.
4. **Inheritance.** A child file need not restate ancestor rules. A leaf file can be small.

Implementation differences matter:

- Codex concatenates from root to leaf, with a default 32 KiB combined limit, and checks `AGENTS.override.md` first in a directory.
- Claude Code reads `CLAUDE.md` natively and walks up from the working directory. A one-line `CLAUDE.md` containing `@AGENTS.md` avoids duplication.
- Some tools read only the nearest file. Write each file so it makes sense on its own, but do not repeat the whole root file.

## What belongs in AGENTS.md

Include:

- One or two lines of project context.
- Exact setup, build, lint, typecheck, and test commands, including the fast file-scoped command.
- The directory map and the rule for where new code goes.
- Non-default conventions the agent cannot infer.
- Hard constraints: files not to touch, actions requiring approval.
- Testing requirements and the definition of done.
- Known traps that repeatedly cause mistakes.
- Pointers to deeper docs with a "read when" trigger.

Exclude:

- Anything the agent can derive by reading the code.
- Tutorials and long explanations. Link instead.
- Information that changes weekly.
- File-by-file descriptions.
- Personas and motivational prose.

## Size and shape

- Aim under 200 lines for a root `AGENTS.md`. Hard ceiling: 500.
- Keep `SKILL.md` under 500 lines. Move detail into `references/`.
- Keep every reference one level deep from `SKILL.md`. Nested reference chains get partially read.
- Prefer pointers to copies. A copied snippet rots.

## Progressive disclosure

At session start, load metadata only. Load the body when the task matches. Load references only when the trigger applies.

A good `SKILL.md` starts with a table:

| Read when | Reference |
|---|---|
| Reviewing a diff | `references/review-checklist.md` |
| Changing an auth path | `references/security-checklist.md` |

This is a router, not a table of contents. Each row names a concrete trigger.

## Writing the description

The `description` field decides whether the skill is selected. Write it in third person, with capability and trigger.

Good:

```yaml
description: "Reviews code changes for correctness, security, tenancy, and test quality. Use when reviewing a pull request, a diff, or an agent-generated change."
```

Poor:

```yaml
description: "A helpful skill for code review."
```

Rules from the Agent Skills specification:

- `name`: 1 to 64 characters, lowercase letters, digits, and hyphens, no leading or trailing hyphen, no consecutive hyphens. Must match the directory name.
- `description`: 1 to 1024 characters, non-empty.
- `license`: optional, short name or bundled file.
- `metadata`: optional string map.
- `allowed-tools`: optional, experimental.

## Compaction priorities

When an agent compacts context, preserve:

1. Explicit constraints and prohibitions: must, must not, always, never.
2. Behavioral requirements: tests, workflows, review steps.
3. Scope-specific overrides.
4. Required commands and ordering.
5. Architectural invariants.

Safe to compress or drop:

- Motivational prose.
- Redundant inherited guidance.
- Long examples.
- Minor style preferences.

When space is tight, prefer fewer, stronger instructions.

## Monorepos

```text
/AGENTS.md                  # repo-wide: commands, boundaries, conventions
/services/payments/AGENTS.md  # payment rules, test command, secrets policy
/services/web/AGENTS.md       # frontend conventions
```

Rules:

- Root file holds universal rules.
- Nested files hold only what differs.
- Do not repeat the root in every leaf.
- Test that a nested file is actually loaded by the target agent.

## Anti-patterns

- A 1000-line root file that nobody reads to the end.
- Copying the same rules into `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and `.cursorrules`.
- A skill that preloads every reference.
- A description that says "helps with code".
- Instructions that contradict the repository's actual commands.
- Stale commands. Review and prune quarterly.
- Secrets or internal URLs in instruction files.

## Checklist for a new instruction file

- [ ] It states behavior, not capability, if it is `AGENTS.md`.
- [ ] It names exact commands.
- [ ] It names hard constraints.
- [ ] It links deeper docs with a "read when" trigger.
- [ ] It is under the size limit.
- [ ] It does not duplicate another file.
- [ ] It was tested with the actual agent.

## References

- AGENTS.md: https://agents.md/
- AGENTS.md v1.1 proposal: https://github.com/agentsmd/agents.md/issues/135
- Agent Skills specification: https://agentskills.io/specification
- Anthropic skill authoring best practices: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- OpenAI Codex AGENTS.md discovery: https://learn.chatgpt.com/docs/agent-configuration/agents-md
