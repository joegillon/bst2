import csv
import globals as gbl
from models.voter import Voter


def save_list(objs, file):
    flds = list(objs[0].__dict__.keys())
    wtr = csv.DictWriter(file, fieldnames=flds)
    wtr.writeheader()
    for obj in objs:
        wtr.writerow(obj.__dict__)


def load_file(file):
    objs = []
    rdr = csv.DictReader(file)
    for row in rdr:
        objs.append(Voter(row))

    return objs


def get_voters_by_residence():
    return gbl.dataset.res_rex
