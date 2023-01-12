import unittest
from os.path import exists

from python import datamining as dm
from python.common import constants


class TestDatamining(unittest.TestCase):
	"""This class contains the unit tests for the datamining module."""

	def test_chebi_archive(self):
		"""This test is for ChebiArchive methods"""
		dm.ChebiArchive.download("https://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_lite_3star.sdf.gz")
		# TODO: Change the url dependance
		self.assertTrue(exists(constants.CHEBI_ARCHIVE_PATH))
		dm.ChebiArchive.clear_cache()
		self.assertFalse(exists(constants.CHEBI_ARCHIVE_PATH))

	def test_chebi_archive_hash(self):
		"""This test will test the hash."""
		dm.ChebiArchive.download("https://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_lite.sdf.gz")
		diff = dm.ChebiArchive.get_hash()
		dm.ChebiArchive.download("https://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_lite_3star.sdf.gz")
		result = dm.ChebiArchive.get_hash()
		self.assertNotEqual(result, diff)

	def test_chebi_database(self):
		"""This test is for ChebiDatabase method"""
		if not exists(constants.CHEBI_ARCHIVE_PATH):
			dm.ChebiArchive.download("https://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_lite_3star.sdf.gz")
			# TODO: Change the url dependance
		dm.ChebiDatabase.extract()
		self.assertFalse(exists(constants.CHEBI_ARCHIVE_PATH))
		self.assertTrue(exists(constants.CHEBI_DATABASE_PATH))
		dm.ChebiDatabase.clear_cache()
		self.assertFalse(exists(constants.CHEBI_DATABASE_PATH))

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
				dm.ChebiArchive.download("https://ftp.ebi.ac.uk/pub/databases/chebi/SDF/ChEBI_lite_3star.sdf.gz")
				# TODO: Change the url dependance
			dm.ChebiDatabase.extract()
			self.assertFalse(exists(constants.CHEBI_ARCHIVE_PATH))
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
	
	