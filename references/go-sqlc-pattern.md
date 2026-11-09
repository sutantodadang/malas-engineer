# Go with sqlc: layers without redundant wrappers

Read this when the stack is Go with sqlc, sqlx, or GORM.

## Default call path

```text
handler -> service -> narrow consumer-owned query interface -> sqlc generated Queries -> database
```

For a new nontrivial Go service using sqlc, this is the default. The generated query layer is already the persistence implementation. A wrapper whose only job is `return q.GetUser(ctx, id)` adds navigation cost without architectural value.

## Consumer-owned interface

Define the interface where it is consumed, with only the methods that consumer needs.

```go
package booking

import (
    "context"

    "example.com/project/internal/db/sqlc"
)

type bookingReader interface {
    GetBooking(ctx context.Context, id string) (sqlc.Booking, error)
    ListBookingsByTenant(ctx context.Context, arg sqlc.ListBookingsByTenantParams) ([]sqlc.Booking, error)
}

type Service struct {
    queries bookingReader
}

func NewService(q bookingReader) *Service {
    return &Service{queries: q}
}
```

`*sqlc.Queries` satisfies the interface implicitly. Inspect the generated code before naming methods. Do not assume a method exists.

## When a handwritten repository earns its place

Add one only when it does real work:

1. Maps persistence structs to independently modeled domain types.
2. Coordinates several generated queries into one persistence operation.
3. Applies tenant scoping or a consistency policy in one place.
4. Hides storage behind multiple consumers or a swappable adapter.
5. Owns transaction composition across several queries.

Do not add one when it only forwards one method with the same arguments and results.

## Transactions

Transaction ownership belongs to the service or use case that defines the business operation.

```go
func (s *Service) Transfer(ctx context.Context, from, to string, amount int64) error {
    return s.tx.WithTx(ctx, func(q *sqlc.Queries) error {
        if err := q.Debit(ctx, sqlc.DebitParams{ID: from, Amount: amount}); err != nil {
            return fmt.Errorf("debit %s: %w", from, err)
        }
        if err := q.Credit(ctx, sqlc.CreditParams{ID: to, Amount: amount}); err != nil {
            return fmt.Errorf("credit %s: %w", to, err)
        }
        return nil
    })
}
```

Rules:

- Never mix `DB` and `Tx` handles accidentally.
- Do not start a transaction inside a repository method that the caller cannot see.
- Keep network calls and slow work outside the transaction.
- Roll back on every error path.

## Context, errors, identifiers

- Accept `context.Context` as the first parameter on request-scoped operations.
- Propagate cancellation. Do not spawn a goroutine that outlives the request without a reason.
- Wrap errors with context: `fmt.Errorf("load booking %s: %w", id, err)`.
- Return domain errors that callers can classify with `errors.Is` or `errors.As`.
- Validate untrusted UUIDs with a function that returns an error. Do not use `uuid.MustParse` on user input.
- Do not leak SQL text or driver internals to clients.

## Money

- Use integer minor units or an exact decimal type.
- Do not convert to `float64` for domain arithmetic unless the precision trade-off is documented and tested.
- Keep rounding rules in one place.
- Preserve existing API and database representations when fixing a bug.

## sqlc-specific pitfalls

- Generated files are not hand-edited. Change the `.sql` file and regenerate.
- Verify nullable columns map to the expected Go type. `sql.NullString` versus `*string` changes call sites.
- Dynamic filters are awkward in sqlc. Prefer explicit query variants or a small query builder over string concatenation.
- Pagination belongs in the query. Do not fetch all rows and slice in Go.
- `SELECT *` couples the generated struct to the table. Select explicit columns for stable contracts.
- Check the generated method signature before writing the service. Names and parameter structs are easy to guess wrong.
- Regenerate after every schema or query change and commit the generated output if the project does.

## Testing

- Unit-test service behavior with a fake consumer interface.
- Integration-test the real generated queries against the real database engine.
- Test empty results, malformed identifiers, tenant scope, canceled contexts, and transaction rollback.
- For money paths, test rounding and boundary amounts.

## Go safety checklist

- [ ] No `panic` on user-controlled input.
- [ ] `context.Context` forwarded to database and external calls.
- [ ] Errors wrapped, not swallowed.
- [ ] No `float64` for money unless justified.
- [ ] Transactions explicit and rolled back on error.
- [ ] Tenant scope applied in every query path, including background jobs.
- [ ] Generated method names and types verified against actual output.
- [ ] No raw SQL in handlers.
- [ ] Bounded queries: pagination, limits, timeouts.

## GORM and sqlx

- **GORM:** keep models out of handlers. Use focused repositories for nontrivial queries. Avoid generic CRUD wrappers around `db.Model(...)`.
- **sqlx:** repositories are usually worth it for scan mapping and composite queries. Keep SQL in repository files, not services.
- **Both:** keep transaction boundaries explicit in the service layer.

## Further reading

- sqlc documentation: https://docs.sqlc.dev/
- Uber Go Style Guide: https://github.com/uber-go/guide/blob/master/style.md
- Google Go Style Decisions: https://google.github.io/styleguide/go/decisions
