# Catalog refresh

Each service wraps its own store. Record keys and view names can be any strings. The store returns a fresh result for each load and may fail. Callers await `service.refresh(key, view)` for a value or the original error.
