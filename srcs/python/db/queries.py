from python.db.models import Molecule, IsIsomorphic, IsomorphicSet
from python.db.options import *

def list_isomorphic_sets(options: QueryOptions=None) -> list:
	"""List all the isomorphic sets in the database.

	Args:
		options: Options for the query.

	Returns:
		A list of isomorphic sets.
	"""
	# TODO: Return a list of isomorphic sets.

def list_isomorphic_sets_of_molecule(id_mol: int, options: QueryOptions=None) -> list:
	"""List all the isomorphic sets of a molecule.

	Args:
		id_mol: The ID of the molecule.
		options: Options for the query.

	Returns:
		A list of isomorphic sets.
	"""
	# TODO: Return the list of isomorphic sets of a molecule.

def list_molecules(options: QueryOptions=None) -> list:
	"""List all the molecules in the database.

	Args:
		options: Options for the query.

	Returns:
		A list of molecules.
	"""
	# TODO: Return a list of molecules.

def list_molecules_in_set(id_set: int, options: QueryOptions=None) -> list:
	"""List all the molecules in a set.

	Args:
		id_set: The ID of the set.
		options: Options for the query.

	Returns:
		A list of molecules.
	"""
	# TODO: Return the list of molecules in a set.

def find_molecules(query: str, options: QueryOptions=None) -> list:
	"""Search a molecule in the database by name or formula.

	Args:
		query: The query to search.
		options: Options for the query.

	Returns:
		A list of molecules corresponding to the search criteria.
	"""
	# TODO: Return a list of molecules corresponding to the search.
