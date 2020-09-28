import unittest
import unbound_sinkhole.cli as cli


cli.main_config = 'unbound_sinkhole/tests/inputs/test_config'
test_file = 'unbound_sinkhole/tests/inputs/records_file_ok'

class TestCLI(unittest.TestCase):
#    def setUp(self):

    def test_reset(self):
        # test reset branch
        cli.main(['reset'])

    def test_modify_record(self):
        # test modify branch

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
        # test modify branch

        # test delete
        cli.main(['modify',
                  '--delete',
                  '--file',
                  test_file])

        # test whitelist
        cli.main(['modify',
                  '--blacklist',
                  '--file',
                  test_file])

        # test blacklist
        cli.main(['modify',
                  '--whitelist',
                  '--file',
                  test_file])

    def test_enable(self):
        cli.main(['enable'])

    def test_disable(self):
        cli.main(['enable'])



if __name__ == '__main__':
    unittest.main()
