from bs4 import BeautifulSoup
from item_model import ArchillectItem
from db import session
import requests

URL = 'http://archillect.com'


def get_item_sources(item_url):
    item_soup = BeautifulSoup(requests.get(item_url).content, 'lxml')
    return list(map(lambda x: x['href'], item_soup.find(id='sources').find_all('a')))


def fetch_items(item_id, items_count):
    items_list = []

    for item_number in range(item_id, max(item_id - items_count, 1), -1):
        item_url = URL + '/' + str(item_number)
        sources = get_item_sources(item_url)
        sources[0] = sources[0][56:]
        items_list.append(ArchillectItem(item_number, sources))

    return items_list

def get_last_items(items_count=10):
    soup = BeautifulSoup(requests.get(URL).content, 'lxml')
    last_id = int(soup.find('div', 'overlay').string.strip())

    return fetch_items(last_id, items_count)


if __name__ == '__main__':
    # TODO: implement inserting properly?
    items = get_last_items()
    session.add_all(items)
    session.commit()
    for item in items:
        print(str(item.item_id) + ' ' + item.sources)
