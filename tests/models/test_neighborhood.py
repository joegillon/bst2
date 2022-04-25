import unittest
from models.neighborhood import Neighborhood


class NeighborhoodTestSuite(unittest.TestCase):

    def setUp(self):
        pass

    def test_get_all(self):
        nhoods = Neighborhood.get()
        pass

    def tearDown(self):
        pass
