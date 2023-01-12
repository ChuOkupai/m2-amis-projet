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
		return sha256.hexdigest()

class ChebiDatabase:
	"""Reads a ChEBI database as a structure-data file (SDF)."""

	@staticmethod
	def clear_cache():
		"""Clears the cache. It removes the extracted file."""
		if exists(constants.CHEBI_DATABASE_PATH):
			remove(constants.CHEBI_DATABASE_PATH)

	@staticmethod
	def extract():
		"""Extracts the ChEBI database file. Remove the downloaded file on success.

		Raises:
			IOError: If the file cannot be extracted.
		"""
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
		except Exception:
			if f_in : 
				f_in.close()
			if f_out : 
				f_out.close()
			raise Exception("IOError")

	def __init__(self):
		"""Open the ChEBI database file.

		Raises:
			IOError: If the file cannot be opened.
		"""
		# TODO: Store the file object (What did that mean?)
		try :
			self.file = open(constants.CHEBI_DATABASE_PATH, 'r')
		except Exception:
			self.file.close()
			raise Exception("IOError")

	def __del__(self):
		"""Close the ChEBI database file."""
		self.file.close()

	def __iter__(self):
		"""Iterate over the molecules in the ChEBI database.
		
		Returns:
			An iterator.
		"""
		self.tab = self.file.readlines()
		self.head = -1			# Reading head
		self.current_mol = -1	# Begin current molecule
		self.next_mol = 0		# Next molecule
		return self

	def __next__(self) -> Molecule:
		"""Get the next molecule in the ChEBI database.

		Returns:
			A molecule.

		Raises:
			ParserError: If an error occurs while parsing the file.
			StopIteration: If there are no more molecules.
		"""
		if self.next_mol == len(self.tab):
			raise StopIteration
		try :
			# new reading head
			self.current_mol = self.next_mol
			self.head = self.next_mol
			# Search for the next tag
			self.next_mol = self.search_tag("$$$$", len(self.tab))+1
			# Search name and ID
			chebi_id = None
			name = None
			self.head = self.search_tag("> <ChEBI ID>", self.next_mol)
			if self.head < self.next_mol :
				line = self.tab[self.head+1].split()
				line = line[0].split(':')
				chebi_id = line[1]
			else :
				raise Exception("id", self.head, self.next_mol)
			self.head = self.current_mol
			self.head = self.search_tag("> <ChEBI Name>", self.next_mol)
			if self.head < self.next_mol :
				name = self.tab[self.head+1][:-1]
			else :
				raise Exception("name")
			# Create Molecule
			mol = Molecule(chebi_id, name)
			# Search for the nodes
			atom_begin = self.current_mol+4
			nb_nodes = self.read_nodes(atom_begin, mol)
			# Search for the bonds
			bond_begin = self.current_mol+4+nb_nodes
			self.read_bonds(bond_begin, mol)
			
		except Exception as e:
			raise Exception("ParsingError", self.current_mol, e.args)
		return mol

	def search_tag(self, tag, limit: int):
		"""Get the next line with the tag after the reading head and before the limit line.

		Returns:
			A line number.
		"""
		i = self.head
		while tag not in self.tab[i] and i<limit:
			i += 1
		return i

	def read_nodes(self, begin: int, mol: Molecule):
		"""Add atoms to the molecule mol.
		Read after the begin line while line have the atom format.

		Returns:
			The number of atoms.
		"""
		i = begin
		line = self.tab[i].split()
		while len(line)>=13:
			mol.add_atom(line[3])
			i += 1
			line = self.tab[i].split()
		return i - begin

	def read_bonds(self, begin: int, mol: Molecule):
		"""Add bonds to the molecule mol.
		Read after the begin line while line have the bond format.

		Returns:
			The number of bonds.
		"""
		i = begin
		line = self.tab[i].split()
		while len(line)>=6:
			mol.add_bond(line[0:3])
			i += 1
			line = self.tab[i].split()
		return i - begin