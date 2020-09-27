from subprocess import CalledProcessError
import unbound_sinkhole.db as db
import os
import re
import shutil
import unbound_sinkhole.tests.test_db as test_db
import unbound_sinkhole.unbound as unbound
import unittest
import unbound_sinkhole.writer as writer

server_config = 'unbound_sinkhole/tests/outputs/server_config'
server_config_original = 'unbound_sinkhole/tests/inputs/server_config_original'

class TestMyClass(unittest.TestCase):

    def setUp(self):
        # do before each test
        db.sql_db = test_db.test_db
        db.init_db()

    def tearDown(self):
        db.purge_db()

    def test_records_to_file(self):
        # create some records
        writer.sinkhole_file = "unbound_sinkhole/tests/outputs/test_sinkhole.conf"

        a = ("0.0.0.0", "a.com")
        b = ("1.1.1.1", "b.com")
        c = ("2.2.2.2", "c.com")

        db.update_records([a,
                           b],
                          True)
        db.update_records([c],
                          False)

        writer.records_to_file()

        blacklist = db.get_blacklist()

        # check that only blacklisted IPs are added
        with open(writer.sinkhole_file) as f:
            line = f.readline()
            self.assertEqual(line.rstrip(),
                             writer.template.format(next(blacklist).url))

            line = f.readline()
            self.assertEqual(line.rstrip(),
                             writer.template.format(next(blacklist).url))

            with self.assertRaises(StopIteration):
                next(blacklist)

    def check_config(self, matches_original=True):
        """Compare the new config with the original.

        Compare the new config generated with the original.
        The two configs should differ by a single line

        args:
            matches_original: whether the new file should match the original

        raises:
            Exception raised when the two files differ beyond the single line
        """
        with open(server_config, "r") as sc, open(server_config_original, "r") as so:
            lineA = sc.readline()
            lineB = so.readline()
            result = False
            while lineA == lineB and lineA != '':
                lineA = sc.readline()
                lineB = so.readline()
            # leading whitespace is determined at the time of insertion
            if matches_original and re.match('^(\s*)' +
                        writer.include_statement.rstrip() + '[\n]'
                        + '$', lineA):
                result = True
                lineA = sc.readline()
            while lineA == lineB  and lineA != '':
                lineA = sc.readline()
                lineB = so.readline()

            if lineA != lineB:
                raise Exception('problem comparing files')
            return result


    def test_modify_server_config(self):
        shutil.copy(server_config_original, server_config)
        writer.sinkhole_file = 'sinkhole.conf'

        with open(writer.sinkhole_file, "w") as sf:
            sf.write('# dummy sinkhole file')

        # check that the test server config is ok
        try:
            unbound.test_server_config(server_config)
        except CalledProcessError as e:
            self.fail()

        # enable
        writer.update_server_config(server_config, enable=True)
        self.assertTrue(self.check_config())
        # enable twice
        writer.update_server_config(server_config, enable=True)
        self.assertTrue(self.check_config())
        # disable
        writer.update_server_config(server_config, enable=False)
        self.assertFalse(self.check_config(matches_original=False))
        # disable twice
        writer.update_server_config(server_config, enable=False)
        self.assertFalse(self.check_config(matches_original=False))


if __name__ == '__main__':
    unittest.main()
