from archillect_parser import get_last_items
from utils import get_arg_value
from requests import put
import json
import sys


def main():
    items_to_parse = get_arg_value(sys.argv[1:], 'items')
    items = get_last_items(int(items_to_parse) if items_to_parse.isdigit() else 10)
    for item in items:
        response = put('http://localhost:5000/items/',
                          data={'item_id': item[0], 'sources': json.dumps(item[1])})
        print(response.json())


if __name__ == '__main__':
    main()
