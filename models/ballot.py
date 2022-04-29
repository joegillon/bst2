flds = [
    'voter_id', 'county_id', 'party',
    'last_name', 'first_name', 'middle_name', 'name_suffix',
    'street_address', 'city', 'zipcode'
]


class Ballot(object):

    def __init__(self, d=None):
        for fld in flds:
            setattr(self, fld, None)
        if d:
            for attr in self.__dict__:
                if attr in d:
                    setattr(self, attr, d[attr])

    def __str__(self):
        s = '%s, %s' % (self.last_name, self.first_name)
        if self.middle_name:
            s += ' %s' % self.middle_name
        if self.name_suffix:
            s += ', %s' % self.name_suffix
        return s
