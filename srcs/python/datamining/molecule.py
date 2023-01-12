from python.common import constants
from os import mkdir
from os.path import isdir, join

class Molecule:
	"""A molecule."""

	def __init__(self, identifier, name):
		"""Initialize a molecule."""
		self.identifier = identifier
		self.name = name
		self._atoms = []
		self._bonds = []

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
		if self.name!=None and self.identifier!=None : # and len(self._atoms)!=0 and len(self._bonds)!=0:
			try :
				path = join(constants.MOLECULES_PATH, str(self.identifier)+".txt")
				f_out = open(path, "w")
				#f_out.write(str(self.identifier)+'\n') # IDs
				#f_out.write(self.name+'\n') # Name
				f_out.write(str(len(self._atoms))+' '+str(len(self._bonds))+'\n') # Atoms and Bonds number
				# Concat atoms
				f_out.write(self._atoms_to_string()+'\n')
				# Format for bonds
				f_out.write(self._bonds_to_string())
				f_out.close()
				return path
			except Exception :
				raise Exception("IOError")
		# if not name or id, do nothing
		return None