import os
import csv
import pandas as pd
import pickle
from models.election import Election
from models.voter import flds as voter_flds
import lib.date_lib as dtl
import globals as gbl

hx_flds = [
    'voter_id', 'election_id', 'election_date', 'county_id', 'absentee'
]

ballot_flds = [
    'voter_id', 'county_id', 'party',
    'last_name', 'first_name', 'middle_name', 'name_suffix',
    'street_address', 'city', 'zipcode'
]


def import_sos_elections(qvf_file):
    from_year = 2010
    print('Importing MI elections from %d' % from_year)
    elections = []
    with qvf_file:
        for line in qvf_file:
            print(line.strip())
            date = dtl.to_date(line[13:21], '%m%d%Y')
            if date.year < from_year:
                continue
            desc = line[21:].strip()
            d = {
                'id': int(line[0:13].strip()),
                'date': dtl.to_string(date),
                'description': desc,
                'birth_yr': date.year - 18,
                'score': Election.get_score(date, desc)
            }
            elections.append(Election(d))

    elections = sorted(elections, key=lambda ele: ele.date, reverse=True)

    outfile = '%s/bst_data/elections.pickle' % gbl.config['app_path']
    with open(outfile, 'wb') as f:
        pickle.dump(elections, f)
    print('Done!')


def import_sos_voters(qvf_file):
    csv_path = '%s/bst_data/voters.csv' % gbl.config['app_path']
    with open(csv_path, 'w', newline='') as csv_file:
        wtr = csv.DictWriter(csv_file, fieldnames=voter_flds)
        wtr.writeheader()
        cnt = 0
        for line in qvf_file:
            try:
                wtr.writerow(qvf_voter_to_dict(line))
                cnt += 1
                if cnt % 10000 == 0:
                    print("{:,}".format(cnt))
            except Exception as e:
                print("Error: %s: %s" % (line, str(e)))
                return False

    print("Pickling {:,} voters...".format(cnt))
    df = pd.read_csv(csv_path)
    df.to_pickle('%s/bst_data/voters.pickle' % gbl.config['app_path'])
    os.remove(csv_path)
    print('Done!')

    return True     # State has a separate history file


def qvf_voter_to_dict(line):
    return {
        'last_name': line[0:35].replace('\\', '').strip(),
        'first_name': line[35:55].replace('\\', '').strip(),
        'middle_name': line[55:75].replace('\\', '').strip(),
        'name_suffix': line[75:78].replace('\\', '').strip(),
        'date_of_birth': None,
        'birth_year': line[78:82].replace('\\', '').strip(),
        'age_group': None,
        'gender': line[82].replace('\\', '').strip(),
        'ethnicity': None,
        'street_address': build_address(line),
        'city': line[156:191].replace('\\', '').strip(),
        'zipcode': line[193:198].replace('\\', '').strip(),
        'county': line[461:463].replace('\\', '').strip(),
        'jurisdiction': line[463:468].replace('\\', '').strip(),
        'ward': line[468:474][0:2].replace('\\', ''),
        'precinct': line[468:474][2:].replace('\\', '').strip(),
        'congress': line[489:494].replace('\\', '').strip(),
        'state_senate': line[484:489].replace('\\', '').strip(),
        'state_house': line[479:484].replace('\\', '').strip(),
        'voter_id': line[448:461].replace('\\', '').strip(),
        'reg_date': line[83:91],
        'status': line[517:519].replace('\\', '').strip(),
        'absentee': line[516].replace('\\', '').strip(),
        'party': None,
        'nhood': None,
        'score': None
    }


def build_address(line):
    house_number = line[92:99].replace('\\', '').strip()
    pre_direction = line[103:105].replace('\\', '').strip()
    street_name = line[105:135].replace('\\', '').strip()
    street_type = line[135:141].replace('\\', '').strip()
    suf_direction = line[141:143].replace('\\', '').strip()
    unit = line[143:156].replace('\\', '').strip()
    return '%s %s %s %s %s %s' % (
        house_number, pre_direction, street_name, street_type, suf_direction, unit
    )


def import_hx(qvf_file):
    election_dates = get_election_dates()
    csv_path = '%s/bst_data/hx.csv' % gbl.config['app_path']
    with open(csv_path, 'w', newline='') as csv_file:
        wtr = csv.DictWriter(csv_file, fieldnames=hx_flds)
        wtr.writeheader()
        cnt = 0
        with qvf_file:
            for line in qvf_file:
                election_id = int(line[25:38].strip())
                if election_id not in election_dates:
                    continue
                d = {
                    'voter_id': int(line[0:13].replace('\\', '').strip()),
                    'election_id': election_id,
                    'election_date': election_dates[election_id],
                    'county_id': int(line[13:15].replace('\\', '').strip()),
                    'absentee': line[38].replace('\\', '').strip()
                }
                wtr.writerow(d)
                cnt += 1
                if cnt % 10000 == 0:
                    print("{:,}".format(cnt))

    print("Pickling {:,} history records...".format(cnt))
    df = pd.read_csv(csv_path)
    df.to_pickle('%s/bst_data/hx.pickle' % gbl.config['app_path'])
    os.remove(csv_path)
    print('Done!')

    import_ballots()     # MI ballot files


def import_ballots():
    qvf_files = ['Democrats.csv', 'Republicans.csv']
    csv_path = '%s/bst_data/ballots.csv' % gbl.config['app_path']
    with open(csv_path, 'w', newline='') as csv_file:
        wtr = csv.DictWriter(csv_file, fieldnames=ballot_flds)
        wtr.writeheader()
        for sos_file in qvf_files:
            path = '%s/sos_data/%s' % (gbl.config['app_path'], sos_file)
            print('Importing ballot file %s' % path)
            with open(path, 'r') as sosf:
                rdr = csv.DictReader(sosf)
                cnt = 0
                for row in rdr:
                    d = {
                        'voter_id': row['VOTERID'],
                        'county_id': row['DLCOUNTYCODE'],
                        'party': row['PRIMARYBALTYPE'],
                        'last_name': row['LASTNAME'],
                        'first_name': row['FIRSTNAME'],
                        'middle_name': row['MIDDLENAME'],
                        'name_suffix': row['SUFFIX'],
                        'street_address': row['RESADDRESS1'],
                        'city': extract_city(row['RESADDRESS2']),
                        'zipcode': row['RESZIPCODE']
                    }
                    wtr.writerow(d)
                    cnt += 1
                    if cnt % 10000 == 0:
                        print("{:,}".format(cnt))

    print("Pickling {:,} ballot records...".format(cnt))
    df = pd.read_csv(csv_path)
    df.to_pickle('%s/bst_data/ballots.pickle' % gbl.config['app_path'])
    os.remove(csv_path)
    print('Done!')


def extract_city(ballot_field):
    parts = ballot_field.split()
    try:
        idx = parts.index('MI')
    except Exception as ex:
        return ballot_field     # Out of state!
    return ' '.join(parts[0:idx])


def get_election_dates():
    path = '%s/bst_data/elections.csv' % gbl.config['app_path']
    dates = {}
    with open(path, 'r') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            dates[int(row['id'])] = row['date']
    return dates
