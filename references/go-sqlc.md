# Go, sqlc and repository ownership

Default new backend: `cmd/api/main.go` or `internal/container/wire.go` (composition), `internal/app/<feature>/handler.go`, `service.go`, optional `contract.go` (consumer owned), `internal/repositories/...` (SQL adapters), `db/queries` and generated sqlc files.

## Direct sqlc contract is valid
If a service needs a subset of generated queries, define a narrow service-owned interface with exactly the methods it calls. Generated `*Queries` can satisfy it. This is dependency injection even without an additional repository implementation. A wrapper earns existence only if it adds transaction coordination, data conversion/validation, tenant safety, caching or a real storage boundary.

```go
// within internal/app/report/service.go
// Actual generated signatures and types must be verified in the real repo.
type ReportReader interface {
    ListReports(ctx context.Context, userID uuid.UUID) ([]Report, error)
}
type Service struct { reader ReportReader }
func NewService(reader ReportReader) *Service { return &Service{reader: reader} }
func (s *Service) Reports(ctx context.Context, userID uuid.UUID) ([]Report, error) {
    return s.reader.ListReports(ctx, userID)
}
```

This is a **didactic contract**; do not assume `ListReports` or `Report` exists in an actual sqlc output. Match actual generated signatures when implementing.

## Explicit production assembly
```go
// cmd/api/main.go (illustrative; adapt to real constructors)
queries := db.New(pool)
reportService := report.NewService(queries)
reportHandler := report.NewHandler(reportService)
router.Register(reportHandler)
```

## Required checks
- No `uuid.MustParse()` on untrusted input; parse with an error.
- Pass context through and handle cancel/timeouts.
- SQLC output is generated; edit source `.sql`, run sqlc and review generated changes.
- For finance, avoid float for exact money computation; decimal, integer minor units or appropriate db numeric types.
- Keep pgx/sqlc type leakage consciously bounded; map to domain types when complexity justifies it.
- Constructors return concrete implementation by default; introduce interface at consumer seam.
- Test fake reader and production assembly separately.
