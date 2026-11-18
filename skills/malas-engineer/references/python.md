# Python explicit layers: Django and FastAPI

Django: `views` handles HTTP/serialization, `services` handles workflow/business decisions, `repositories` (optional) handles complex queries/persistence seams; `models` remains ORM models. FastAPI: `routers` -> `services` -> repository/adapter -> DB. Composition through app factory or FastAPI Depends at boundary; Django service construction in view/factory explicit.

```python
from typing import Protocol

class InvoiceStore(Protocol):
    def find(self, invoice_id: str) -> "Invoice | None": ...

class InvoiceService:
    def __init__(self, store: InvoiceStore) -> None:
        self._store = store

    def get_invoice(self, invoice_id: str) -> "Invoice":
        invoice = self._store.find(invoice_id)
        if invoice is None:
            raise InvoiceNotFound(invoice_id)
        return invoice

# Composition root, not in service:
service = InvoiceService(DjangoInvoiceStore())
```

This is a schematic example; `Invoice`, `InvoiceNotFound`, and `DjangoInvoiceStore` must be declared in real code.

No `Model.objects` inside reusable service when complex persistence boundary is intended; however direct ORM in a small service may be an intentional Django convention if injecting a wrapper adds no value. Explicitly explain choice. No global service singleton holding mutable request state. Keep type hints, PEP 8, clear exceptions and proper transaction atomicity.

Do NOT automatically move each small business function into its own file. `services/import_service.py` is correct when import orchestration forms one cohesive job. A named `csv_parser.py` is justified when parsing has independent tests/rules.
