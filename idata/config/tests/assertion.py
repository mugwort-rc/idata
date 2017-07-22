from unittest import TestCase

from .. import assertion
from .. import csv


class TestRowAssertion(TestCase):
    def setUp(self):
        self.config = csv.CSVTableSourceConfig(columns=[{
            "name": "hoge",
        }])

    def test_assert_eq(self):
        row_assert = assertion.RowAssertion(self.config, {
            "type": "row",
            "f": "eq",
            "args": {
                "source": 0,
                "value": "hoge",
            },
        })
        self.assertEqual(row_assert.check(["hoge"]), True)
        self.assertEqual(row_assert.check(["fuga"]), False)

    def test_assert_in(self):
        row_assert = assertion.RowAssertion(self.config, {
            "type": "row",
            "f": "in",
            "args": {
                "value": "o",
                "source": 0,
            },
        })
        self.assertEqual(row_assert.check(["hoge"]), True)
        self.assertEqual(row_assert.check(["fuga"]), False)
        self.assertEqual(row_assert.check(["piyo"]), True)
