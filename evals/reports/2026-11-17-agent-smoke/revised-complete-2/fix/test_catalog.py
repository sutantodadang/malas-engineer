import unittest
from unittest.mock import Mock

from catalog import CatalogService


class CatalogServiceTests(unittest.TestCase):
    def test_supplied_reader_controls_result(self):
        self.assertEqual(CatalogService({"1": "Supplied"}).title("1"), "Supplied")
        self.assertEqual(CatalogService({"1": "Other"}).title("1"), "Other")

    def test_strips_id_before_lookup(self):
        reader = Mock()
        reader.get.return_value = "Supplied"
        self.assertEqual(CatalogService(reader).title(" \t1\n"), "Supplied")
        reader.get.assert_called_once_with("1")

    def test_empty_id_rejected_before_lookup(self):
        for book_id in ("", " \t\n"):
            with self.subTest(book_id=book_id):
                reader = Mock()
                with self.assertRaises(ValueError):
                    CatalogService(reader).title(book_id)
                reader.get.assert_not_called()

    def test_missing_book_raises_lookup_error(self):
        for book_id in ("1", "missing"):
            with self.subTest(book_id=book_id):
                with self.assertRaises(LookupError):
                    CatalogService({}).title(book_id)

    def test_empty_title_is_not_missing(self):
        self.assertEqual(CatalogService({"1": ""}).title("1"), "")

    def test_reader_failure_propagates_unchanged(self):
        error = RuntimeError("reader unavailable")
        reader = Mock()
        reader.get.side_effect = error
        with self.assertRaises(RuntimeError) as caught:
            CatalogService(reader).title("1")
        self.assertIs(caught.exception, error)


if __name__ == "__main__":
    unittest.main()
