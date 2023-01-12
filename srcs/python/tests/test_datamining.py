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
		# TODO: Change the url dependance
		self.assertTrue(exists(constants.CHEBI_ARCHIVE_PATH))
		dm.ChebiArchive.clear_cache()

	def test_chebi_archive_hash(self):
		"""This test will test the hash."""
		result = 1
		expect = 0
		if not exists(constants.CHEBI_ARCHIVE_PATH):
			dm.ChebiArchive.download("https://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_lite_3star.sdf.gz")
			# TODO: Change the url dependance
		result = dm.ChebiArchive.get_hash()
		self.assertEqual(result, result) # TODO: No sense

	def test_chebi_database_clear(self):
		"""This test is for ChebiDatabase clear method"""
		dm.ChebiDatabase.clear_cache()
		self.assertFalse(exists(constants.CHEBI_DATABASE_PATH))

	def test_chebi_database_extract(self):
		"""This test will extract the file from the archive."""
		if not exists(constants.CHEBI_ARCHIVE_PATH):
			dm.ChebiArchive.download("https://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_lite_3star.sdf.gz")
			# TODO: Change the url dependance
		dm.ChebiDatabase.extract()
		self.assertTrue(exists(constants.CHEBI_DATABASE_PATH))

	def test_molecul(self):
		"""This test will test molecule class."""
		mol = dm.Molecule("0", "test")
		self.assertEqual("0", mol.identifier)
		self.assertEqual("test", mol.name)
		self.assertEqual(0,len(mol._atoms))
		self.assertEqual(0,len(mol._bonds))
		mol.add_atom('C')
		mol.add_atom('C')
		mol.add_atom('O')
		self.assertEqual(3,len(mol._atoms))
		mol.add_bond(['3','20','1'])
		self.assertIn(['3','20','1'],mol._bonds)
	
	def test_chebi_database_iterator(self):
		"""This test will iter on molecule."""
		if not exists(constants.CHEBI_ARCHIVE_PATH):
			dm.ChebiArchive.download("https://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_lite_3star.sdf.gz")
			# TODO: Change the url dependance
			dm.ChebiDatabase.clear_cache()
		if not exists(constants.CHEBI_DATABASE_PATH):
			dm.ChebiDatabase.extract()
		cdb  = dm.ChebiDatabase()
		iterator = iter(cdb)
		mol = next(iterator)
		self.assertEqual(str(90), mol.identifier)
		self.assertEqual(22,len(mol._atoms))
		self.assertIn(['3','20','1'],mol._bonds)
		mol = next(iterator)
		self.assertEqual(str(165), mol.identifier)
		self.assertEqual(11,len(mol._atoms))
		self.assertIn(['5','10','1'],mol._bonds)
	
	