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
    nhood = Neighborhood(name)
    nhood.state = gbl.config['state']
    nhood.city = gbl.config['city']
    nhood.streets = streets
    nhood.voters = []
    return nhood


def save_nhood(nhood):
    voterdf = get_my_voters(nhood)
    voterdf = add_hx(voterdf)
    if 'Ballots' in gbl.config:
        add_ballots(voterdf, gbl.config['Ballots']['date'])
    save_nhood_streets(nhood)
    save_nhood_voters(nhood, voterdf)
    print('Done!')


def get_my_voters(nhood):
    print('Getting all voters...')
    path = '%s/bst_data/voters.pickle' % gbl.config['app_path']
    all_vdf = pd.read_pickle(path)

    # Just my city
    print('Just %s voters...' % nhood.city)
    all_vdf = all_vdf[all_vdf.city == nhood.city.upper()]

    my_vdf = pd.DataFrame()

    # Just the neighborhood streets
    for nhood_street in nhood.streets:
        print('Just the voters for %s...' % nhood_street.name)
        x = all_vdf[all_vdf.street_address.str.contains(nhood_street.name.upper())]
        my_vdf = pd.concat([my_vdf, x], axis=0)

    # But some only have certain blocks
    # First make 2 new columns to separate house numbers & street names
    house_number = []
    street_name = []
    for addr in my_vdf.street_address:
        nbr, name, unit = adl.parse(addr)
        house_number.append(nbr)
        street_name.append(name)
    my_vdf['house_number'] = house_number
    my_vdf['street_name'] = street_name

    print('Getting voters for specified blocks...')
    for nhood_street in nhood.streets:
        nhood_street_name = nhood_street.name.upper()
        index_list = []
        if nhood_street.lo:
            index_list += list(my_vdf[(my_vdf.street_name == nhood_street_name) &
                                      (my_vdf.house_number < int(nhood_street.lo))].index)
        if nhood_street.hi:
            index_list += list(my_vdf[(my_vdf.street_name == nhood_street_name) &
                                      (my_vdf.house_number > int(nhood_street.hi))].index)
        if nhood_street.side == 'E':
            index_list += list(my_vdf[(my_vdf.street_name == nhood_street_name) &
                                      (my_vdf.house_number % 2 != 0)].index)
        if nhood_street.side == 'O':
            index_list += list(my_vdf[(my_vdf.street_name == nhood_street_name) &
                                      (my_vdf.house_number % 2 == 0)].index)
        my_vdf.drop(index_list, inplace=True)

    return my_vdf


def add_hx(vdf):
    print('Adding voter history and avidity scores...')
    print('Getting all voter history records...')
    hdf = pd.read_pickle('%s/bst_data/hx.pickle' % gbl.config['app_path'])

    print('Just history records for my voters...')
    my_hdf = hdf[hdf.voter_id.isin(set(vdf.voter_id))]

    elections = pd.read_pickle('%s/bst_data/elections.pickle' % gbl.config['app_path'])

    voters = vdf.to_dict('records')

    print('Just my voters...')
    for voter in voters:
        voter['age_group'] = dtl.get_age_group(voter['birth_year'])
        voter['reg_date'] = dtl.to_string(reg_date_to_date(voter['reg_date']))
        voter['score'] = '0 (0/0)'
        hx_rex = my_hdf[my_hdf.voter_id == voter['voter_id']]
        earliest_edate = hx_rex.election_date.min()
        if (pd.isna(earliest_edate)) or (voter['reg_date'] < earliest_edate):
            earliest_edate = voter['reg_date']
        voter_election_ids = list(hx_rex.election_id)
        possible_score = 0
        actual_score = 0
        for election in elections:
            eyear = int(election.date[0:4])
            if election.id in voter_election_ids:
                voter[election.date] = 'Y'
                possible_score += election.score
                actual_score += election.score
            elif eyear < election.birth_yr:
                voter[election.date] = 'U'
            elif election.date > earliest_edate:
                voter[election.date] = 'N'
                possible_score += election.score
            else:
                voter[election.date] = 'X'

        if possible_score:
            voter['score'] = '%.2f (%d/%d)' % (
                actual_score / possible_score,
                actual_score, possible_score)

    return pd.DataFrame.from_dict(voters)


def add_ballots(vdf, election_date):
    print('Adding ballot selection...')
    print('Getting all ballots...')
    app_path = gbl.config['app_path']
    path = '%s/bst_data/ballots.pickle' % app_path
    bdf = pd.read_pickle(path)

    print('Just history records for my voters...')
    bdf = bdf[bdf.voter_id.isin(set(vdf.voter_id))]

    print('Just ballots for my voters...')
    bid = list(bdf.voter_id.unique())
    for vid in vdf.voter_id:
        if vid in bid:
            party = bdf.loc[bdf.voter_id == vid, 'party'].values[0]
            vdf.loc[vdf.voter_id == vid, election_date] = party


def reg_date_to_date(rd):
    return dtl.to_date(str(rd), '%m%d%Y')


def save_nhood_streets(nhood):
    print('Saving streets for %s...' % nhood.name)
    nhood_name = nhood.name.replace(' ', '_')
    path = '%s/my_data/%s_streets.csv' % (gbl.config['app_path'], nhood_name)
    with open(path, 'w', newline='') as f:
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


def save_nhood_voters(nhood, vdf):
    print('Saving voters for %s...' % nhood.name)
    nhood_name = nhood.name.replace(' ', '_')
    path = '%s/my_data/%s_voters.csv' % (gbl.config['app_path'], nhood_name)
    vdf.to_csv(path, index=False, header=True)
