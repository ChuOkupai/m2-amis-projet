import unittest
from python import datamining as dm
from python.common import constants

from os.path import exists

class TestDatamining(unittest.TestCase):
	"""This class contains the unit tests for the datamining module."""

	def test_chebi_archive_clear(self):
		"""This test is for ChebiArchive clear method"""
		dm.ChebiArchive.clear_cache()
		self.assertFalse(exists(constants.CHEBI_ARCHIVE_PATH))

	def test_chebi_archive_download(self):
		"""This test is for ChebiArchive download methodd"""
		dm.ChebiArchive.download("https://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_lite_3star.sdf.gz")
		# TODO: Change the test and the url dependance
		self.assertTrue(exists(constants.CHEBI_ARCHIVE_PATH))
		dm.ChebiArchive.clear_cache()

	def test_chebi_archive_hash(self):
		"""This test will test the hash."""
		# TODO: Change the test
		result = 1
		expect = 0
		if not exists(constants.CHEBI_ARCHIVE_PATH):
			dm.ChebiArchive.download("https://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_lite_3star.sdf.gz")
		result = dm.ChebiArchive.get_hash()
		if exists(constants.CHEBI_HASH_PATH):
			f = open(constants.CHEBI_HASH_PATH, "r")
			expect = f.read()
			f.close()
		self.assertEqual(result, expect)

	def test_chebi_database_clear(self):
		"""This test is for ChebiDatabase clear method"""
		dm.ChebiDatabase.clear_cache()
		self.assertFalse(exists(constants.CHEBI_DATABASE_PATH))

	def test_chebi_database_extract(self):
		"""This test will extract the file from the archive."""
		if not exists(constants.CHEBI_ARCHIVE_PATH):
			dm.ChebiArchive.download("https://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_lite_3star.sdf.gz")
		dm.ChebiDatabase.extract()
		# TODO: Change the test and the url dependance
		self.assertTrue(exists(constants.CHEBI_DATABASE_PATH))

	def test_chebi_database_iterator(self):
		"""This test will iter on molecule."""
		# TODO: Create the test
		self.assertEqual(1, 1)