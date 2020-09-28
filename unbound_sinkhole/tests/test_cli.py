"""cli module tests.
"""

import unittest

import unbound_sinkhole.cli as cli

cli.MAIN_CONFIG = 'unbound_sinkhole/tests/inputs/test_config'
TEST_FILE = 'unbound_sinkhole/tests/inputs/records_file_ok'

class TestCLI(unittest.TestCase):
    """cli module tests.
    """
    def test_reset(self):
        """Test reset branch.
        """
        cli.main(['reset'])

    def test_modify_record(self):
        """Test modify branch with cmdline records.
        """

        # test delete
        cli.main(['modify',
                  '--delete',
                  '0.0.0.0',
                  'badsite.com'])

        # test whitelist
        cli.main(['modify',
                  '--blacklist',
                  '0.0.0.0',
                  'badsite.com'])


        # test blacklist
        cli.main(['modify',
                  '--whitelist',
                  '0.0.0.0',
                  'badsite.com'])

    def test_modify_records(self):
        """Test modify branch with files.
        """

        # test delete
        cli.main(['modify',
                  '--delete',
                  '--file',
                  TEST_FILE])

        # test whitelist
        cli.main(['modify',
                  '--blacklist',
                  '--file',
                  TEST_FILE])

        # test blacklist
        cli.main(['modify',
                  '--whitelist',
                  '--file',
                  TEST_FILE])

    def test_enable(self):
        """Test enable branch.
        """
        cli.main(['enable'])

    def test_disable(self):
        """Test disable branch.
        """
        cli.main(['enable'])


if __name__ == '__main__':
    unittest.main()
