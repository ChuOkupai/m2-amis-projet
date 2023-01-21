from python.datamining.graph import Graph


class Compare:
	"""Compare two molecules."""

	def __init__(self, molecule1, molecule2):
		"""Initialize the similarity.

		Args:
			molecule1: The identifier of the first molecule.
			molecule2: The identifier of the second molecule.
		"""
		self._id1 = molecule1
		self._id2 = molecule2
		self._molecule1, self._colors1 = Graph.get_graph_from_file(self._id1)
		self._molecule2, self._colors2 = Graph.get_graph_from_file(self._id2)

	def get_atoms_frequency(self):
		"""Get the frequency of atoms.

		Returns:
			A pair of dictionaries with the frequency of atoms in the molecules.
		"""
		atoms_frequency = Graph.get_atoms_frequency(self._molecule1,self._molecule2)
		return atoms_frequency

	def get_bonds_frequency(self):
		"""Get the frequency of bonds.

		Returns:
			A pair of dictionaries with the frequency of bonds in the molecules.
		"""
		#self._molecule1 = Graph.get_graph_from_file(self._id1)
		#self._molecule2 = Graph.get_graph_from_file(self._id2)
		bonds_frequency = Graph.get_bonds_frequency(self._molecule1,self._molecule2)
		return bonds_frequency

	def mcis(self) -> float:
		"""Get the maximum common induced subgraph.

		Returns:
			The size of the maximum common induced subgraph.
		"""
		g_mcis = Graph.construct_mcis(self._molecule1,self._molecule2)
		
		if g_mcis!= None :
			# Raymond similarity value
			alpha_m = g_mcis.number_of_edges() + g_mcis.number_of_nodes()
			alpha_a = self._molecule1.number_of_edges()+self._molecule1.number_of_nodes()
			alpha_b = self._molecule2.number_of_edges()+self._molecule2.number_of_nodes()
			res = alpha_m * alpha_m  # square
			res /= (alpha_a*alpha_b)
			return res
		return 0.0
