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

	def to_file(self):
		"""Write the molecule to a file.

		Returns:
			The path to the file.

		Raises:
			IOError: If the file cannot be written.
		"""
		# TODO: Write the molecule to MOLECULES_PATH/identifier.sdf using the format defined in the specs.
