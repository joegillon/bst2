import dao


def import_sos_elections(path):
    dao.import_sos_elections(path)


def import_sos_voters(path):
    return dao.import_sos_voters(path)


def import_hx(path):
    dao.import_hx(path)
