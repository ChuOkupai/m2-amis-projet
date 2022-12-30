class Compare:
	"""Compare two molecules."""

	def __init__(self, molecule1, molecule2):
		"""Initialize the similarity.

		Args:
			molecule1: The identifier of the first molecule.
			molecule2: The identifier of the second molecule.
		"""
		self._molecule1 = molecule1
		self._molecule2 = molecule2
		# TODO: Loads the molecules from the database and the system file.

	def get_atoms_frequency(self):
		"""Get the frequency of atoms.

		Returns:
			A pair of dictionaries with the frequency of atoms in the molecules.
		"""
		# TODO: Calculate the frequency of atoms in the molecules.
		return ({}, {})

	def get_bonds_frequency(self):
		"""Get the frequency of bonds.

		Returns:
			A pair of dictionaries with the frequency of bonds in the molecules.
		"""
		# TODO: Calculate the frequency of bonds in the molecules.
		return ({}, {})

	def mcis(self):
		"""Get the maximum common induced subgraph.

		Returns:
			The size of the maximum common induced subgraph.
		"""
		# TODO: Calculate the maximum common induced subgraph of the molecules.
		return 0
