from python.common import constants
from python import datamining as dm
from python.api import config

from os.path import exists

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
		# When the hash file exist or not
		if exists(constants.CHEBI_HASH_PATH):
			dm.ChebiArchive.download(conf.get("chebi_url").value)
			# Compare hash
			new_hash = dm.ChebiArchive.get_hash()
			f = open(constants.CHEBI_HASH_PATH, "r")
			old_hash = f.read()
			f.close()
			if new_hash != old_hash:
				dm.ChebiDatabase.extract()
				sync = True
		else :
			dm.ChebiArchive.download(conf.get("chebi_url").value)
			# Write hash file
			f = open(constants.CHEBI_HASH_PATH, "w")
			f.write(dm.ChebiArchive.get_hash())
			f.close()
			# Extract Database
			dm.ChebiDatabase.extract()
			sync = True
		# Erase the archive file
		dm.ChebiArchive.clear_cache()
	except Exception:
		raise Exception("IOError")
	# If the database change, synchronisation
	if sync:
		try :
			chebi_db = dm.ChebiDatabase()
			nb_mol = 0
			for mol in chebi_db:
				mol.to_file()
				nb_mol += 1
				# TODO: Use the database module to insert the molecules in the database
				# TODO: Use the nauty module to find the isomorphic sets
			dm.ChebiDatabase.clear_cache()
			return nb_mol
		except Exception as e:
			raise Exception(e.args)
	else :
		return 0

def generate_molecules_distribution():
	"""Generates the molecules distribution.

	TODO: Complete the description.
	"""
	# return ?
