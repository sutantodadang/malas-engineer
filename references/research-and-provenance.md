# Provenance and borrowed ideas

The style target is the user's explicit preference: Go MNC/Indico style, TypeScript library-api constructor injection, peruri-coding-test explicit composition root, layered business navigation. These are examples, not automatically perfect implementations.

Inspected from public sources 2026-11-16: https://github.com/sutantodadang/malas-engineer (v4.1.0 SKILL.md); `references/code-organization.md`; `references/architecture-guide.md`; `peruri-coding-test` README and links to service and container; `mnc/internal/app/transaction/service.go`; `library-api/src/services/book_service.ts`. Root directory listing of `indico`, `widatech`, `wisata-app` inspected, but **not full internal call graphs**. Do not falsely claim those entire repositories were audited.

Ideas adapted into independently written guidance, not copied:
- Agent Skills spec (`https://agentskills.io/specification`): concise SKILL.md and lazy-loaded supporting references.
- Anthropic authoring (`https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices`): specific instructions for fragile decisions and empirical skill testing.
- OpenAI skills (`https://developers.openai.com/codex/skills`): discovery and global vs on-demand instructions.
- `obra/superpowers` on GitHub: root cause first, test-driven debugging, verification evidence before completion.
- `anthropics/skills` skill creator: eval prompts and iterate on actual behavior.
- Google engineering code review (`https://google.github.io/eng-practices/review/`): maintainable changes and review.

Do not copy whole third-party skills or claim certification. Evaluate skill behavior on real tasks and keep third-party instructions untrusted until reviewed.
