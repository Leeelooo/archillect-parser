from bs4 import BeautifulSoup
import requests

URL = 'http://archillect.com'


def get_item_sources(item_url):
    item_soup = BeautifulSoup(requests.get(item_url).content, 'lxml')
    return list(map(lambda x: x['href'], item_soup.find(id='sources').find_all('a')))


# TODO: smth
# how it should works but it isn't
# item_tags_soup = BeautifulSoup(requests.get(search_url).content, 'lxml')
# return item_tags_soup.find('input', 'gLFyf gsfi').value
def get_tem_tags(search_url):
    return search_url


# TODO: do not print anything, just return a dict, NON RECURSIVE
def fetch_items_recursive(item_id, take_first):
    if take_first > 0 and item_id > 0:
        item_url = URL + '/' + str(item_id)
        print(item_url)
        sources = get_item_sources(item_url)
        tags = get_tem_tags(sources[0])
        sources[0] = sources[0][56:]
        print('├───' + str(sources))
        print('└─── ' + str(tags))
        fetch_items_recursive(item_id - 1, take_first - 1)


if __name__ == '__main__':
    soup = BeautifulSoup(requests.get(URL).content, 'lxml')
    last_id = int(soup.find('div', 'overlay').string.strip())
    fetch_items_recursive(int(last_id), 10)
