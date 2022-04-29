import dao


def import_sos_elections(path, prg_ctrl):
    dao.import_sos_elections(path, prg_ctrl)


def import_sos_voters(path, prg_ctrl):
    return dao.import_sos_voters(path, prg_ctrl)


def import_hx(path, prg_ctrl):
    dao.import_hx(path, prg_ctrl)
