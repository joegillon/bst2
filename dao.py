import os
import csv
from models.election import Election
from lib.ui_lib import eprint
import lib.date_lib as dtl


def elections_to_csv(qvf_file, view):
    from_year = 2010
    view.log('Importing MI elections from %d' % from_year)
    elections = []
    with qvf_file:
        for line in qvf_file:
            view.log(line.strip())
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
            elections.append(d)

    elections = sorted(elections, key=lambda ele: ele['date'], reverse=True)

    cwd = os.getcwd()

    outfile = '%s/bst_data/elections.csv' % cwd
    with open(outfile, 'w', newline='') as outf:
        wtr = csv.DictWriter(outf, fieldnames=elections[0].keys())
        wtr.writeheader()
        for election in elections:
            wtr.writerow(election)
            view.log('Imported ' + str(election))

    view.log('Done!')


def voters_to_csv(csv_writer):
    cnt = 0
    with open('michigan/sos_data/entire_state_v.lst', 'r', newline='') as lst_file:
        for line in lst_file:
            try:
                csv_writer.writerow(qvf_voter_to_dict(line))
                cnt += 1
                if cnt % 10000 == 0:
                    eprint(f'{cnt:,d}')
            except Exception as e:
                eprint("Error: %s: %s" % (line, str(e)))


def qvf_voter_to_dict(line):
    return {
        'last_name': line[0:35].replace('\\', '').strip(),
        'first_name': line[35:55].replace('\\', '').strip(),
        'middle_name': line[55:75].replace('\\', '').strip(),
        'name_suffix': line[75:78].replace('\\', '').strip(),
        'date_of_birth': None,
        'birth_year': line[78:82].replace('\\', '').strip(),
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
        'party': None
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
