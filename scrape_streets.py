from bs4 import BeautifulSoup as bs
import requests


def get_house_nums(parser):
    nums = []
    divs = parser.find_all('div', class_='b-homemetry-property street')
    for div in divs:
        house_num = div.get('id')
        if house_num:
            nums.append(house_num[1:])

    return nums


def scrape_initial_page(prefix, state, city, street):
    url = '%s/%s,+%s+%s' % (
        prefix,
        street.replace(' ', '+').upper(),
        city.replace(' ', '+').upper(),
        state
    )
    req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    parser = bs(req.text, 'html.parser')

    tbl = parser.find('section', class_='b-street-index').find('table')
    rows = tbl.find_all('tr')
    this_block = rows[1].find('td').get_text()
    links = [a['href'] for a in tbl.find_all('a', href=True)]

    house_nums = get_house_nums(parser)

    return this_block, links, house_nums


def scrape_links(prefix, links):
    house_nums = []
    for link in links:
        url = '%s/%s' % (prefix, link)
        req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        parser = bs(req.text, 'html.parser')
        house_nums += get_house_nums(parser)
    return house_nums


def main():

    city = 'Ann Arbor'
    state = 'MI'

    prefix = 'https://www.geographic.org/streetview/usa'
    state = state.lower()

    url = '%s/%s/%s.html' % (
        prefix, state, city.replace(' ', '_').lower()
    )
    req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    parser = bs(req.text, 'html.parser')

    span = parser.find('span', class_='listspan')
    ul = span.findChild('ul')
    li = ul.findChildren('li')

    streets = []
    for item in li:
        streets.append(item.findChild('a').get_text())

    with open('c:/bench/bst/data/%s/streets.txt' % state, 'w') as f:
        for street in streets:
            f.write(street + '\n')


if __name__ == '__main__':
    main()
