import unittest
from catalog.bootstrap import build_application
from catalog.service import Book, BookNotFoundError, BookService

class FakeReader:
    def __init__(self): self.calls = []
    def get(self, book_id):
        self.calls.append(book_id)
        return Book(book_id, "Injected")

class ContractTests(unittest.TestCase):
    def test_uses_injected_reader(self):
        fake = FakeReader()
        self.assertEqual(BookService(fake).get_book("X").title, "Injected")
        self.assertEqual(fake.calls, ["X"])

    def test_invalid_id_does_not_hit_reader(self):
        fake = FakeReader()
        with self.assertRaises(ValueError): BookService(fake).get_book("")
        self.assertEqual(fake.calls, [])

    def test_real_wiring_reaches_transport(self):
        application = build_application()
        self.assertEqual(application("1"), (200, {"id":"1", "title":"Verified"}))
        self.assertEqual(application("missing")[0], 404)
        self.assertEqual(application("")[0], 400)

if __name__ == "__main__": unittest.main()
