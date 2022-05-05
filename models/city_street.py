class CityStreet(object):

    def __init__(self, d):
        self.name = d['name']
        self.house_nums = list(map(int, d['house_nums'].split('|'))) \
            if d['house_nums'] else []
