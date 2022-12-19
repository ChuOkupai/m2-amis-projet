"""Tests for the Data Mining module"""

import unittest
from datamining import sample

class TestDataMining(unittest.TestCase):
    """
    This class contains the unit tests for the Data Mining module
    """

    def test_get_1(self):
        """
        Test the get_1 function
        """
        self.assertEqual(sample.get_1(), 1, "get_1 should return 1")
