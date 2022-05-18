class NeighborhoodStreet(object):

    def __init__(self, d):
        self.name = d['name']
        self.lo = d['lo'] if 'lo' in d else ''
        self.hi = d['hi'] if 'hi' in d else ''
        self.side = d['side'] if 'side' in d else 'B'
        self.house_nums = []
        if 'house_nums' in d:
            if isinstance(d['house_nums'], str):
                d['house_nums'] = d['house_nums'].split('|')
            self.house_nums = d['house_nums']

    @staticmethod
    def reconfig_street(street):
        nums = street.house_nums

        lo_idx = nums.index(street.lo)
        hi_idx = nums.index(street.hi)

        nums = nums[lo_idx:hi_idx+1]

        if street.side != 'B':
            nums = map(int, nums)
            if street.side == 'E':
                nums = [n for n in nums if n % 2 == 0]
            else:
                nums = [n for n in nums if n % 2 != 0]
            nums = list(map(str, nums))

        street.house_nums = nums
