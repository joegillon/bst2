import os
import csv
import globals as gbl
import lib.addr_lib as adl
import lib.date_lib as dtl
from models.neighborhood import Neighborhood
from models.election import Election
from models.neighborhood_street import NeighborhoodStreet


def get_nhoods():
    return gbl.dataset.my_neighborhoods

def get_election_dates():
    path = '%s/my_data/elections.csv' % gbl.config['app_path']
    elections = Election.get(path)
    gbl.dataset['elections'] = elections
    return [e.date for e in elections]
