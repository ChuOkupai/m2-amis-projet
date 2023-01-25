import hashlib
from os import mkdir
from os.path import isdir, join

from python.common import constants


class Molecule:
	"""A molecule."""

	def __init__(self, identifier, name : str):
		"""Initialize a molecule."""
		self.identifier = identifier
		self.name = name.replace(' ', '_')
		self._atoms = []
		self._bonds = []
		self.hash = None

	def add_atom(self, atom):
		"""Add an atom to the molecule.

		Args:
			atom: The atom to add.
		"""
		self._atoms.append(atom)

	def add_bond(self, bond):
		"""Add a bond to the molecule.

		Args:
			bond: The bond to add.
		"""
		self._bonds.append(bond)

	def _atoms_to_string(self):
		"""Concat the atoms
		Returns:
			The string of the atoms.
		"""
		s = ""
		if len(self._atoms)>0:
			for atom in self._atoms:
				s += str(atom) + ' '
			return s[:-1]
		return s

	def _bonds_to_string(self):
		"""Concat the bonds
		Returns:
			The string of the atoms.
		"""
		s = ""
		if len(self._bonds)>0:
			for bond in self._bonds:
				for elem in bond:
					s += str(elem) + ' '
				s = s[:-1] + '\n'
		return s

	def get_hash(self):
		"""Gets the hash of the object.

		Returns:
			The hash of the Molecule object.
		"""
		if self.hash == None:
			sha256 = hashlib.sha256()
			sha256.update(bytes(self.identifier, encoding='utf-8'))
			sha256.update(bytes(self.name, encoding='utf-8'))
			for atom in self._atoms:
				sha256.update(bytes(atom, encoding='utf-8'))
			for bond in self._bonds:
				string = bond[0]+' '+bond[1]+' '+bond[2]
				sha256.update(bytes(string, encoding='utf-8'))
			self.hash = sha256.hexdigest()
		return self.hash

	def to_file(self):
		"""Write the molecule to a file MOLECULES_PATH/identifier.txt 
			using the format defined here :
				[number_of_atoms] SPACE [number_of_bonds] LF
				[[atom_element]*number_of_atoms] LF
				[[atom1_number] SPACE [atom1_number] SPACE [bond_type] LF]*number_of_bonds

		Returns:
			The path to the file.

		Raises:
			IOError: If the file cannot be written.
		"""
		if not isdir(constants.MOLECULES_PATH):
			mkdir(constants.MOLECULES_PATH)
		if self.name!=None and self.identifier!=None and len(self._bonds) > 1:
			try :
				path = join(constants.MOLECULES_PATH, str(self.identifier)+".txt")
				f_out = open(path, "w")
				f_out.write(str(len(self._atoms))+' '+str(len(self._bonds))+'\n') # Atoms and Bonds number
				# Concat atoms
				f_out.write(self._atoms_to_string()+'\n')
				# Format for bonds
				f_out.write(self._bonds_to_string())
				f_out.close()
				return path
			except (OSError, Exception) :
				raise IOError
		# if not name or id, do nothing
		return None