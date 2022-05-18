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
                if 'streets' in file.name:
                    nhood_name = file.name.split('.')[0][:-8]
                    nhood = Neighborhood(nhood_name)
                    nhood.get(file.path)
                    nhoods[nhood_name] = nhood

        self.my_neighborhoods = nhoods

        self.res_rex = self.build_residence_data()

    def build_residence_data(self):
        rex = []
        for nhood in list(self.my_neighborhoods.values()):
            d = {}
            for voter in nhood.voters:
                voter_addr = '%s %s' % (voter.house_number, voter.street_name)
                if voter_addr not in d:
                    d[voter_addr] = []
                d[voter_addr].append(voter)
            for street in nhood.streets:
                for house_num in street.house_nums:
                    num = house_num.strip()
                    st = street.name.upper().strip()
                    street_addr = num + ' ' + st
                    if street_addr not in d:
                        rex.append(self.no_voter_at(num, st))
                    else:
                        for vrec in d[street_addr]:
                            rex.append(vrec)

        return rex

    def no_voter_at(self, house_num, street_name):
        voter = Voter()
        voter.street_address = house_num + ' ' + street_name
        voter.house_number = house_num
        voter.street_name = street_name
        return voter

    def save_my_elections(self, elections):
        # rebuild voters
        path = '%s/my_data/elections.csv' % self.cwd
        Election.save(path, elections)
