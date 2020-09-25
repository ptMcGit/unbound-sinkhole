"""
Sqlite3 functions.

The sqlite3 functions like tuples so most of
the functions that modify the DB expect lists
of tuples of the form (<ip_addres>, <url>).

"""

import sqlite3
import pathlib

sql_db = "./unbound-sinkhole.db"
db_sinkhole_table = "list"

def _set_blacklist(blacklist):
    return ("TRUE" if blacklist else "FALSE")

def _generate_records(cursor):
    for r in cursor.fetchall():
        yield r

def init_db():
    """ Initialize the database,
    or return if db already exists """
    if pathlib.Path(sql_db).exists():
        return

    with sqlite3.connect(sql_db) as con:
        con.execute('''CREATE TABLE {0} (
        id INTEGER PRIMARY KEY,
        sinkhole BOOLEAN DEFAULT TRUE,
        ip_addr VARCHAR(64) NOT NULL,
        url VARCHAR(64) NOT NULL,
        UNIQUE(ip_addr, url))'''.format(db_sinkhole_table))

def update_records(records, blacklist=True):
    """ Update the db with records.

    Add or update an individual record or a list of records.

    Args:
        records: list of records to update
        blacklist: whether the records should be added to the blacklist

    Raises:
        Any error that is not sqlite3.IntegrityError.
    """

    blacklist = _set_blacklist(blacklist)
    with sqlite3.connect(sql_db) as con:
        for r in records:
            print((blacklist,) + r)
            try:
                con.execute('''INSERT INTO {0}
                (sinkhole, ip_addr, url) VALUES(?, ?, ?)'''.format(db_sinkhole_table, blacklist), (blacklist,) + r)
            except sqlite3.IntegrityError as e:
                con.execute('''UPDATE {0}
                SET sinkhole = "{1}"
                WHERE (ip_addr = "{2}" AND url = "{3}")'''.format(db_sinkhole_table, blacklist, r[0], r[1]))

def delete_records(records):
    """ Delete records provided from the DB.

    Args:
        records: list of records to delete.

    Raises:
        Any error that is not sqlite3.IntegrityError.
    """

    with sqlite3.connect(sql_db) as con:
        for r in records:
            con.execute('''DELETE FROM {0}
            WHERE (ip_addr = "{1}" AND url = "{2}")'''.format(db_sinkhole_table,
                                                         r[0],
                                                         r[1]))

def purge_db():
    """ Purge all the records from the db.
    """
    with sqlite3.connect(sql_db) as con:
        con.execute("DELETE FROM {0}".format(db_sinkhole_table))

def get_blacklist():
    """ Get all blacklist records.
    Returns:
        List containing all blacklist records.
    """
    with sqlite3.connect(sql_db) as con:
        cursor = con.execute('''SELECT ip_addr, url FROM {0}
        WHERE sinkhole = "TRUE"'''.format(db_sinkhole_table))
    return _generate_records(cursor)
