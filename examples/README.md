# Executable reference contracts

These are **three illustrative miniature examples**, not the only languages supported. They are not copies of user code and do not claim SQLC is actually generated here. For every other language follow [universal application](../references/universal-application.md) and the current project conventions. They express dependency boundaries in plain Go, Python, and TypeScript, with actual wiring and fake-adapter tests.

- Go: `cd examples/go-contract && go test ./...` (stdlib-only, Go 1.22+)
- Python: `cd examples/python-contract && python -m unittest discover -s tests -v` (stdlib-only)
- TypeScript: `node --experimental-strip-types --test examples/typescript-contract/service.test.ts` (Node 22+ experimental type stripping; not a `tsc` check)

For the pinned compiler, run `npm ci --prefix examples/typescript-contract --ignore-scripts --no-audit --no-fund`, then `node examples/typescript-contract/node_modules/typescript/bin/tsc -p examples/typescript-contract/tsconfig.json`. This type-checks the application sources; the Node tests are executed separately, not included in that typecheck.

Each example proves that a fake injected dependency is invoked and demonstrates production wiring from a composition root. They are not production-ready implementations.
