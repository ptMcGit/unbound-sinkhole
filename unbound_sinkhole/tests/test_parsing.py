"""Test parsing module.
"""

from pathlib import Path
import unittest

import unbound_sinkhole.parsing as parsing

class TestParsing(unittest.TestCase):
    """Test parsing module.
    """
    def test_record_check(self):
        """Check parsing of records.
        """
        # good ipv4 record
        rec = "0.0.0.0 www.example.com"
        self.assertIsNotNone(parsing.record_check(rec))

        # bad ipv4 record
        rec = "0.0.0 www.example.com"
        self.assertIsNone(parsing.record_check(rec))

        # bad ipv6 record
        rec = "::: www.example.com"
        self.assertIsNone(parsing.record_check(rec))

        # bad hostnames
        rec = "0.0.0.0 www._.com"
        self.assertIsNone(parsing.record_check(rec))
        rec = "0.0.0.0 www._.com/home"
        self.assertIsNone(parsing.record_check(rec))
        rec = "0.0.0.0 www._.com/home/?s=5"
        self.assertIsNone(parsing.record_check(rec))

    def test_process_files(self):
        """Check processing of files.
        """
        # check ok files
        recs = list(parsing.process_files(['unbound_sinkhole/tests/inputs/records_file_ok',
                                   'unbound_sinkhole/tests/inputs/records_file_ok2']))

        self.assertEqual([('0.0.0.0', 'bad-site.com'),
                          ('181.16.9.1', 'www.evil-site.com'),
                          ('5666::1112', 'www.scary-site.co.us'),
                          ('0.0.0.0', 'ok-site.com')],
                         recs)

        # check file that doesn't exist
        non_file = "unbound_sinkhole/tests/inputs/nonexistent_file"
        self.assertFalse(Path(non_file).exists())

        with self.assertRaises(Exception):
            parsing.process_files(non_file)

        # check file with bad records
        bad_records_file = 'unbound_sinkhole/tests/inputs/records_file_bad'
        with self.assertRaises(Exception):
            parsing.process_files(bad_records_file)


if __name__ == '__main__':
    unittest.main()
