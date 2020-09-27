import unbound_sinkhole.parsing as parsing

from pathlib import Path
import unittest

class TestParsing(unittest.TestCase):

    def setUp(self):
        return

    def tearDown(self):
        return

    def test_record_check(self):
        # good ipv4 record
        r = "0.0.0.0 www.example.com"
        self.assertIsNotNone(parsing.record_check(r))

        # bad ipv4 record
        r = "0.0.0 www.example.com"
        self.assertIsNone(parsing.record_check(r))

        # bad ipv6 record
        r = "::: www.example.com"
        self.assertIsNone(parsing.record_check(r))

        # bad hostnames
        r = "0.0.0.0 www._.com"
        self.assertIsNone(parsing.record_check(r))
        r = "0.0.0.0 www._.com/home"
        self.assertIsNone(parsing.record_check(r))
        r = "0.0.0.0 www._.com/home/?s=5"
        self.assertIsNone(parsing.record_check(r))

    def test_process_files(self):
        # check ok files
        l = list(parsing.process_files(['unbound_sinkhole/tests/inputs/records_file_ok',
                                   'unbound_sinkhole/tests/inputs/records_file_ok2']))

        self.assertEqual([('0.0.0.0', 'bad-site.com'),
                          ('181.16.9.1', 'www.evil-site.com'),
                          ('5666::1112', 'www.scary-site.co.us'),
                          ('0.0.0.0', 'ok-site.com')],
                         l)

        # check file that doesn't exist
        non_file = "unbound_sinkhole/tests/inputs/nonexistent_file"
        self.assertFalse(Path(non_file).exists())

        with self.assertRaises(Exception):
            parsing.process_files(non_file)

        # check file with bad records
        bad_records_file = 'unbound_sinkhole/tests/inputs/records_file_bad'
        with self.assertRaises(Exception):
            parsing.process_files(bad_records__file)


if __name__ == '__main__':
    unittest.main()
