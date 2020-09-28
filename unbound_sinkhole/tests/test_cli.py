import unittest
import unbound_sinkhole.cli as cli


cli.main_config = 'unbound_sinkhole/tests/inputs/test_config'

class TestCLI(unittest.TestCase):
#    def setUp(self):

    def test_reset(self):
        # test reset branch
        cli.main(['reset'])

    def test_modify(self):
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

    def test_enable(self):
        cli.main(['enable'])

    def test_disable(self):
        cli.main(['enable'])



if __name__ == '__main__':
    unittest.main()
