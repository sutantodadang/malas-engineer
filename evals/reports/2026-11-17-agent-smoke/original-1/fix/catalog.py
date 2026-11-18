class CatalogService:
    def __init__(self, reader):
        self.reader = reader

    def title(self, book_id):
        book_id = book_id.strip()
        if not book_id:
            raise ValueError("book_id must not be empty")
        title = self.reader.get(book_id)
        if title is None:
            raise LookupError(book_id)
        return title


DEFAULT_READER = {"1": "Default title"}
