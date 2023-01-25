from python.datamining.graph import Graph
from scipy.stats import chi2

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
		return self.khi2(atoms_frequency)

	def get_bonds_frequency(self):
		"""Get the frequency of bonds.

		Returns:
			A pair of dictionaries with the frequency of bonds in the molecules.
		"""
		bonds_frequency = Graph.get_bonds_frequency(self._molecule1,self._molecule2)
		return self.khi2(bonds_frequency)

	def khi2(self, distr) -> tuple:
		"""Get the distributions.

		Returns:
			A value from the cumulative distribution function of chi2.
		"""
		distr1 = distr["count"][0]
		distr2 = distr["count"][1]
		assert len(distr1.keys()) == len(distr2.keys())
		ddl = len(distr1.keys())-1
		if ddl > 0: # If many value to compare
			sum = 0.0
			suminv = 0.0
			count1 = 0
			count2 = 0
			count1inv = 0
			count2inv = 0
			for k in distr1.keys():
				if distr1[k] != 0:
					count1 += distr1[k]
					count2 += distr2[k]
				if distr2[k] != 0:
					count1inv += distr1[k]
					count2inv += distr2[k]
			for k in distr1.keys():
				if distr1[k] != 0:
					res = (distr2[k]/count2 - distr1[k]/count1)
					res *= res
					res /= distr1[k]/count1
					sum += res
				if distr2[k] != 0:
					res = (distr1[k]/count1inv - distr2[k]/count2inv)
					res *= res
					res /= (distr2[k]/count2inv)
					suminv += res
			return (1- chi2.cdf(sum, ddl),1- chi2.cdf(suminv, ddl))
		else : # If one value to compare
			k1 = distr1.keys()
			k2 = distr2.keys()
			if k1[0] == k2[0]:
				return (1.0,0.0)
			return (0.0,0.0)

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
