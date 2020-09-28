"""Test unbound module.
"""

import unittest

class TestUnbound(unittest.TestCase):
    """Test unbound moudle.
    """

    def test_insert_line(self):
        """Test insertion into unbound config.
        """
        # this gets covered by test_writer.test_modify_SERVER_CONFig()
        ...


if __name__ == '__main__':
    unittest.main()
