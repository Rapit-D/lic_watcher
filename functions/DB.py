import sqlite3
import os.path
from datetime import date, time


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'licenses.db')


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn = sqlite3.connect(DB_PATH)
conn.row_factory = dict_factory
session = conn.cursor()
