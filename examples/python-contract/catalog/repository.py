"""Persistence adapter; a real app would use Django ORM or SQLAlchemy here."""
from .service import Book

class MemoryBookRepository:
    def __init__(self, books: dict[str, Book]) -> None:
        self.books = books

    def get(self, book_id: str) -> Book | None:
        return self.books.get(book_id)
