import unittest
from os.path import exists

from python import datamining as dm
from python.common import constants


class TestDatamining(unittest.TestCase):
	"""This class contains the unit tests for the datamining module."""
	url = "https://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_lite_3star.sdf.gz"
	
	def test_chebi_archive(self):
		"""This test is for ChebiArchive methods"""
		dm.ChebiArchive.download(self.url)
		# TODO: Change the url dependance
		self.assertTrue(exists(constants.CHEBI_ARCHIVE_PATH))
		dm.ChebiArchive.clear_cache()
		self.assertFalse(exists(constants.CHEBI_ARCHIVE_PATH))

	def test_chebi_archive_error(self):
		"""This test is for ChebiArchive download error"""
		with self.assertRaises(IOError):
			# raise IOError if url incorrect
			dm.ChebiArchive.download(self.url+"X")

	def test_chebi_archive_hash_error(self):
		"""This test will test the error in ChebiArchive hash."""
		dm.ChebiArchive.clear_cache()
		with self.assertRaises(IOError):
			# raise IOError if no file
			dm.ChebiArchive.get_hash()
	
	def test_chebi_database(self):
		"""This test is for ChebiDatabase method"""
		if not exists(constants.CHEBI_ARCHIVE_PATH):
			dm.ChebiArchive.download(self.url)
			# TODO: Change the url dependance
		dm.ChebiDatabase.extract()
		self.assertFalse(exists(constants.CHEBI_ARCHIVE_PATH))
		self.assertTrue(exists(constants.CHEBI_DATABASE_PATH))
		dm.ChebiDatabase.clear_cache()
		self.assertFalse(exists(constants.CHEBI_DATABASE_PATH))
	
	def test_chebi_database_init_error(self):
		"""This test will test the error in ChebiDatabase init."""
		dm.ChebiDatabase.clear_cache()
		with self.assertRaises(IOError):
			# raise IOError if no file
			dm.ChebiDatabase()
	
	def test_chebi_database_extract_error(self):
		"""This test will test the error in ChebiDatabase extract."""
		dm.ChebiArchive.clear_cache()
		with self.assertRaises(IOError):
			# raise IOError if no file
			dm.ChebiDatabase.extract()

	def test_molecule(self):
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
	
	def test_molecule_hash(self):
		"""This test will compare two molecule hash."""
		mol1 = dm.Molecule("0", "test")
		mol1.add_atom('C')
		mol1.add_atom('C')
		mol1.add_atom('O')
		mol2 = dm.Molecule("0", "test")
		mol2.add_atom('C')
		mol2.add_atom('C')
		mol2.add_atom('O')
		self.assertEqual(mol1.get_hash(),mol2.get_hash())

	def test_chebi_database_iterator(self):
		"""This test will iter on molecule."""
		if not exists(constants.CHEBI_DATABASE_PATH):
			if not exists(constants.CHEBI_ARCHIVE_PATH):
				dm.ChebiArchive.download(self.url)
				# TODO: Change the url dependance
			dm.ChebiDatabase.extract()
			self.assertFalse(exists(constants.CHEBI_ARCHIVE_PATH))
		cdb  = dm.ChebiDatabase()
		iterator = iter(cdb)
		mol = next(iterator)
		# Fisrt one in lite_3star file
		self.assertEqual(str(90), mol.identifier)
		self.assertEqual(22,len(mol._atoms))
		self.assertIn(['3','20','1'],mol._bonds)
		mol = next(iterator)
		# Second one in lite_3star file
		self.assertEqual(str(165), mol.identifier)
		self.assertEqual(11,len(mol._atoms))
		self.assertIn(['5','10','1'],mol._bonds)
	
	