import sqlite3

conn = sqlite3.connect(':memory:')

def is_items_table_created(curs):
    curs.execute(''' SELECT count(name) 
                     FROM sqlite_master  
                     WHERE type='table' 
                           AND name='table_items' ''')
    return curs.fetchone()[0] == 1


def create_items_table(curs):
    curs.execute(''' CREATE TABLE table_items
                     (item_id integer PRIMARY KEY, 
                      sources text NOT NULL)''')


def insert_new_items(items):
    curs = conn.cursor()
    if not is_items_table_created(curs):
        create_items_table(curs)
    curs.executemany(''' INSERT 
                         INTO table_items(item_id,sources) 
                         VALUES (?, ?)''', items)
    conn.commit()


def get_cached_items():
    curs = conn.cursor()
    cached = {}
    if is_items_table_created(curs):
        for row in curs.execute(''' SELECT * FROM table_items'''):
            print(row)
            cached[row[0]] = row[1]
    conn.close()
    return cached
