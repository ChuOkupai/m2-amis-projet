"""Tests for the API module"""

import unittest
from api import sample

class TestApi(unittest.TestCase):
    """
    This class contains the unit tests for the API module
    """

    def test_get_1(self):
        """
        Test the get_1 function
        """
        self.assertEqual(sample.get_1(), 1, "get_1 should return 1")
