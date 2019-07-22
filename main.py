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
# done
def fetch_items(item_id, items_count):
    items_dict = {}

    for item_number in range(item_id, max(item_id-items_count, 1), -1):
        item_url = URL + '/' + str(item_number)
        sources = get_item_sources(item_url)
        tags = get_tem_tags(sources[0])
        sources[0] = sources[0][56:]
        items_dict[item_url] = [sources, tags]

    return items_dict


if __name__ == '__main__':
    soup = BeautifulSoup(requests.get(URL).content, 'lxml')
    last_id = int(soup.find('div', 'overlay').string.strip())
    items = fetch_items(int(last_id), 10)

    for url in items:
        print(url)
        print('├───' + str(items[url][0]))
        print('└─── ' + str(items[url][1]))
