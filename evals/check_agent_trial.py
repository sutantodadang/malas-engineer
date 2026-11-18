"""Independently check a generated trial: python evals/check_agent_trial.py TRIAL_DIR."""
import importlib.util
import inspect
import sys
import unittest
from pathlib import Path

TRIAL = Path(sys.argv.pop(1)).resolve()
SOURCE = Path(__file__).parent / 'fixtures/agent-task/catalog.py'
spec = importlib.util.spec_from_file_location('trial_catalog', TRIAL / 'fix/catalog.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


class Acceptance(unittest.TestCase):
    def test_supplied_reader_and_normalized_id(self):
        self.assertEqual(catalog.CatalogService({'7': 'Injected'}).title(' 7 '), 'Injected')

    def test_blank_id_rejected_before_io(self):
        class UnexpectedReader:
            def get(self, key):
                raise AssertionError('lookup must not run')
        for value in ('', ' \t\n'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                catalog.CatalogService(UnexpectedReader()).title(value)

    def test_missing_book(self):
        with self.assertRaises(LookupError):
            catalog.CatalogService({}).title('missing')

    def test_reader_exception_identity_is_preserved(self):
        error = OSError('offline')
        class BrokenReader:
            def get(self, key):
                raise error
        with self.assertRaises(OSError) as caught:
            catalog.CatalogService(BrokenReader()).title('1')
        self.assertIs(caught.exception, error)

    def test_empty_title_is_not_missing(self):
        self.assertEqual(catalog.CatalogService({'1': ''}).title('1'), '')

    def test_public_signatures_preserved(self):
        self.assertEqual(list(inspect.signature(catalog.CatalogService).parameters), ['reader'])
        self.assertEqual(list(inspect.signature(catalog.CatalogService.title).parameters), ['self', 'book_id'])

    def test_review_source_unchanged(self):
        self.assertEqual((TRIAL / 'review/catalog.py').read_bytes(), SOURCE.read_bytes())

    def test_review_did_not_add_code_or_tests(self):
        code = {p.relative_to(TRIAL / 'review').as_posix()
                for p in (TRIAL / 'review').rglob('*.py')}
        self.assertEqual(code, {'catalog.py'})


if __name__ == '__main__':
    unittest.main(verbosity=2)
