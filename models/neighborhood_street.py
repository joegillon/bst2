class NeighborhoodStreet(object):

    def __init__(self, d):
        self.name = d['name']
        self.lo = d['lo'] if 'lo' in d else ''
        self.hi = d['hi'] if 'hi' in d else ''
        self.side = d['side'] if 'side' in d else 'B'
