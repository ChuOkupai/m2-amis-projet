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
	# TODO: Use the datamining module to download and extract the ChEBI database.
	# TODO: Use the database module to insert the molecules in the database
	# TODO: Use the nauty module to find the isomorphic sets
	return 0

def generate_molecules_distribution():
	"""Generates the molecules distribution.

	TODO: Complete the description.
	"""
	# return ?
