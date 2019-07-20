from bs4 import BeautifulSoup
import requests

URL = 'http://archillect.com'


def items_fetching_recursive(item_id, take_first):
    if take_first > 0 and item_id > 0:
        item_url = URL + '/' + str(item_id)
        print(item_url)
        item_soup = BeautifulSoup(requests.get(item_url).content, 'lxml')
        sources = list(map(lambda x: x['href'], item_soup.find(id='sources').find_all('a')))
        sources[0] = sources[0][56:]
        print('\t' + str(sources))
        items_fetching_recursive(item_id - 1, take_first - 1)


soup = BeautifulSoup(requests.get(URL).content, 'lxml')
last_id = int(soup.find('div', 'overlay').string.strip())
items_fetching_recursive(int(last_id), 1)
