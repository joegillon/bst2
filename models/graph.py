import os
import csv

flds = ['name', 'value']


class Graph(object):

    def __init__(self, d=None):
        for fld in flds:
            setattr(self, fld, None)
        if d:
            for attr in self.__dict__:
                if attr in d:
                    setattr(self, attr, d[attr])

    @staticmethod
    def get():
        graphs = []
        cwd = os.getcwd()
        path = '%s/data/graphs.csv' % cwd
        with open(path, 'r') as f:
            rdr = csv.DictReader(f)
            for row in rdr:
                graphs.append(Graph(row))

        return graphs
