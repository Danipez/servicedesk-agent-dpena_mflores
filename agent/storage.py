import sqlite3
from contextlib import contextmanager
from config import settings

@contextmanager
def conectar():
    conn = sqlite3.connect(settings.DB_PATH, timeout=20)
    conn.row_factory = sqlite3.Row
    try:
        with conn:
            yield conn
    finally:
        conn.close()
