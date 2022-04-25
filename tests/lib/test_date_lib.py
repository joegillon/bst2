import unittest
import lib.date_lib as dtl


class TestDateLib(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_get_age(self):
        byr = 1944
        expected = 77
        actual = dtl.get_age(byr)
        self.assertEqual(expected, actual)

        byr = 1999
        expected = 22
        actual = dtl.get_age(byr)
        self.assertEqual(expected, actual)

    def test_get_age_group(self):
        pass