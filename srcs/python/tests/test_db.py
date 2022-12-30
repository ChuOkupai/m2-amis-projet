import unittest
from python import db

class TestDb(unittest.TestCase):
	"""This class contains the unit tests for the DB module."""

	def test_1_equals_1(self):
		"""This test will always pass because 1 equals 1."""
		self.assertEqual(1, 1)
