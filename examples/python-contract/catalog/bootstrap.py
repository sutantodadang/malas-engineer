"""Composition root is the only place that creates concrete collaborators."""
from .api import get_book_response
from .repository import MemoryBookRepository
from .service import Book, BookService

def build_application():
    repository = MemoryBookRepository({"1": Book("1", "Verified")})
    service = BookService(repository)
    return lambda book_id: get_book_response(service, book_id)
