import gzip
import hashlib
import shutil
from os import remove
from os.path import exists
from parser import ParserError

import requests
from python.common import constants
from python.datamining.molecule import Molecule
from requests.exceptions import RequestException


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
			IOError: If the file cannot be downloaded.
		"""
		ChebiArchive.clear_cache()
		try:
			response = requests.get(url)
			response.raise_for_status()
		except RequestException as e :
			#print("Error in the chebi url or http request : ",url)
			raise IOError(e.args, url)
		try:
			f = open(constants.CHEBI_ARCHIVE_PATH, "wb")
			f.write(response.content)
			f.close()
		except (OSError, Exception):
			#print("Error in coping file \n")
			raise IOError
		

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
		except (OSError, FileNotFoundError, Exception):
			raise IOError
		return sha256.hexdigest()

class ChebiDatabase:
	"""Reads a ChEBI database as a structure-data file (SDF)."""
	file = None

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
		f_in, f_out = None, None
		try:
			if not exists(constants.CHEBI_ARCHIVE_PATH):
				raise FileNotFoundError
			with gzip.open(constants.CHEBI_ARCHIVE_PATH, 'rb') as f_in:
				with open(constants.CHEBI_DATABASE_PATH, 'wb') as f_out:
					shutil.copyfileobj(f_in, f_out)
			f_in.close()
			f_out.close()
			ChebiArchive.clear_cache()
		except (OSError, FileNotFoundError, Exception) :
			if f_in:
				f_in.close()
			if f_out:
				f_out.close()
			raise IOError

	def __init__(self, path=constants.CHEBI_DATABASE_PATH):
		"""Open the ChEBI database file.

		Args:
			path: The PATH to the ChEBI database.

		Raises:
			IOError: If the file cannot be opened.
		"""
		try :
			self.file = open(path, 'r')
		except (OSError, FileNotFoundError, Exception):
			if self.file:
				self.file.close()
			raise IOError

	def __del__(self):
		"""Close the ChEBI database file."""
		if self.file:
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
			raise ParserError("id",self.current_mol)
		self.head = self.current_mol
		self.head = self.search_tag("> <ChEBI Name>", self.next_mol)
		if self.head < self.next_mol :
			name = self.tab[self.head+1][:-1]
		else :
			raise ParserError("name",self.current_mol)
		# Create Molecule
		mol = Molecule(chebi_id, name)
		# Search for the nodes
		atom_begin = self.current_mol+4
		nb_nodes = self.read_nodes(atom_begin, mol)
		# Search for the bonds
		bond_begin = self.current_mol+4+nb_nodes
		self.read_bonds(bond_begin, mol)
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
		line = self.tab[i]
		while len(line)>=69:
			elem = line[31:34].replace(' ','')
			if elem == "":
				elem = "*"
			mol.add_atom(elem)
			i += 1
			line = self.tab[i]
		return i - begin

	def read_bonds(self, begin: int, mol: Molecule):
		"""Add bonds to the molecule mol.
		Read after the begin line while line have the bond format.

		Returns:
			The number of bonds.
		"""
		i = begin
		ignored = 0
		line = self.tab[i]
		while len(line)>=21:
			bond = [line[0:3].replace(' ',''),
					line[3:6].replace(' ',''),
					line[6:9].replace(' ','')]
			if bond[0]!='M':
				mol.add_bond(bond)
			else :
				ignored +=1
			i += 1
			line = self.tab[i]
		return i - begin - ignored