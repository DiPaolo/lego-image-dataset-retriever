import sqlite3
from typing import List

from entities.part import Part


def _create_connection():
    conn = None
    try:
        conn = sqlite3.connect('lidr.db')
    except sqlite3.Error as e:
        print(f'ERROR Failed to connect database. {e}')

    return conn


def _close_connection(conn):
    conn.close()


def _create_table(conn, table_name, columns: List[str]):
    try:
        c = conn.cursor()
        c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});''')
    except sqlite3.Error as e:
        print(f'ERROR Failed to create table. {e}')


def init():
    conn = _create_connection()

    # parts
    _create_table(conn, 'parts', [
        'id integer PRIMARY KEY',
        'name text NOT NULL',
        'part_num text NOT NULL',
        'part_cat_id text',
        'part_url text NOT NULL',
        'width integer',
        'height integer'
    ])

    # parts images
    _create_table(conn, 'parts_images', [
        'id integer PRIMARY KEY',
        'part_id integer NOT NULL',
        'part_img_url text NOT NULL',
        'is_downloaded BIT NOT NULL',
        'FOREIGN KEY(part_id) REFERENCES parts(id)'
    ])

    _close_connection(conn)


def add_parts(parts: List[Part]):
    conn = _create_connection()
    cur = conn.cursor()

    for part in parts:
        sql = f'''INSERT INTO parts(name, part_num, part_cat_id, part_url)
                  VALUES({part.name()}, {part.part_num()}, {part.part_cat_id()}, {part.part_url()})'''
        try:
            cur.execute(sql, conn)
        except sqlite3.Error as e:
            print(f'ERROR Failed to add part {part.name()} ({part.part_num()}) to database. {e}')


    conn.commit()
    _close_connection(conn)

    return cur.lastrowid
