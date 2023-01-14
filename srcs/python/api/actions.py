from os.path import exists, join

from python.datamining import ChebiArchive, ChebiDatabase, Molecule
from python.api import config
from python.common import constants


def sync_database():
	"""Update the database.

	Downloads the ChEBI database and extracts it. Then, it parses the file and
	inserts the molecules in the database.
	The nauty library is used to find the isomorphic sets.

	Returns:
		The number of new molecules inserted in the database.
		If the database is already up-to-date, it returns 0.

	Raises:
		IOError: If the file cannot be downloaded or extracted.
		ParseError: If the file cannot be parsed.
	"""
	# Load configuration
	conf = config.Config()
	conf.load()
	sync = False
	try :
		ChebiArchive.download(conf.get("chebi_url").value)
		# When the hash file exist or not
		if exists(constants.CHEBI_HASH_PATH):
			# Compare hash
			new_hash = ChebiArchive.get_hash()
			with open(constants.CHEBI_HASH_PATH, "r") as f:
				old_hash = f.read()
				f.close()
			if new_hash != old_hash:
				# Write hash file
				with open(constants.CHEBI_HASH_PATH, "w") as f:
					f.write(new_hash)
					f.close()
				# Extract Database
				ChebiDatabase.extract()
				sync = True
		else :
			# Write hash file
			with open(constants.CHEBI_HASH_PATH, "w") as f:
				f.write(ChebiArchive.get_hash())
				f.close()
			# Extract Database
			ChebiDatabase.extract()
			sync = True
	except (OSError, FileNotFoundError, IOError):
		raise IOError
	# If the database change, synchronisation
	if sync:
		# This part let raise IOError and ParserError if its occur
		chebi_db = ChebiDatabase()
		nb_mol = 0
		for mol in chebi_db:
			if update_molecule(mol):
				nb_mol += 1
		ChebiDatabase.clear_cache()
		return nb_mol
	else :
		return 0

def update_molecule(mol: Molecule) ->bool:
	"""Update one molecule on the database.

	Returns:
		If the molecule is updated, it returns True
		Else it return False

	Raises:
		IOError: If the molecule file cannot be writed.
	"""
	if mol.identifier == "test" :# TODO: Test if molecule identifier in database
		if mol.get_hash() == "test" :# TODO: Test if hash equal
			return False
	# Write the molecule file
	path = mol.to_file()
	if path : # Check if the molecule are written
		# TODO: Use the database module to insert the molecules in the database
		mol.identifier
		mol.name
		mol.get_hash()
		# TODO: Use the nauty module to find the isomorphic sets
		return True
	return False

def generate_molecules_distribution():
	"""Generates the molecules distribution.

	TODO: Complete the description.
	"""
	# return ?
