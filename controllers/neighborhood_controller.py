import os
import csv
import pandas as pd
import pickle
import globals as gbl
import lib.addr_lib as adl
import lib.date_lib as dtl
import lib.scraper_lib as scraper
from models.neighborhood import Neighborhood
from models.neighborhood_street import NeighborhoodStreet


def get_city_streets():
    path = '%s/bst_data/streets.pickle' % gbl.config['app_path']
    if os.path.exists(path):
        with open(path, 'rb') as f:
            streets = pickle.load(f)
        return streets

    state = gbl.config['state']
    city = gbl.config['city']
    street_names = scraper.scrape_streets(state, city)

    streets = [NeighborhoodStreet({'name': street}) for street in street_names]

    path = '%s/bst_data/streets.pickle' % gbl.config['app_path']
    print('Pickling %d streets...' % len(streets))
    with open(path, 'wb') as f:
        pickle.dump(streets, f)

    return streets
    

def get_house_nums(street):
    state = gbl.config['state']
    city = gbl.config['city']
    street.house_nums = scraper.scrape_house_nums(state, city, street)
    street.lo = street.house_nums[0]
    street.hi = street.house_nums[-1]
    street.side = 'B'

    path = '%s/bst_data/streets.pickle' % gbl.config['app_path']
    with open(path, 'rb') as f:
        streets = pickle.load(f)

    my_street = [s for s in streets if s.name == street.name][0]
    my_street.lo = street.house_nums[0]
    my_street.hi = street.house_nums[-1]
    my_street.side = 'B'
    my_street.house_nums = street.house_nums

    with open(path, 'wb') as f:
        pickle.dump(streets, f)


def new_nhood(name, streets):
    state = gbl.config['state']
    city = gbl.config['city']
    for street in streets:
        scrape_house_nums(state, city, street)
    # get voters
    # add hx
    # add ballots

    nhood = Neighborhood(name)
    nhood.state = gbl.config['state']
    nhood.city = gbl.config['city']
    return nhood


def add_nhood_street(obj):
    obj.house_nums = scrape_house_nums(gbl.config['state'], gbl.config['city'], obj.name)
    update_streets_file(obj)
    return obj


def update_streets_file(obj):
    path = '%s/bst_data/streets.pickle' % gbl.config['app_path']
    with open(path, 'rb') as f:
        streets = pickle.load(f)

    street = [s for s in streets if s.name == obj.name][0]
    street.house_nums = obj.house_nums

    with open(path, 'wb') as f:
        pickle.dump(streets, f)

# def add_street(nhood, name, lo, hi, oe):
#     street = NeighborhoodStreet({
#         'name': name,
#         'lo': lo,
#         'hi': hi,
#         'oe': oe
#     })
#     scrape_house_nums(nhood.state, nhood.city, street)
#     nhood.streets.append(street)


def edit_street(nhood, idx, new_street):
    nhood.streets[idx] = new_street


def drop_street(nhood, idx):
    del nhood.streets[idx]


def save_nhood(nhood):
    my_voters = get_my_voters(nhood)
    add_hx(my_voters)
    save_nhood_streets(nhood)
    save_nhood_voters(nhood, my_voters)


def get_my_voters(nhood):
    path = 'bst_data/voters/%s.csv' % nhood.city
    all_voters = pd.read_csv(path)

    # Just the neighborhood streets
    my_voters = pd.DataFrame()
    for nhood_street in nhood.streets:
        x = all_voters[all_voters.street_address.str.contains(nhood_street.name)]
        my_voters = pd.concat([my_voters, x], axis=0)

    # But some only have certain blocks
    # First make 2 new columns to separate house numbers & street names
    house_number = []
    street_name = []
    for addr in my_voters.street_address:
        nbr, name, unit = adl.parse(addr)
        house_number.append(nbr)
        street_name.append(name)
    my_voters['house_number'] = house_number
    my_voters['street_name'] = street_name

    for nhood_street in nhood.streets:
        index_list = []
        if nhood_street.lo:
            index_list += list(my_voters[(my_voters.street_name == nhood_street.name) &
                                         (my_voters.house_number < int(nhood_street.lo))].index)
        if nhood_street.hi:
            index_list += list(my_voters[(my_voters.street_name == nhood_street.name) &
                                         (my_voters.house_number > int(nhood_street.hi))].index)
        if nhood_street.side == 'E':
            index_list += list(my_voters[(my_voters.street_name == nhood_street.name) &
                                         (my_voters.house_number % 2 != 0)].index)
        if nhood_street.side == 'O':
            index_list += list(my_voters[(my_voters.street_name == nhood_street.name) &
                                         (my_voters.house_number % 2 == 0)].index)
        my_voters.drop(index_list, inplace=True)

    return my_voters


def add_hx(my_voters):
    hx = pd.read_csv('bst_data/hx.csv')
    my_hx = hx[hx.voter_id.isin(set(my_voters.voter_id))]

    elections = pd.read_csv('bst_data/elections.csv')

    # add_edate(my_hx, elections)

    elections = elections.to_dict('records')

    my_voters = my_voters.to_dict('records')

    for voter in my_voters:
        voter['age_group'] = dtl.get_age_group(voter['birth_year'])
        voter['reg_date'] = dtl.to_string(reg_date_to_date(voter['reg_date']))
        voter['score'] = '0 (0/0)'
        hx_rex = my_hx[my_hx.voter_id == voter['voter_id']]
        earliest_edate = hx_rex.election_date.min()
        if (pd.isna(earliest_edate)) or (voter['reg_date'] < earliest_edate):
            earliest_edate = voter['reg_date']
        voter_election_ids = list(hx_rex.election_id)
        possible_score = 0
        actual_score = 0
        for election in elections:
            eyear = int(election['date'][0:4])
            if election['id'] in voter_election_ids:
                voter[election['date']] = 'Y'
                possible_score += election['score']
                actual_score += election['score']
            elif eyear < election['birth_yr']:
                voter[election['date']] = 'U'
            elif election['date'] > earliest_edate:
                voter[election['date']] = 'N'
                possible_score += election['score']
            else:
                voter[election['date']] = 'X'

        if possible_score:
            voter['score'] = '%.2f (%d/%d)' % (
                actual_score / possible_score,
                actual_score, possible_score)

    return my_voters


def add_edate(hx_df, election_df):
    # Prevent a buttload of strange warnings
    pd.set_option('mode.chained_assignment', None)

    hx_df['election_date'] = 0
    for hx_eid in pd.unique(hx_df.election_id):
        d = election_df[election_df.id == hx_eid].iloc[0, 1]
        hx_df.loc[hx_df.election_id == hx_eid, 'election_date'] = d


def reg_date_to_date(rd):
    return dtl.to_date(str(rd), '%m%d%Y')


def save_nhood_streets(nhood):
    nhood_name = nhood.name.replace(' ', '_')
    fname = '%s_nhood.csv' % nhood_name
    with open('my_data/%s' % fname, 'w', newline='') as f:
        wtr = csv.DictWriter(f, fieldnames=[
            'name', 'lo', 'hi', 'side'])
        wtr.writeheader()
        for street in nhood.streets:
            wtr.writerow({
                'name': street.name,
                'lo': street.lo,
                'hi': street.hi,
                'side': street.side
            })


def save_nhood_voters(nhood, voters):
    pass
