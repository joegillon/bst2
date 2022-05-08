from bs4 import BeautifulSoup as bs
import requests


prefix = 'https://homemetry.com'


def scrape_house_nums(state, city, street):
    url = '%s/%s,+%s+%s' % (
        prefix,
        street.replace(' ', '+').upper(),
        city.replace(' ', '+').upper(),
        state.upper()
    )
    page = get_page(url)
    nums, links = scrape_page(page)
    nums += scrape_links(links)

    return nums


def get_page(url):
    print('Scraping %s...' % url)
    req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    return bs(req.text, 'html.parser')


def scrape_page(page):
    return get_house_nums(page), get_page_links(page)


def get_house_nums(page):
    nums = []
    divs = page.find_all('div', class_='b-homemetry-property street')
    for div in divs:
        house_num = div.get('id')
        if house_num:
            nums.append(house_num[1:])

    return nums


def get_page_links(page):
    tbl = page.find('section', class_='b-street-index').find('table')
    rows = tbl.find_all('tr')[1:]
    last_row = rows[-1]
    col = last_row.find('td')
    if col.find('a'):
        idx = 0
        for row in rows:
            if not row.find('td').find('a'):
                break
            idx += 1
        return [a['href'] for a in tbl.find_all('a', href=True)][idx:]
    return []


def scrape_links(links):
    my_nums = []
    for link in links[0:-1]:
        url = '%s/%s' % (prefix, link)
        page = get_page(url)
        my_nums += get_house_nums(page)

    url = '%s/%s' % (prefix, links[-1])
    page = get_page(url)
    last_nums, links = scrape_page(page)

    my_nums += last_nums

    if links:
        my_nums += scrape_links(links)
    else:
        pass

    return my_nums
