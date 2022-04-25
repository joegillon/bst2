import os
import csv
from models.neighborhood_street import NeighborhoodStreet
from models.voter import Voter


class Neighborhood(object):

    def __init__(self, city, name):
        self.city = city.replace(' ', '_')
        self.name = name.replace(' ', '_')
        self.streets = []
        self.voters = []

    @staticmethod
    def get():
        data_dir = '%s/my_data' % os.getcwd()
        nhoods = []
        for file in os.scandir(data_dir):
            parts = file.name.split('.')
            if 'nhood' in parts[0]:
                parts[0] = parts[0][:-6]
                n = parts[0].replace('_', ' ')
                nhood = Neighborhood('Ann Arbor', n)
                with open(file.path, 'r') as csv_file:
                    rdr = csv.DictReader(csv_file)
                    for st in rdr:
                        nhood.streets.append(NeighborhoodStreet(st))
                    nhood.voters = Voter.get(parts[0])
                nhoods.append(nhood)

        return nhoods

    @staticmethod
    def get_one(city, name):
        nhood = Neighborhood(city, name)
        path = '%s/data/neighborhoods/%s.csv' % \
            (os.getcwd(), nhood.name)
        with open(path, 'r') as f:
            rdr = csv.DictReader(f)
            for street in rdr:
                nhood.streets.append(NeighborhoodStreet(street))
        return nhood
