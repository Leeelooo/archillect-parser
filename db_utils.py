"""
Sqlite3 database singleton helper

Example:

>>> import db_utils
>>> db.utils.connect_database(':memory:')
>>> db_utils.create_table('posts')
"""

import sqlite3
from typing import List

CONNECTION = None
CURSOR = None


def check_cursor(cursor: sqlite3.Cursor):
    if not cursor:
        raise ConnectionError('Сonnection to the database is not established')

    return True


def make_value_string(length: int):
    """Make string like '(?,?)' for use in sql queries"""
    return '(' + ','.join(['?']*length) + ')'


# TODO: check if all dangerous characters are escaped
def escape_string(string):
    """Escape string to prevent injection"""
    return string.replace('"', '""').replace("'", "''")


def connect_database(path: str):
    """
    Create database connection
    If file does not exists it will be created
    """
    global CONNECTION, CURSOR
    CONNECTION = sqlite3.connect(path)
    CURSOR = CONNECTION.cursor()


def check_table_existence(table_name: str):
    check_cursor(CURSOR)
    CURSOR.execute('''
        SELECT count(name) 
        FROM sqlite_master  
        WHERE type = 'table' 
        AND name = '{}' 
    '''.format(escape_string(table_name)))
    return CURSOR.fetchone()[0] == 1


def create_table(table_name: str):
    check_cursor(CURSOR)
    CURSOR.execute('''
        create table if not exists {}
        (id integer primary key, sources text not null)
    '''.format(escape_string(table_name)))


def delete_table(table_name: str):
    check_cursor(CURSOR)
    CURSOR.execute('''
        drop table if exists {}
    '''.format(escape_string(table_name)))


def insert(table_name: str, item_tuple: tuple):
    if not check_table_existence(table_name):
        create_table(table_name)
    CURSOR.execute('''
        insert into {} values (?, ?)
    '''.format(escape_string(table_name)), item_tuple)
    CONNECTION.commit()


def insert_many(table_name: str, items_list: List[tuple]):
    if not check_table_existence(table_name):
        create_table(table_name)
    CURSOR.executemany('''
        insert into {} values (?, ?)
    '''.format(escape_string(table_name)), items_list)
    CONNECTION.commit()


def delete(table_name: str, item_id: int):
    if not check_table_existence(table_name):
        return
    CURSOR.execute('''
        delete from {} where id = ?
    '''.format(escape_string(table_name)), (item_id,))
    CONNECTION.commit()


def delete_many(table_name: str, item_id_list: List[int]):
    if not check_table_existence(table_name):
        return
    CURSOR.executemany('''
        delete from {} where id = ?
    '''.format(escape_string(table_name)), list(map(lambda x: (x,), item_id_list)))
    CONNECTION.commit()


def update(table_name, item_id, new_sources):
    if not check_table_existence(table_name):
        return
    CURSOR.execute('''
        update {}
        set sources = ?
        where id = ?
    '''.format(escape_string(table_name)), (new_sources, item_id))
    CONNECTION.commit()


def update_many(table_name, item_id_list, new_sources_list):
    if not check_table_existence(table_name):
        return
    CURSOR.executemany('''
        update {}
        set sources = ?
        where id = ?
    '''.format(escape_string(table_name)), list(map(lambda x, y: (x, y), new_sources_list, item_id_list)))
    CONNECTION.commit()


def get_item(table_name: str, item_id: int):
    if not check_table_existence(table_name):
        return None
    CURSOR.execute('''
        select * from {} where id = ?
    '''.format(escape_string(table_name)), (item_id,))
    return CURSOR.fetchone()


def get_items(table_name: str, item_id_list: List[int]):
    if not check_table_existence(table_name):
        return None
    CURSOR.execute('''
        select * from {0} where id in({1})
    '''.format(table_name, ', '.join(list(map(str, item_id_list)))))
    return CURSOR.fetchall()


def disconnect_database():
    global CONNECTION, CURSOR
    CONNECTION.close()
    CONNECTION = None
    CURSOR = None


# if __name__ == '__main__':
    # A simple example
    # connect_database('mydatabase.db')
    #
    # values = [
    #     ('0', 'google.com'),
    #     ('1', 'vk.com'),
    #     ('2', 'facebook.com'),
    #     ('3', 'reddit.com')
    # ]
    # create_table('sources')
    # insert_many('sources', values)
    # print(get_item('sources', 0))
    # print(get_items('sources', (1, 2, 3)))
    #
    # disconnect_database()
