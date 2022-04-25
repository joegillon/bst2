import os
import csv

flds = [
    'voter_id', 'election_id', 'absentee'
]


class VoterHx(object):

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
    def build_hx(county_num):
        cwd = os.getcwd()
        infile = '%s/data/mi/sos/entire_state_h.lst' % cwd
        outfile = '%s/data/mi/hx.csv' % cwd
        with open(outfile, 'w', newline='') as outf:
            wtr = csv.DictWriter(outf, fieldnames=flds)
            wtr.writeheader()
            with open(infile, 'r') as inf:
                for line in inf.readlines():
                    county_id = int(line[13:15].replace('\\', '').strip())
                    if county_id != county_num:
                        continue
                    d = {
                        'voter_id': int(line[0:13].replace('\\', '').strip()),
                        'election_id': int(line[25:38].replace('\\', '').strip()),
                        'absentee': line[38].replace('\\', '').strip()
                    }
                    wtr.writerow(d)
