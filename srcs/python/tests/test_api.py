import unittest
from python import api

class TestApi(unittest.TestCase):
	"""This class contains the unit tests for the API module."""
	
	def test_load_conf(self):
		"""this test is for the Config class method load"""
		conf = api.Config()
		conf.load()
		self.assertEqual(len(conf._params.keys()),2) # TODO: change the test

	def test_load_Error(self):
		"""this test is for the error in the Config class method load"""
		with self.assertRaises(Exception) as context:
			api.Config.load("data/testFail.txt")
			self.assertTrue('IOError' in context.exception)

	def test_get_Config(self):
		"""this test is for the Config class method get"""
		conf = api.Config()
		conf.load()
		expect_value = "0xffff" # TODO: change the test
		expect_default = "0xaaaa"
		extract = conf.get("test")
		self.assertEqual(extract.value, expect_value)
		self.assertEqual(extract.default, expect_default)

	def test_set_Error(self):
		"""this test is for the error in the Config class method set"""
		conf = api.Config()
		conf.load()
		with self.assertRaises(Exception) as context:
			conf.set("-", "-")
			self.assertTrue("KeyError"in context.exception)
		# TODO: change the test
