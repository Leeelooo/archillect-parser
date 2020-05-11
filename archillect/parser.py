from bs4 import BeautifulSoup
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
        items_list.append((item_number, sources))

    return items_list


def get_last_items(items_count=10):
    soup = BeautifulSoup(requests.get(URL).content, 'lxml')
    last_id = int(soup.find('div', 'overlay').string.strip())

    return fetch_items(last_id, items_count)


# def main():
#     items_to_parse = get_arg_value(sys.argv[1:], 'items')
#     items = get_last_items(int(items_to_parse) if items_to_parse.isdigit() else 10)
#     for item in items:
#         print(item[0])
#         print('└───' + str(item[1]))


# if __name__ == '__main__':
#     main()
