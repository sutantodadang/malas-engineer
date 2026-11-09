# Changelog

All notable changes to this skill are documented here. The format follows Keep a Changelog, and the project uses Semantic Versioning.

## [4.0.0] - 2026-11-01

### Added

- Lean `SKILL.md` router with progressive disclosure, under 250 lines.
- Architecture selection ladder: script, small API, explicit layers, domain model, vertical slices, ports and adapters.
- Layer contract table with allowed and forbidden imports.
- Testing guide: test selection matrix, contract testing, property-based testing, mutation testing, Testcontainers, flaky-test policy.
- Security checklist mapped to OWASP secure code review and ASVS themes.
- Reliability guide: SLIs as ratios, SLOs, error budgets, latency budgets, load testing.
- AI-generated code protocol with the eight observed bug categories and a verification checklist.
- Migration guide for incremental adoption.
- MADR architecture decision record template.
- Agent context guide covering AGENTS.md jurisdiction, accumulation, precedence, and progressive disclosure.
- `scripts/validate_skill.py` and `scripts/review_diff.sh`.
- Apache-2.0 license, README, CONTRIBUTING, SECURITY.

### Changed

- Architecture guidance is now a default with explicit exceptions, not a universal mandate.
- Review protocol adds severity labels and two independent passes.
- Reporting now uses an evidence ledger: observed, inferred, unknown.
- Definition of done is explicit.
- Go and sqlc guidance distinguishes a consumer-owned interface from a redundant repository wrapper.

### Removed

- Duplicated instruction bodies across `SKILL.md`, `AGENTS.md`, and `CLAUDE.md`.
- Unqualified claims that clean architecture is always correct.

## [3.1.0] - 2026-10-20

### Added

- Explicit layered architecture as the default for nontrivial backends.
- Go and sqlc persistence guidance.
- Anti-hallucination and evidence discipline.
- ASD-STE100-inspired technical English.

## [1.0.0] - 2026-09-01

Initial internal version.
