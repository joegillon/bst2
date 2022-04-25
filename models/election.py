import os
import csv
import lib.date_lib as dtl

flds = ['id', 'date', 'description', 'birth_yr', 'score']


class Election(object):

    def __init__(self, d=None):
        for fld in flds:
            setattr(self, fld, None)
        if d:
            for attr in self.__dict__:
                if attr in d:
                    setattr(self, attr, d[attr])

    def __str__(self):
        return '%s, %s' % (self.description, self.date)

    @staticmethod
    def get_score(dt, desc):
        m = dt.month
        y = dt.year
        if m == 11:
            if dtl.is_leap_year(y):
                return 1
            if y % 2 == 0:
                return 2

        if 'PRESIDENTIAL PRIMARY' in desc:
            return 3

        if 'STATE' in desc:
            return 4

        return 5

    @staticmethod
    def get_my():
        return Election.get('my')

    @staticmethod
    def get_bst():
        return Election.get('bst')

    @staticmethod
    def get(folder):
        elections = []
        cwd = os.getcwd()
        path = '%s/%s_data/elections.csv' % (cwd, folder)
        if not os.path.exists(path):
            return []
        with open(path, 'r') as f:
            rdr = csv.DictReader(f)
            for row in rdr:
                elections.append(Election(row))

        return elections

    @staticmethod
    def save(elections):
        cwd = os.getcwd()
        path = '%s/my_data/elections.csv' % (cwd,)
        with open(path, 'w', newline='') as f:
            wtr = csv.DictWriter(f, fieldnames=flds)
            wtr.writeheader()
            for election in elections:
                wtr.writerow(election.__dict__)
