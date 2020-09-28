"""Sqlite3 functions.

Functions for interacting with the database.
The sqlite3 functions like tuples so most of
the functions that modify the DB expect lists
of tuples of the form (<ip_addres>, <url>).
"""

from collections import namedtuple
from pathlib import Path
import sqlite3

import unbound_sinkhole.conf as conf

DB_SINKHOLE_TABLE = "list"

Record = namedtuple('Record', 'address url')

def _db_sanity_checks():
    """Sanity checks for the db.

    - Does the DB exist?
    - Is the DB setup?

    Returns: True if DB checks out, False otherwise.
    """
    msg = 'the DB does not exist or is not setup'

    if not Path(conf.SINKHOLE_DB).exists():
        raise Exception(msg)

    with sqlite3.connect(conf.SINKHOLE_DB) as con:
        query = con.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        if DB_SINKHOLE_TABLE not in [t[0] for t in query.fetchall()]:
            raise Exception(msg)

def _set_blacklist(blacklist):
    return "TRUE" if blacklist else "FALSE"

def _generate_records(cursor):
    for record in cursor.fetchall():
        yield Record(*list(record))

def init_db():
    """ Initialize the database,
    or return if db already exists """

    if Path(conf.SINKHOLE_DB).exists():
        return


    with sqlite3.connect(conf.SINKHOLE_DB) as con:
        con.execute('''CREATE TABLE {0} (
        id INTEGER PRIMARY KEY,
        sinkhole BOOLEAN DEFAULT TRUE,
        ip_addr VARCHAR(64) NOT NULL,
        url VARCHAR(64) NOT NULL,
        UNIQUE(ip_addr, url))'''.format(DB_SINKHOLE_TABLE))

def update_records(records, blacklist=True):
    """ Update the db with records.

    Add or update an individual record or a list of records.

    Args:
        records: list of records to update
        blacklist: whether the records should be added to the blacklist

    Raises:
        Any error that is not sqlite3.IntegrityError.
    """

    _db_sanity_checks()

    blacklist = _set_blacklist(blacklist)
    with sqlite3.connect(conf.SINKHOLE_DB) as con:
        for record in records:
            try:
                con.execute('''INSERT INTO {0}
                (sinkhole, ip_addr, url)
                VALUES(?, ?, ?)'''.format(DB_SINKHOLE_TABLE),
                            (blacklist,) + record)
            except sqlite3.IntegrityError:
                con.execute('''UPDATE {0}
                SET sinkhole = "{1}"
                WHERE (ip_addr = "{2}"
                AND url = "{3}")'''.format(DB_SINKHOLE_TABLE,
                                           blacklist,
                                           record[0],
                                           record[1]))

def delete_records(records):
    """ Delete records provided from the DB.

    Args:
        records: list of records to delete.

    Raises:
        Any error that is not sqlite3.IntegrityError.
    """

    _db_sanity_checks()

    with sqlite3.connect(conf.SINKHOLE_DB) as con:
        for record in records:
            con.execute('''DELETE FROM {0}
            WHERE (ip_addr = "{1}" AND url = "{2}")'''.format(DB_SINKHOLE_TABLE,
                                                         record[0],
                                                         record[1]))
    return True

def purge_db():
    """ Purge all the records from the db.
    """
    try:
        _db_sanity_checks()
    except RuntimeError:
        init_db()
        return False

    with sqlite3.connect(conf.SINKHOLE_DB) as con:
        con.execute("DELETE FROM {0}".format(DB_SINKHOLE_TABLE))

    return True

def get_blacklist():
    """ Get all blacklist records.
    Returns:
        List containing all blacklist records.
    """
    with sqlite3.connect(conf.SINKHOLE_DB) as con:
        cursor = con.execute('''SELECT ip_addr, url FROM {0}
        WHERE sinkhole = "TRUE"'''.format(DB_SINKHOLE_TABLE))
    return _generate_records(cursor)
