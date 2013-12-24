from contextlib import contextmanager

import mysql.connector


@contextmanager
def connect(*args, **kwargs):
    try:
        cnx = mysql.connector.connect(*args, **kwargs)
        cur = cnx.cursor()
        yield cur
        cnx.commit()
    finally:
        cur.close()
        cnx.close()
