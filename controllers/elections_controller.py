import globals as gbl


def get_state_elections():
    return gbl.dataset.state_elections


def get_my_elections():
    return gbl.dataset.my_elections


def save(elections):
    if is_my_elections(elections):
        return
    gbl.dataset.save_my_elections(elections)


def is_my_elections(oth_elections):
    my_keys = set([election.id for election in glb.dataset.my_elections])
    oth_keys = set([election.id for election in oth_elections])
    return my_keys - oth_keys == []
