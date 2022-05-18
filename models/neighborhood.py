import os
import csv
from models.neighborhood_street import NeighborhoodStreet
from models.voter import Voter


class Neighborhood(object):

    def __init__(self, name):
        self.name = name
        self.state = None
        self.city = None
        self.streets = []
        self.voters = []

    # # @staticmethod
    # # def get():
    # #     data_dir = '%s/my_data' % os.getcwd()
    # #     nhoods = []
    # #     for file in os.scandir(data_dir):
    # #         parts = file.name.split('.')
    # #         if 'nhood' in parts[0]:
    # #             parts[0] = parts[0][:-6]
    # #             n = parts[0].replace('_', ' ')
    # #             nhood = Neighborhood('Ann Arbor', n)
    # #             with open(file.path, 'r') as csv_file:
    # #                 rdr = csv.DictReader(csv_file)
    # #                 for st in rdr:
    # #                     nhood.streets.append(NeighborhoodStreet(st))
    # #                 nhood.voters = Voter.get(parts[0])
    # #             nhoods.append(nhood)
    #
    #     return nhoods

    def get(self, path):
        with open(path, 'r') as f:
            rdr = csv.DictReader(f)
            for street in rdr:
                self.streets.append(NeighborhoodStreet(street))
                self.voters = Voter.get(path.replace('streets', 'voters'))
