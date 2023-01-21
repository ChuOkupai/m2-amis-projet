import unittest

from peewee import *
from python.datamining.molecule import Molecule as StructMol
from python.db import Connection
from python.db.queries import *

MODELS = [DbMol, IsoSet, IsIso]

class TestDb(unittest.TestCase):
	"""This class contains the unit tests for the DB module."""
	
	def setUp(self):
		_conn = Connection.get_instance()
		if len(_conn.get_tables()) == 0:
			_conn.create_tables(MODELS)
	
	""" Trop fort lorsque la base de données a été rempli"""
	def tearDown(self):
		DbMol.delete_by_id(3)
		DbMol.delete_by_id(5)
		IsoSet.delete().where(IsoSet.nauty_sign=="signature")
		IsIso.delete().where(IsIso.id_mol==3)
		IsIso.delete().where(IsIso.id_mol==5)
		#_conn = Connection.get_instance()
		#_conn.drop_tables([DbMol, IsIsomorphic, IsomorphicSet])
	

	def test_insert_Mol(self):
		"""This test is for the molecule insertion method."""
		obj1 = DbMol.create(id = 3, name="eau", nb_atoms=3, hash="jnfz")
		obj1.save()
		obj2 = DbMol.get_by_id(3)
		self.assertEqual(obj1, obj2)
		DbMol.delete_by_id(3)

	def test_contains_mol(self):
		"""This test is for the molecule insertion method."""
		obj1 = DbMol.create(id = 3, name="eau", nb_atoms=3, hash="jnfz")
		self.assertTrue(contains_molecule(3))
		DbMol.delete_by_id(3)

	def test_queries_insert_mol(self):
		"""This test is for the molecule insertion method."""
		obj1 = StructMol(identifier = str(5), name="eau")
		insert_molecule(obj1)
		obj2 = DbMol.get_by_id(5)
		self.assertEqual(obj1.identifier, str(obj2.id))
		self.assertEqual(obj1.name, obj2.name)
		obj1.name = "caf"
		insert_molecule(obj1)
		obj2 = DbMol.get_by_id(5)
		self.assertEqual("5", str(obj2.id))
		self.assertEqual("caf", obj2.name)
		DbMol.delete_by_id(5)
	
	def test_find_molecule_by_name(self):
		"""This test is for find_molecule_by_name"""
		obj1 = StructMol(identifier = str(5), name="eau")
		insert_molecule(obj1)
		obj2 = find_molecule_by_name("eau")
		self.assertEqual(obj1.identifier, str(obj2.id))
		self.assertEqual(obj1.name, obj2.name)
		DbMol.delete_by_id(5)
  
	def test_find_molecule_by_id(self):
		"""This test is for find_molecule_by_id"""
		obj1 = StructMol(identifier = str(5), name="eau")
		insert_molecule(obj1)
		obj2 = find_molecule_by_id(5)
		self.assertEqual(obj1.identifier, str(obj2.id))
		self.assertEqual(obj1.name, obj2.name)
		DbMol.delete_by_id(5)

	def test_contains_isoset(self):
		"""This test is for the molecule insertion method."""
		DbMol.create(id = 3, name="eau", nb_atoms=3, hash="jnfz")
		insert_isoset("signature", False, 3)
		self.assertTrue(contains_isoset("signature",False))
		DbMol.delete_by_id(3)
		IsoSet.delete().where(IsoSet.nauty_sign=="signature")

	def test_queries_insert_Set(self):
		"""This test the set insertion."""
		obj1 = StructMol(identifier = str(5), name="eau")
		obj2 = StructMol(identifier = str(3), name="caf")
		insert_molecule(obj1)
		insert_molecule(obj2)
		insert_isoset("signature", False, 5)
		set1 = IsoSet.select().where(IsoSet.nauty_sign=="signature")
		self.assertTrue(len(set1)>0)
		self.assertEqual("signature", set1[0].nauty_sign)
		self.assertFalse(set1[0].mult_bound)
		insert_isoset("signature", True, 3)
		set2 = IsoSet.select().where(IsoSet.nauty_sign=="signature")
		self.assertTrue(len(set1)==2)
		self.assertEqual(set1[0].id, set2[0].id)
		IsoSet.delete().where(IsoSet.nauty_sign=="signature")
		DbMol.delete_by_id(3)
		DbMol.delete_by_id(5)
	
	def test_find_isoset_by_sign(self):
		"""This test is for find_molecule_by_name"""
		obj1 = StructMol(identifier = str(5), name="eau")
		insert_molecule(obj1)
		insert_isoset("signature", False, 5)
		obj2 = find_isoset_by_sign("signature",False)
		self.assertEqual("signature",obj2.nauty_sign)
		self.assertFalse(obj2.mult_bound)
		IsoSet.delete().where(IsoSet.nauty_sign=="signature")
  
	def test_find_isoset_by_id(self):
		"""This test is for find_molecule_by_id"""
		obj1 = StructMol(identifier = str(5), name="eau")
		insert_molecule(obj1)
		insert_isoset("signature", False, 5)
		obj2 = find_isoset_by_sign("signature",False)
		obj3 = find_isoset_by_id(obj2.id)
		self.assertEqual("signature",obj3.nauty_sign)
		self.assertTrue(obj2==obj3)
		IsoSet.delete().where(IsoSet.nauty_sign=="signature")

	def test_list(self):
		"""This test is for select queries"""
		obj1 = StructMol(identifier = str(5), name="eau")
		insert_molecule(obj1)
		id1 = insert_isoset("signature", False, 5)
		list = list_isomorphic_sets()
		self.assertGreater(len(list), 0)
		list = list_molecules()
		self.assertGreater(len(list), 0)
		IsoSet.delete().where(IsoSet.nauty_sign=="signature")
		DbMol.delete_by_id(5)
	
	def test_list_isosets_of_mol(self):
		"""This test is for list_isosets_in_mol"""
		obj1 = StructMol(identifier = str(5), name="eau")
		insert_molecule(obj1)
		id1 = insert_isoset("signature", False, 5)
		id2 = insert_isoset("signature", True, 5)
		list = list_isomorphic_sets_of_molecule(5)
		self.assertTrue(len(list)==2)
		self.assertTrue(id1 in (list[0].id, list[1].id))
		self.assertTrue(id2 in (list[0].id, list[1].id))
		IsoSet.delete().where(IsoSet.nauty_sign=="signature")
		DbMol.delete_by_id(5)

	def test_list_molecules_in_set(self):
		"""This test is for list_molecules_in_set"""
		obj1 = StructMol(identifier = str(5), name="eau")
		obj2 = StructMol(identifier = str(3), name="caf")
		insert_molecule(obj1)
		insert_molecule(obj2)
		set1 = insert_isoset("signature", False, 5)
		set2 = insert_isoset("signature", False, 3)
		self.assertEqual(set1,set2)
		list = list_molecules_in_set(set1)
		self.assertTrue(len(list)==2)
		self.assertTrue(3 in (list[0].id, list[1].id))
		self.assertTrue(5 in (list[0].id, list[1].id))
		IsoSet.delete().where(IsoSet.nauty_sign=="signature")
		DbMol.delete_by_id(3)
		DbMol.delete_by_id(5)

	