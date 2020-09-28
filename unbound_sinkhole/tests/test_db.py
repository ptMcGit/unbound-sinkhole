import unbound_sinkhole.conf as conf
import unbound_sinkhole.db as db
import sqlite3
import unittest

conf.initialize_confs('unbound_sinkhole/tests/inputs/test_config')
db.sinkhole_db = conf.sinkhole_db


class TestDb(unittest.TestCase):
    def setUp(self):
        db.init_db()

    def tearDown(self):
        db.purge_db()

    def get_records(self):
        ''' Helper method to get all records
        '''
        with sqlite3.connect(conf.sinkhole_db) as con:
            return con.execute("SELECT * FROM {0}".format(db.db_sinkhole_table)).fetchall()

    def test_update_records(self):
        ''' Various checks for method for
        inserting records. '''

        records1 = [("0.0.0.0", "yahoo.com.")]

        db.update_records(records1, blacklist=True)
        # insert duplicate
        db.update_records(records1, blacklist=True)

        r = self.get_records()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0][1], 'TRUE')

        # update sinkhole boolean
        db.update_records(records1, blacklist=False)

        r = self.get_records()
        self.assertEqual(len(r), 1)
        self.assertEqual(r[0][1], 'FALSE')

        # attempt insert record with same ip, different host
        db.update_records([("0.0.0.0", "google.com.")]
                          , blacklist=False)

        r = self.get_records()
        self.assertEqual(len(r), 2)

        # record with different ip same host
        db.update_records([("1.1.1.1", "google.com.")],
                          blacklist=True)

        r = self.get_records()
        self.assertEqual(len(r), 3)

    def test_delete_records(self):
        ''' Test deleting records.
        '''
        a = ("0.0.0.0", "a.com")
        b = ("1.1.1.1", "b.com")
        c = ("2.2.2.2", "c.com")

        db.update_records([a,
                           b,
                           c],
                          blacklist=True)

        db.delete_records([a, b])
        r = self.get_records()
        self.assertEqual(len(r), 1)

        db.delete_records([c])

        # delete twice
        db.delete_records([c])
        r = self.get_records()
        self.assertEqual(len(r), 0)


    def test_get_blacklist(self):
        ''' Test getting the blacklist.
        '''
        a = ("0.0.0.0", "a.com")
        b = ("1.1.1.1", "b.com")
        db.update_records([a,
                           b],
                          blacklist=True)
        db.update_records([("2.2.2.2", "c.com")], blacklist=False)
        r = list(db.get_blacklist())

        self.assertEqual(r[0], a)
        self.assertEqual(r[1], b)
        self.assertEqual(len(r), 2)

if __name__ == '__main__':
    unittest.main()
