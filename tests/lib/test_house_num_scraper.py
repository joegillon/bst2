import unittest
import lib.house_num_scraper as scraper


class TestHouseNumScraper(unittest.TestCase):

    def test_scrape_house_nums(self):
        state = 'MI'
        city = 'Ann Arbor'
        # street = 'Bruce St'
        # nums = scraper.scrape_house_nums(state, city, street)

        street = 'Miller Ave'
        nums = scraper.scrape_house_nums(state, city, street)
        pass
