from python.datamining.molecule import Molecule

class ChebiArchive:
	"""Tools to download and extracts the ChEBI database."""

	@staticmethod
	def clear_cache():
		"""Clears the cache. It removes the downloaded file."""
		# TODO: Remove CHEBI_ARCHIVE_PATH.

	@staticmethod
	def download(url):
		"""Downloads the ChEBI database. If the file already exists, it is first removed.

		Args:
			url: The URL to the ChEBI database.

		Raises:
			IOError: If the file cannot be downloaded.
		"""
		# TODO: Download the file from url to CHEBI_ARCHIVE_PATH.

	@staticmethod
	def get_hash():
		"""Gets the hash of the ChEBI archive.

		Returns:
			The hash of the downloaded file.

		Raises:
			IOError: If the file cannot be opened.
		"""
		# TODO: Return the SHA-256 of the file from CHEBI_ARCHIVE_PATH.
		return 0x6f01af629fc8e15a3f88f38c698af68722298839214eada0590218699e0c4fbf

class ChebiDatabase:
	"""Reads a ChEBI database as a structure-data file (SDF)."""

	@staticmethod
	def clear_cache():
		"""Clears the cache. It removes the extracted file."""
		# TODO: Remove CHEBI_DATABASE_PATH.

	@staticmethod
	def extract():
		"""Extracts the ChEBI database file. Remove the downloaded file on success.

		Raises:
			IOError: If the file cannot be extracted.
		"""
		# TODO: Extract the file from CHEBI_ARCHIVE_PATH to CHEBI_DATABASE_PATH.

	def __init__(self):
		"""Open the ChEBI database file.

		Raises:
			IOError: If the file cannot be opened.
		"""
		# TODO: Open the file from CHEBI_DATABASE_PATH and store the file object.


	def __iter__(self):
		"""Iterate over the molecules in the ChEBI database.

		Returns:
			An iterator.
		"""
		return self

	def __next__(self) -> Molecule:
		"""Get the next molecule in the ChEBI database.

		Returns:
			A molecule.

		Raises:
			ParserError: If an error occurs while parsing the file.
			StopIteration: If there are no more molecules.
		"""
		# TODO: Implement a parser for the SDF format.
		return Molecule(0, "Molecule")
