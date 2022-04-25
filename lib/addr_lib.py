import usaddress
import re


def to_dict(s):
    return {t[1]: t[0] for t in usaddress.parse(s)}


def parse(s):
    d = to_dict(s)

    house_num = d['AddressNumber']
    occupancy_type = ''
    occupancy_id = ''
    if not house_num.isdigit():
        occupancy_type = 'APT'
        occupancy_id = re.findall(r"\D+", house_num)[0]
        house_num = re.findall(r"\d+", house_num)[0]

    sname = ''
    flds = [
        'StreetNamePreDirectional',
        'StreetName',
        'StreetNamePostType',
        'StreetNamePostDirectional'
    ]
    for fld in flds:
        if fld in d:
            sname += d[fld] + ' '
    sname = sname.strip()

    occupancy_type = d['OccupancyType'] \
        if 'OccupancyType' in d else occupancy_type
    occupancy_id = d['OccupancyIdentifier'] \
        if 'OccupancyIdentifier' in d else occupancy_id
    unit = '%s %s' % (occupancy_type, occupancy_id)

    return int(house_num), sname.strip(), unit.strip()


def reg_date_to_date(reg_date):
    s = str(reg_date)
    dm = s[-6:]
    d = dm[0:2]
    y = dm[2:]
    m = s[0:len(s) - 6]
    if len(m) == 1:
        m = '0' + m
    return '%s-%s-%s' % (y, m, d)

