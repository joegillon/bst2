import unittest
import os
import controllers.neighborhood_controller as controller
from models.neighborhood_street import NeighborhoodStreet
from models.neighborhood import Neighborhood


class TestNeighborhoodController(unittest.TestCase):

    def setUp(self):
        import globals as gbl

        gbl.config = {
            'state': 'MI', 'state_name': 'Michigan', 'city': 'Ann Arbor',
            'app_path': os.getcwd()[0:-18],
            'Ballots': {'date': '2016-03-08'}
        }

    def tearDown(self) -> None:
        pass

    def testSaveNhood(self):
        nhood = Neighborhood('Test')
        nhood.state = 'MI'
        nhood.city = 'Ann Arbor'
        nhood.streets = [
            NeighborhoodStreet({
                'name': 'Bruce St', 'lo': '401', 'hi': '1033', 'side': 'B'
            }),
            NeighborhoodStreet({
                'name': 'Miller Ave', 'lo': '1775', 'hi': '2133', 'side': 'O'
            })
        ]
        controller.save_nhood(nhood)
        pass
