from python.datamining.molecule import Molecule
from python.common import constants

from os import remove
from os.path import exists
import gzip
import shutil
import requests
import hashlib


class ChebiArchive:
	"""Tools to download and extracts the ChEBI database."""

	@staticmethod
	def clear_cache():
		"""Clears the cache. It removes the downloaded file."""
		# TODO: Test for Remove CHEBI_ARCHIVE_PATH.
		if exists(constants.CHEBI_ARCHIVE_PATH):
			remove(constants.CHEBI_ARCHIVE_PATH)

	@staticmethod
	def download(url):
		"""Downloads the ChEBI database. If the file already exists, it is first removed.

		Args:
			url: The URL to the ChEBI database.

		Raises:
			IOError: If the file cannot be downloaded. #TODO: Error can't be raised for test part
		"""
		# TODO: Test for Download the file from url to CHEBI_ARCHIVE_PATH.
		ChebiArchive.clear_cache()
		try:
			response = requests.get(url)
		except Exception:
			#print("Error in the chebi url or download : ",url)
			raise Exception("IOError")
		try:
			f = open(constants.CHEBI_ARCHIVE_PATH, "wb")
			f.write(response.content)
			f.close()
		except Exception:
			#print("Error in coping file \n")
			raise Exception("IOError")
		

	@staticmethod
	def get_hash():
		"""Gets the hash of the ChEBI archive.

		Returns:
			The hash of the downloaded file.

		Raises:
			IOError: If the file cannot be opened.
		"""
		# TODO: Test for Return the SHA-256 of the file from CHEBI_ARCHIVE_PATH.
		BUF_SIZE = 65536
		sha256 = hashlib.sha256()
		try :
			with open(constants.CHEBI_ARCHIVE_PATH, 'rb') as f:
				while True:
					data = f.read(BUF_SIZE)
					if not data:
						f.close()
						break
					sha256.update(data)
		except Exception:
			raise Exception("IOError")
		# TODO: move this code somewhere else
		f = open(constants.CHEBI_HASH_PATH, "w")
		f.write(sha256.hexdigest())
		f.close()
		return sha256.hexdigest() #0x6f01af629fc8e15a3f88f38c698af68722298839214eada0590218699e0c4fbf

class ChebiDatabase:
	"""Reads a ChEBI database as a structure-data file (SDF)."""

	@staticmethod
	def clear_cache():
		"""Clears the cache. It removes the extracted file."""
		# TODO: Test for Remove CHEBI_DATABASE_PATH.
		if exists(constants.CHEBI_DATABASE_PATH):
			remove(constants.CHEBI_DATABASE_PATH)

	@staticmethod
	def extract():
		"""Extracts the ChEBI database file. Remove the downloaded file on success.

		Raises:
			IOError: If the file cannot be extracted.
		"""
		# TODO: Test for Extract the file from CHEBI_ARCHIVE_PATH to CHEBI_DATABASE_PATH.
		# TODO: Remove the downloaded file (did that mean the CHEBI_ARCHIVE one?)
		f_in, f_out = None, None
		try:
			if not exists(constants.CHEBI_ARCHIVE_PATH):
				raise Exception("FileNotFoundError")
			with gzip.open(constants.CHEBI_ARCHIVE_PATH, 'rb') as f_in:
				with open(constants.CHEBI_DATABASE_PATH, 'wb') as f_out:
					shutil.copyfileobj(f_in, f_out)
			f_in.close()
			f_out.close()
			#print("succesful decompress of the file ")
		except Exception:
			if f_in : 
				f_in.close()
			if f_out : 
				f_out.close()
			#print("Error in decompressing file \n")
			raise Exception("IOError")

	def __init__(self):
		"""Open the ChEBI database file.

		Raises:
			IOError: If the file cannot be opened.
		"""
		# TODO: Test for Open the file from CHEBI_DATABASE_PATH and store the file object
		try :
			self.file = open(constants.CHEBI_DATABASE_PATH, 'r')
			self.file.close() # TODO: Move to the end process in next
		except Exception:
			self.file.close()
			raise Exception("IOError")


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

