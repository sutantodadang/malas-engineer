class CatalogService:
    def __init__(self, reader):
        self.reader = reader

    def title(self, book_id):
        return DEFAULT_READER.get(book_id)


DEFAULT_READER = {"1": "Default title"}
