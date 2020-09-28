"""Test db module.
"""

import sqlite3
import unittest

import unbound_sinkhole.conf as conf
import unbound_sinkhole.db as db

conf.initialize_confs('unbound_sinkhole/tests/inputs/test_config')
db.SINKHOLE_DB = conf.SINKHOLE_DB

class TestDb(unittest.TestCase):
    """Test db module.
    """
    def setUp(self):
        """Initialize the database.
        """
        db.init_db()

    def tearDown(self):
        """Purge all records from the DB.
        """
        db.purge_db()

    def get_records(self):
        """ Helper method to get all records
        """
        with sqlite3.connect(conf.SINKHOLE_DB) as con:
            return con.execute("SELECT * FROM {0}".format(db.DB_SINKHOLE_TABLE)).fetchall()

    def test_update_records(self):
        """ Various checks for method for
        inserting records. """

        records1 = [("0.0.0.0", "yahoo.com.")]

        db.update_records(records1, blacklist=True)
        # insert duplicate
        db.update_records(records1, blacklist=True)

        recs = self.get_records()
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0][1], 'TRUE')

        # update sinkhole boolean
        db.update_records(records1, blacklist=False)

        recs = self.get_records()
        self.assertEqual(len(recs), 1)
        self.assertEqual(recs[0][1], 'FALSE')

        # attempt insert record with same ip, different host
        db.update_records([("0.0.0.0", "google.com.")]
                          , blacklist=False)

        recs = self.get_records()
        self.assertEqual(len(recs), 2)

        # record with different ip same host
        db.update_records([("1.1.1.1", "google.com.")],
                          blacklist=True)

        recs = self.get_records()
        self.assertEqual(len(recs), 3)

    def test_delete_records(self):
        """ Test deleting records.
        """
        a_rec = ("0.0.0.0", "a.com")
        b_rec = ("1.1.1.1", "b.com")
        c_rec = ("2.2.2.2", "c.com")

        db.update_records([a_rec,
                           b_rec,
                           c_rec],
                          blacklist=True)

        db.delete_records([a_rec, b_rec])
        recs = self.get_records()
        self.assertEqual(len(recs), 1)

        db.delete_records([c_rec])

        # delete twice
        db.delete_records([c_rec])
        recs = self.get_records()
        self.assertEqual(len(recs), 0)


    def test_get_blacklist(self):
        """ Test getting the blacklist.
        """
        a_rec = ("0.0.0.0", "a.com")
        b_rec = ("1.1.1.1", "b.com")
        db.update_records([a_rec,
                           b_rec],
                          blacklist=True)
        db.update_records([("2.2.2.2", "c.com")], blacklist=False)
        recs = list(db.get_blacklist())

        self.assertEqual(recs[0], a_rec)
        self.assertEqual(recs[1], b_rec)
        self.assertEqual(len(recs), 2)

if __name__ == '__main__':
    unittest.main()
