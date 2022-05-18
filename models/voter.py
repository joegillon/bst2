import csv
import lib.addr_lib as adl

flds = [
    'last_name', 'first_name', 'middle_name', 'name_suffix',
    'date_of_birth', 'birth_year', 'age_group', 'gender', 'ethnicity',
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
        if not self.last_name:
            return ''
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
    def get(path):
        voters = []
        with open(path, 'r') as f:
            rdr = csv.DictReader(f)
            for row in rdr:
                voters.append(Voter(row))

        return voters
