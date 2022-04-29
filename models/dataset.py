import os
from models.election import Election
from models.neighborhood import Neighborhood
from models.voter import Voter


class Dataset(object):

    def __init__(self):
        self.cwd = os.getcwd()

        self.state_elections = []
        self.my_elections = []
        self.my_neighborhoods = {}

        self.load_state_elections()
        self.load_my_elections()
        self.load_neighborhoods()

    def load_state_elections(self):
        path = '%s/bst_data/elections.csv' % self.cwd
        self.state_elections = Election.get(path)

    def load_my_elections(self):
        path = '%s/my_data/elections.csv' % self.cwd
        self.my_elections = Election.get(path)

    def load_neighborhoods(self):
        nhoods = {}
        folder = self.cwd + '/my_data'
        with os.scandir(folder) as all_files:
            for file in all_files:
                if 'nhood' in file.name:
                    nhood_name = file.name.split('.')[0][:-6]
                    nhood = Neighborhood(nhood_name)
                    nhood.get(file.path)
                    nhoods[nhood_name] = nhood
                elif 'voters' in file.name:
                    nhood_name = file.name.split('.')[0][:-7]
                    nhoods[nhood_name].voters = Voter.get(file.path)
                else:
                    continue

        self.my_neighborhoods = nhoods

    def save_my_elections(self, elections):
        # rebuild voters
        path = '%s/my_data/elections.csv' % self.cwd
        Election.save(path, elections)
