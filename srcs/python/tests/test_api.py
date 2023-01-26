import unittest
from os import listdir, remove
from os.path import isdir, isfile, join

from python import api
from python.common import constants
from python.datamining import ChebiArchive as ChA


class TestApi(unittest.TestCase):
	"""This class contains the unit tests for the API module."""
	
	def test_load_conf(self):
		"""this test is for the Config class method load"""
		conf = api.Config()
		conf.load()
		self.assertGreater(len(conf._params.keys()),0)

	def test_load_Error(self):
		"""this test is for the error in the Config class method load"""
		with self.assertRaises(IOError):
			api.Config.load("data/testFail.txt")

	def test_get_Config(self):
		"""this test is for the Config class method get"""
		conf = api.Config()
		conf.load()
		expect_default = "0xaaaa"
		extract = conf.get("test")
		self.assertEqual(extract.default, expect_default)

	def test_set_Error(self):
		"""this test is for the error in the Config class method set"""
		conf = api.Config()
		conf.load()
		with self.assertRaises(KeyError):
			conf.set("-", "-")
		with self.assertRaises(TypeError):
			conf.set("test", 3)

	def test_save_Config(self):
		"""this test is for the Config class method save"""
		conf = api.Config()
		conf.load()
		expect_value = "0xffff"
		changed_value = "0xtest"
		extract = conf.get("test")
		self.assertEqual(extract.value, expect_value)
		conf.set("test",changed_value)
		conf.save()
		conf2 = api.Config()
		conf2.load()
		extract = conf2.get("test")
		self.assertEqual(extract.value, changed_value)
		conf2.set("test",expect_value)
		conf2.save()

	def test_search(self):
		"""This test the search action."""
		res = api.search("#c")
		self.assertGreater(len(res), 0)