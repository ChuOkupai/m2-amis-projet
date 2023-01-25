from os.path import exists

from python.api import config
from python.cli.exceptions import InvalidMoleculeError
from python.common import constants
from python.datamining import ChebiArchive, ChebiDatabase, Graph, Molecule
from python.db import queries
from python.similarity import Compare
from matplotlib import pyplot as plt
import numpy as np

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
	if queries.contains_molecule(int(mol.identifier)) :
		db_mol = queries.find_molecule_by_id(int(mol.identifier))
		if mol.get_hash() == db_mol.hash :
			return False
	# Write the molecule file
	path = mol.to_file()
	if path : # Check if the molecule are written
		queries.insert_molecule(mol)
		# TODO: Use the nauty module to find the isomorphic sets
		return True
	return False

def compare_frequency(molecule1_id : int, molecule2_id : int):
	# Execute
	# Init the compare class
	comp = Compare(molecule1_id,molecule2_id)
	# Show the molecules
	Graph.show_mols(G1=comp._molecule1, node_colors1=comp._colors1, G2=comp._molecule2, node_colors2=comp._colors2)
	return (comp.get_atoms_frequency(), comp.get_bonds_frequency())

def get_mcis(molecule1_id : int, molecule2_id : int):
	# Search MCIS and compute Raymond similarity
	comp = Compare(molecule1_id,molecule2_id)
	return comp.mcis()

def show_graph(mol_id : int):
	G, colors = Graph.get_graph_from_file(mol_id)
	Graph.show_mol(G, colors)

def show_mcis(g_mcis):
	colors = Graph.get_colors(g_mcis)
	Graph.show_mol(g_mcis, colors)

def search(molecule_reference) -> list:
	molecules = queries.find_molecules(molecule_reference)
	if len(molecules) > 0:
		return molecules
	raise InvalidMoleculeError(molecule_reference)

def show_distrib(multi_bound : int):
	distrib = queries.distrib(multi_bound==1)
	distrib = distrib.sort()
	plt.figure()
	values = [x+1 for x in range(len(distrib))]
	plt.bar(x=values, height=distrib)
	plt.ylabel("Number of molecules")
	plt.xlabel("Sets of Isomorphs")
	plt.xticks(values)
	plt.show()
	plt.clf()
	return {'nb_sets':len(distrib), 'nb_molecules': np.cumsum(distrib)[-1]}

def find(molecule_reference) -> Molecule:
	# Test if molecule identifier or name exists in the database and get it
	if (molecule_reference.isdigit()):
		molecule = queries.find_molecule_by_id(int(molecule_reference))	
	else:
		molecule = queries.find_molecule_by_name(molecule_reference)
	if molecule != None:
		return molecule
	raise InvalidMoleculeError(molecule_reference)

def list_set_isomorph_mol(molecule_reference)-> list: 
	# Test if the molecule exists and return the list of isomorphic group of molecules
	molecule = find(molecule_reference)
	if (molecule is not None):
		list_isomorphic_set=queries.list_isomorphic_sets_of_molecule(molecule.id)
		return list_isomorphic_set # TODO : change the return format (actual SQL instruction)

def list_set_isomorph()-> list: 
	# Test if the molecule exists and return the list of isomorphic group of molecules
		list_all_isomorphic_set=queries.list_isomorphic_sets()
		return list_all_isomorphic_set
