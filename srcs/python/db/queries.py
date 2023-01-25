from python.datamining import Molecule as StructMol
from python.db.models import IsIsomorphic as IsIso
from python.db.models import IsomorphicSet as IsoSet
from python.db.models import Molecule as DbMol
from python.db.options import *
from playhouse.shortcuts import fn

def list_isomorphic_sets(options: QueryOptions=None) -> list:
	"""List all the isomorphic sets in the database.

	Args:
		options: Options for the query.

	Returns:
		A list of isomorphic sets.
	"""
	rows = IsoSet.select().execute()
	result = []
	for elem in rows :
		result.append({"id": elem.id, "mult_bound": elem.mult_bound, "nauty_sign": elem.nauty_sign})
	return result

def list_isomorphic_sets_of_molecule(id_mol: int, options: QueryOptions=None) -> list:
	"""List all the isomorphic sets of a molecule.

	Args:
		id_mol: The ID of the molecule.
		options: Options for the query.

	Returns:
		A list of isomorphic sets.
	"""
	# TODO: return SQL instructions
	rows = IsoSet.select(IsoSet.id, IsoSet.nauty_sign, IsoSet.mult_bound).join(IsIso, on=(IsIso.id_set == IsoSet.id)).where(IsIso.id_mol == id_mol)
	result = []
	for elem in rows :
		result.append({"id": elem.id, "mult_bound": elem.mult_bound, "nauty_sign": elem.nauty_sign})
	return result

def list_molecules(options: QueryOptions=None) -> list:
	"""List all the molecules in the database.

	Args:
		options: Options for the query.

	Returns:
		A list of molecules.
	"""
	rows = DbMol.select().execute()
	result = []
	for elem in rows :
		result.append({"id": elem.id, "nb_atoms": elem.nb_atoms, "name": elem.name})
	return result


def list_molecules_in_set(id_set: int, options: QueryOptions=None) -> list:
	"""List all the molecules in a set.

	Args:
		id_set: The ID of the set.
		options: Options for the query.

	Returns:
		A list of molecules.
	"""
	rows = DbMol.select(DbMol.id, DbMol.name, DbMol.nb_atoms).join(IsIso, on=(IsIso.id_mol == DbMol.id)).where(IsIso.id_set == id_set)
	result = []
	for elem in rows :
		result.append({"id": elem.id, "nb_atoms": elem.nb_atoms, "name": elem.name})
	return result

def find_molecules(query: str, options: QueryOptions=None) -> list:
	"""Search a molecule in the database by name.

	Args:
		query: The query to search.
		options: Options for the query.

	Returns:
		A list of molecules corresponding to the search criteria.
	"""
	rows = DbMol.select().where(DbMol.name.contains(query))
	result = []
	for elem in rows :
		result.append({"id": elem.id, "nb_atoms": elem.nb_atoms, "name": elem.name})
	return result

def contains_molecule(id_mol, options: QueryOptions=None) -> bool:
	"""Test the presence of one molecule.

	Args:
		id_mol: The ID of the molecule.
		options: Options for the query.

	Returns:
		A boolean, True if the molecule is on the table.
		
	"""
	rows = DbMol.select().where(DbMol.id==int(id_mol))
	return len(rows)>0
 
def find_molecule_by_id(id_mol, options: QueryOptions=None) -> DbMol:
	"""Return all the informations of one molecule.

	Args:
		id_mol: The ID of the molecule.
		options: Options for the query.

	Returns:
		One molecule.
		
	"""
	rows = DbMol.select().where(DbMol.id==int(id_mol))
	if len(rows)==1:
		obj = rows[0]
		return obj
	return None

def find_molecule_by_name(name_mol, options: QueryOptions=None) -> DbMol:
	"""Return all the informations of one molecule.

	Args:
		id_mol: The ID of the molecule.
		options: Options for the query.

	Returns:
		One molecule.
		
	"""
	rows = DbMol.select().where(DbMol.name==name_mol)
	if len(rows)>0:
		obj = rows[0]
		return obj
	return None

def insert_molecule(object: StructMol, options:QueryOptions=None) -> bool:
	"""Create or update one molecule.

	Args:
		object: The molecule as Molecule.class.
		options: Options for the query.

	Returns:
		A boolean, True if created or updated.
		
	"""
	try:
		rows = DbMol.select().where(DbMol.id==int(object.identifier))
		if len(rows)==0 :
			element = DbMol.create(id=int(object.identifier), 
								name=object.name, 
								nb_atoms=len(object._atoms), 
								hash=object.get_hash())
		else :
			element = DbMol(id=int(object.identifier), 
							name=object.name, 
							nb_atoms=len(object._atoms), 
							hash=object.get_hash())
			element.save()
		return True
	except Exception:
		return False

def contains_isoset(nauty_sign, mult_bound:bool, options: QueryOptions=None) -> bool:
	"""Test the presence of one set.

	Args:
		nauty_sign: The signature on Nauty.
		mult_bound: The boolean for multi bound type.
		options: Options for the query.

	Returns:
		A boolean, True if the set is on the table.
		
	"""
	rows = IsoSet.select().where(IsoSet.nauty_sign==nauty_sign, IsoSet.mult_bound==mult_bound)
	return len(rows)==1

def find_isoset_by_sign(nauty_sign, mult_bound:bool, options: QueryOptions=None) -> IsoSet:
	"""Return all the informations of one set.

	Args:
		nauty_sign: The signature of the set of isomorphism.
		mult_bound: The boolean for multi bound type.
		options: Options for the query.

	Returns:
		One set information.
		
	"""
	rows = IsoSet.select().where(IsoSet.nauty_sign==nauty_sign, IsoSet.mult_bound==mult_bound)
	if len(rows)==1:
		return rows[0] #return only the first
	return None

def find_isoset_by_id(id_set, options: QueryOptions=None) -> IsoSet:
	"""Return all the informations of one set.

	Args:
		id: The ID of the set.
		options: Options for the query.

	Returns:
		One set information.
		
	"""
	rows = IsoSet.select().where(IsoSet.id== id_set)
	if len(rows)==1:
		return rows[0] #return only the first
	return None

def insert_isoset(sign, mult_bound: bool, id_new_mol, options:QueryOptions=None) :
	"""Create or update one set.

	Args:
		sign: The signature on Nauty.
		mult_bound: The use of multi_bound transformation.
		id_new_mol: The ID of the molecule with this signature on Nauty
		options: Options for the query.

	Returns:
		The set ID
		
	"""
	try:
		rows = IsoSet.select().where(IsoSet.nauty_sign==sign, IsoSet.mult_bound==mult_bound)
		if len(rows)==0:
			isoset = IsoSet.create(nauty_sign=sign, mult_bound=mult_bound)
		else :
			isoset = rows[0]
		rows = IsIso.select().where(IsIso.id_set==isoset.id, IsIso.id_mol==id_new_mol)
		if len(rows)==0:
			link = IsIso.create(id_set=isoset.id, id_mol=id_new_mol)
		else :
			link = rows[0]
		return isoset.id
	except Exception as e:
		raise e

def distrib(mult_bound: bool, options:QueryOptions=None) ->list :
	"""Create or update one set.

	Args:
		mult_bound: The use of multi_bound transformation.
		options: Options for the query.

	Returns:
		The list of isoset size
		
	"""
	result = []
	rows = IsIso.select(fn.COUNT(IsoSet.nauty_sign).alias('count')).join(IsoSet, on=(IsIso.id_set == IsoSet.id)).where(IsoSet.mult_bound == mult_bound).group_by(IsoSet.nauty_sign)
	for elem in rows :
		result.append(elem.count)
	return result