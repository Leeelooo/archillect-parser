from bs4 import BeautifulSoup
import requests
import json
import db_utils

URL = 'http://archillect.com'


def get_item_sources(item_url):
    item_soup = BeautifulSoup(requests.get(item_url).content, 'lxml')
    return list(map(lambda x: x['href'], item_soup.find(id='sources').find_all('a')))


def fetch_items(item_id, items_count=10):
    items_list = []

    for item_number in range(item_id, max(item_id - items_count, 1), -1):
        item_url = URL + '/' + str(item_number)
        sources = get_item_sources(item_url)
        sources[0] = sources[0][56:]
        items_list.append((item_number, json.dumps(sources)))

    return items_list


if __name__ == '__main__':
    soup = BeautifulSoup(requests.get(URL).content, 'lxml')
    last_id = int(soup.find('div', 'overlay').string.strip())

    db_utils.connect_database('archillect_images.db')
    db_utils.create_table('sources')
    db_utils.insert_many('sources', fetch_items(int(last_id), 10))

    items = db_utils.get_items('sources', tuple(range(last_id, last_id-10, -1)))
    for item_id, item_sources in items:
        print(item_id, ': ', item_sources, sep='')
