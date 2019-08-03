import argparse
from archillect.parser import get_last_items

parser = argparse.ArgumentParser(description='Parse Archillect posts')

parser.add_argument('-l', '--last', type=int, default=1)

if __name__ == "__main__":
    args = parser.parse_args()

    items = get_last_items(args.last)
    for item in items:
        for item in items:
        print(item[0])
        print('└───' + str(item[1]))
