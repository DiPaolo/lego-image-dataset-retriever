import sqlite3
from typing import List

from entities.part import Part
from entities.part_category import PartCategory
from entities.part_image import PartImage


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

    # parts categories
    _create_table(conn, 'part_categories', [
        'id integer PRIMARY KEY',
        'name text NOT NULL',
        'rba_part_cat_id text',
        'part_count integer'
    ])

    # parts
    _create_table(conn, 'parts', [
        'id integer PRIMARY KEY',
        'name text NOT NULL',
        'rba_part_num text NOT NULL',
        'rba_part_cat_id text',
        'rba_part_url text NOT NULL',
        'FOREIGN KEY(rba_part_cat_id) REFERENCES part_categories(id)'
    ])

    # parts images
    _create_table(conn, 'part_images', [
        'id integer PRIMARY KEY',
        'part_id integer NOT NULL',
        'width integer',
        'height integer',
        'rba_part_img_url text NOT NULL',
        'downloaded_filename text',
        'is_downloaded BIT NOT NULL',
        'FOREIGN KEY(part_id) REFERENCES parts(id)'
    ])

    _close_connection(conn)


def add_part_categories(part_categories: List[PartCategory]):
    conn = _create_connection()
    cur = conn.cursor()

    for part_cat in part_categories:
        sql = f'''INSERT INTO part_categories(name, rba_part_cat_id, part_count)
                  VALUES({part_cat.name()}, {part_cat.id()}, {part_cat.part_count()})'''
        try:
            cur.execute(sql, cur)
        except sqlite3.Error as e:
            print(f'ERROR Failed to add part category {part_cat.name()} ({part_cat.id()}) to database. {e}')

    conn.commit()
    _close_connection(conn)

    return cur.lastrowid


def add_part(part: Part):
    conn = _create_connection()
    cur = conn.cursor()

    sql = f'''INSERT INTO parts(name, rba_part_num, rba_part_cat_id, rba_part_url)
              VALUES(?, ?, ?, ?)'''

    try:
        cur.execute(sql, [part.name(), part.part_num(), part.part_cat_id(), part.part_url()])
    except sqlite3.Error as e:
        print(f'ERROR Failed to add part {part.name()} ({part.part_num()}) to database. {e}')

    conn.commit()
    _close_connection(conn)

    return cur.lastrowid


def add_part_image(part_id: int, part_image: PartImage):
    conn = _create_connection()
    cur = conn.cursor()

    sql = f'''INSERT INTO part_images(part_id, width, height, rba_part_img_url, downloaded_filename, is_downloaded)
              VALUES(?, ?, ?, ?, ?, ?)'''
    try:
        cur.execute(sql, [part_id, part_image.width(), part_image.height(), part_image.image_url(),
                          part_image.downloaded_filename(), part_image.is_downloaded()])
    except sqlite3.Error as e:
        print(
            f'ERROR Failed to add image for part with ID {part_id} (image URL {part_image.image_url()}) to database. {e}')

    conn.commit()
    _close_connection(conn)

    return cur.lastrowid


def fetch_resolutions(part_cat_id: int):
    conn = _create_connection()
    cur = conn.cursor()

    sql = f'''
        SELECT width, height
        FROM part_images
        INNER JOIN parts
        ON part_images.part_id = parts.id
        WHERE parts.rba_part_cat_id == {part_cat_id}'''

    res_stats = dict()
    for res in cur.execute(sql):
        key = (res[0], res[1])
        if key in res_stats:
            res_stats[key] += 1
        else:
            res_stats[key] = 1

    _close_connection(conn)

    return res_stats


def fetch_categories():
    conn = _create_connection()
    cur = conn.cursor()

    sql = f'''
        SELECT parts.rba_part_cat_id, COUNT(parts.rba_part_cat_id)
        FROM part_images
        INNER JOIN parts
        ON part_images.part_id = parts.id
        GROUP BY parts.rba_part_cat_id
        ORDER BY COUNT(parts.rba_part_cat_id) DESC'''

    res_stats = dict()
    for res in cur.execute(sql):
        key = res[0]
        if key in res_stats:
            res_stats[key] += res[1]
        else:
            res_stats[key] = res[1]

    _close_connection(conn)

    return res_stats
