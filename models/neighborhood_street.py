class NeighborhoodStreet(object):

    def __init__(self, d):
        self.name = d['name']
        self.lo = d['lo']
        self.hi = d['hi']
        self.side = d['oe']
        self.house_nums = []

