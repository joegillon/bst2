import unittest

import lib.addr_lib as adl


class TestAddrLib(unittest.TestCase):

    def test_parse(self):
        s = '110A S MAIN ST NW'
        num, st = adl.parse(s)
        self.assertEqual(110, num)
        self.assertEqual('S MAIN ST NW APT A', st)

        s = '332 ISLAND DR APT 101'
        num, st = adl.parse(s)
        self.assertEqual(332, num)
        self.assertEqual('ISLAND DR APT 101', st)
