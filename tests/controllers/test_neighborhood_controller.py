import unittest
import os
import controllers.neighborhood_controller as controller
from models.neighborhood_street import NeighborhoodStreet
from models.neighborhood import Neighborhood


class TestNeighborhoodController(unittest.TestCase):

    def setUp(self):
        self.cwd = os.getcwd()[0:-18]

    def tearDown(self) -> None:
        pass

    def testGetStateCity(self):
        path = '%s/config.ini' % self.cwd
        state, city = controller.get_config(path)
        self.assertEqual('MI', state)
        self.assertEqual('Ann Arbor', city)

    def testScrapeStreets(self):
        path = '%s/bst_data/streets.txt' % self.cwd
        controller.scrape_streets('MI', 'Ann Arbor', path)
        pass

    def testScrapeHouseNums(self):
        street = NeighborhoodStreet({
            'name': 'Bruce St', 'lo': None, 'hi': None, 'oe': None, 'house_nums': []
        })
        street.name = 'Bruce St'
        controller.scrape_house_nums('MI', 'Ann Arbor', street)
        pass

    def testAddStreet(self):
        nhood = Neighborhood('Bruce St')
        nhood.state = 'MI'
        nhood.city = 'Ann Arbor'
        street = NeighborhoodStreet({
            'name': 'Bruce St', 'lo': None, 'hi': None, 'oe': None, 'house_nums': []
        })
        controller.add_street(nhood, 'Bruce St', None, None, None)
        pass
