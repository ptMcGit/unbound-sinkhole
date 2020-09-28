"""Test writer module.
"""

import re
import shutil
from subprocess import CalledProcessError
import unittest

import unbound_sinkhole.conf as conf
import unbound_sinkhole.db as db
import unbound_sinkhole.unbound as unbound
import unbound_sinkhole.writer as writer

conf.initialize_confs('unbound_sinkhole/tests/inputs/test_config')

SERVER_CONFIG = conf.SERVER_CONF
SERVER_CONFIG_ORIGINAL = 'unbound_sinkhole/tests/inputs/server_config_original'

class TestMyClass(unittest.TestCase):
    """Test writer module.
    """

    def setUp(self):
        """Initialize the database.
        """
        db.init_db()

    def tearDown(self):
        """Purge records from the database.
        """
        db.purge_db()

    def test_records_to_file(self):
        """Test writing of records to a file.
        """
        # create some records
        writer.sinkhole_file = "unbound_sinkhole/tests/outputs/test_sinkhole.conf"

        a_rec = ("0.0.0.0", "a.com")
        b_rec = ("1.1.1.1", "b.com")
        c_rec = ("2.2.2.2", "c.com")

        db.update_records([a_rec,
                           b_rec],
                          True)
        db.update_records([c_rec],
                          False)

        writer.records_to_file()

        blacklist = db.get_blacklist()

        # check that only blacklisted IPs are added
        with open(writer.sinkhole_file) as sfh:
            line = sfh.readline()
            self.assertEqual(line.rstrip(),
                             writer.TEMPLATE.format(next(blacklist).url))

            line = sfh.readline()
            self.assertEqual(line.rstrip(),
                             writer.TEMPLATE.format(next(blacklist).url))

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
        with open(SERVER_CONFIG, "r") as sch, open(SERVER_CONFIG_ORIGINAL, "r") as soh:
            line_a = sch.readline()
            line_b = soh.readline()
            result = False
            while line_a == line_b and line_a != '':
                line_a = sch.readline()
                line_b = soh.readline()

            # leading whitespace is determined at the time of insertion
            if (not matches_original and
                re.match(r'^(\s*)'
                         + writer.INCLUDE_STATEMENT.rstrip().format(conf.SINKHOLE_CONF)
                         + '[\n]'
                         + '$', line_a)):
                result = True
                line_a = sch.readline()
            while line_a == line_b  and line_a != '':
                line_a = sch.readline()
                line_b = soh.readline()

            if line_a != line_b:
                raise Exception('problem comparing files')
            return result

    def test_modify_server_config(self):
        """Test modification of the Unbound server config.
        """
        shutil.copy(SERVER_CONFIG_ORIGINAL, SERVER_CONFIG)
        writer.sinkhole_file = 'sinkhole.conf'

        with open(writer.sinkhole_file, "w") as sfh:
            sfh.write('# dummy sinkhole file')

        # check that the test server config is ok
        try:
            unbound.test_server_config(SERVER_CONFIG)
        except CalledProcessError:
            self.fail()

        # enable
        writer.update_server_config(SERVER_CONFIG, enable=True)
        self.assertTrue(self.check_config(matches_original=False))
        # enable twice
        writer.update_server_config(SERVER_CONFIG, enable=True)
        self.assertTrue(self.check_config(matches_original=False))
        # disable
        writer.update_server_config(SERVER_CONFIG, enable=False)
        self.assertFalse(self.check_config(matches_original=True))
        # disable twice
        writer.update_server_config(SERVER_CONFIG, enable=False)
        self.assertFalse(self.check_config(matches_original=True))


if __name__ == '__main__':
    unittest.main()
