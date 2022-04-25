import os
import csv
import pandas as pd
import lib.addr_lib as adl
import lib.date_lib as dtl

flds = [
    'last_name', 'first_name', 'middle_name', 'name_suffix',
    'birth_year', 'gender', 'age_group',
    'street_address', 'city', 'zipcode', 'county',
    'jurisdiction', 'ward', 'precinct',
    'congress', 'state_senate', 'state_house',
    'voter_id', 'reg_date', 'status', 'absentee', 'party',
    'nhood', 'score'
]


class Voter(object):

    def __init__(self, d=None):
        for fld in flds:
            setattr(self, fld, None)
        if d:
            for attr in d:
                if attr in d:
                    setattr(self, attr, d[attr])

    def __str__(self):
        s = '%s, %s' % (self.last_name, self.first_name)
        if self.middle_name:
            s += ' %s' % self.middle_name
        if self.name_suffix:
            s += ', %s' % self.name_suffix
        return s

    def addr_cmp(self, other, ascending):
        me_num, me_street, me_unit = adl.parse(self.street_address)
        oth_num, oth_street, oth_unit = adl.parse(other.street_address)
        if me_street != oth_street:
            return me_street > oth_street if ascending else me_street < oth_street
        if me_num != oth_num:
            return me_num >= oth_num if ascending else me_num < oth_num
        return me_unit >= oth_unit if ascending else me_unit < oth_unit

    @staticmethod
    def get(nhood):
        voters = []
        path = '%s/my_data/%s_voters.csv' % (os.getcwd(), nhood)
        with open(path, 'r') as f:
            rdr = csv.DictReader(f)
            for row in rdr:
                voters.append(Voter(row))

        return voters

    @staticmethod
    def build_my_voters(nhood):
        # path = '%s/data/mi/voters.csv' % (os.getcwd(),)
        # all_voters = pd.read_csv(path)
        # all_voters = all_voters[all_voters.city == nhood.city]

        path = '%s/data/voters/%s.csv' % (os.getcwd(), nhood.city)
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
            if nhood_street.oe == 'E':
                index_list += list(my_voters[(my_voters.street_name == nhood_street.name) &
                                             (my_voters.house_number % 2 != 0)].index)
            if nhood_street.oe == 'O':
                index_list += list(my_voters[(my_voters.street_name == nhood_street.name) &
                                             (my_voters.house_number % 2 == 0)].index)
            my_voters.drop(index_list, inplace=True)

        hx = pd.read_csv('data/mi/hx.csv')
        my_hx = hx[hx.voter_id.isin(set(my_voters.voter_id))]

        elections = pd.read_csv('data/mi/elections.csv')

        Voter.add_edate(my_hx, elections)

        elections = elections.to_dict('records')

        my_voters = my_voters.to_dict('records')

        for voter in my_voters:
            voter['age_group'] = dtl.get_age_group(voter['birth_year'])
            voter['reg_date'] = dtl.to_string(Voter.reg_date_to_date(voter['reg_date']))
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

        my_voters = pd.DataFrame(my_voters)
        path = 'data/voters/%s_voters.csv' % nhood.name
        my_voters.to_csv(path, header=True, index=False)

    @staticmethod
    def add_edate(hx_df, election_df):
        # Prevent a buttload of strange warnings
        pd.set_option('mode.chained_assignment', None)

        hx_df['election_date'] = 0
        for hx_eid in pd.unique(hx_df.election_id):
            d = election_df[election_df.id == hx_eid].iloc[0, 1]
            hx_df.loc[hx_df.election_id == hx_eid, 'election_date'] = d

    @staticmethod
    def reg_date_to_date(rd):
        return dtl.to_date(str(rd), '%m%d%Y')

    @staticmethod
    def add_ballots(nhoods):
        cwd = os.getcwd()
        path = '%s/data/mi/sos/Democrats.csv' % cwd
        dems = pd.read_csv(path)
        path = '%s/data/mi/sos/Republicans.csv' % cwd
        reps = pd.read_csv(path)
        for nhood in nhoods:
            voter_path = '%s/data/voters/%s_voters.csv' % (cwd, nhood)
            vdf = pd.read_csv(voter_path)

            vdf.party = 'X'

            nhood_dems = dems[dems.VOTERID.isin(vdf.voter_id)]
            nhood_reps = reps[reps.VOTERID.isin(vdf.voter_id)]

            for vid in nhood_dems.VOTERID:
                vdf.loc[vdf.voter_id == vid, 'party'] = 'D'

            for vid in nhood_reps.VOTERID:
                vdf.loc[vdf.voter_id == vid, 'party'] = 'R'

            vdf.to_csv(voter_path, header=True, index=False)
