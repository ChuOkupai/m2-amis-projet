from os.path import join

import matplotlib.pyplot as plt
import networkx as nx
from python.common.constants import MOLECULES_PATH
from python.common.element_color import ELEMENTS


def _labels_match(n1_attrib,n2_attrib):
	"""Compare two nodes attributes label.

	Args:
		n1_attrib: The attributs of the first node.
		n2_attrib: The attributs of the second node.

	Returns:
		False if either does not have a label or if the labels do not match.
	"""
	try:
		return n1_attrib['label']==n2_attrib['label']
	except KeyError:
		print('Error in labels_match')
		return False

def _edge_match(e1_attrib,e2_attrib):
	"""Compare two edges attributes weight.

	Args:
		e1_attrib: The attributs of the first edge.
		e2_attrib: The attributs of the second edge.

	Returns:
		False if either does not have a weight or if the weight do not match.
	"""
	try:
		return e1_attrib['weight']==e2_attrib['weight']
	except KeyError:
		print('Error in edge_col_match')
		return False

class Graph:
	def get_graph_from_file(id_mol : int)-> nx:
		try :
			with open(join(MOLECULES_PATH,str(id_mol)+".txt"), 'r') as f:
				n_atoms, n_edges = map(int, f.readline().strip().split())
				atoms = f.readline().strip().split()

				# create an empty graph
				G = nx.Graph()

				node_colors = []
				# add nodes to the graph
				for i in range(n_atoms):
					G.add_node(i+1, label=atoms[i])
					node_colors.append(ELEMENTS.get(atoms[i]))

				# add edges to the graph
				for i in range(n_edges):
					a, b, weight = f.readline().strip().split()
					G.add_edge(int(a), int(b), weight=weight)

				return G, node_colors
		except (Exception, FileNotFoundError) as e:
			raise e

	def get_colors(G : nx.Graph):
		node_colors = []
		for node in G.nodes():
			elem = G.nodes[node]["label"]
			node_colors.append(ELEMENTS.get(elem))
		return node_colors

	def show_mol(G, node_colors=None):
		"""Show the graph G with matplotlib.

		Args:
			G (nx.Graph): The graph representing the molecule.
		"""
		plt.clf()
		pos = nx.spring_layout(G)
		node_labels = nx.get_node_attributes(G, 'label')
		edge_labels = nx.get_edge_attributes(G, 'weight')
		nx.draw_networkx_nodes(G, pos, node_color=node_colors, edgecolors='#000000')
		nx.draw_networkx_edges(G, pos, edge_color='#000000')
		nx.draw_networkx_labels(G, pos, labels=node_labels)
		nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
		plt.show()
		

	def show_mols(G1, G2, node_colors1=None, node_colors2=None):
		pos1 = nx.spring_layout(G1)
		pos2 = nx.spring_layout(G2)
		node_labels1 = nx.get_node_attributes(G1, 'label')
		node_labels2 = nx.get_node_attributes(G2, 'label')
		edge_labels1 = nx.get_edge_attributes(G1, 'weight')
		edge_labels2 = nx.get_edge_attributes(G2, 'weight')

		plt.figure(figsize=(10,5))
		plt.clf()
		plt.subplot(121)
		nx.draw_networkx_nodes(G1, pos1, node_color=node_colors1, edgecolors='#000000')
		nx.draw_networkx_edges(G1, pos1, edge_color='#000000')
		nx.draw_networkx_labels(G1, pos1, labels=node_labels1)
		nx.draw_networkx_edge_labels(G1, pos1, edge_labels=edge_labels1)

		plt.subplot(122)
		nx.draw_networkx_nodes(G2, pos2, node_color=node_colors2, edgecolors='#000000')
		nx.draw_networkx_edges(G2, pos2, edge_color='#000000')
		nx.draw_networkx_labels(G2, pos2, labels=node_labels2)
		nx.draw_networkx_edge_labels(G2, pos2, edge_labels=edge_labels2)
		plt.show()
		
	
	def get_atoms_frequency(G1, G2) -> dict:
		"""Get the frequency of atoms in two graphs G1 and G2.

		Args:
			G1 (nx.Graph): The first graph representing the molecule.
			G2 (nx.Graph): The second graph representing the molecule.

		Returns:
			A dictionary with the frequency of atoms in the molecules.
		"""
		# Get the list of atoms in each graph
		d_atoms1 = nx.get_node_attributes(G1, 'label')
		d_atoms2 = nx.get_node_attributes(G2, 'label')
		atoms1 = []
		atoms2 = []
		elements = []
		for k, value in d_atoms1.items():
			atoms1.append(value)
			if value not in elements:
				elements.append(value)
		for k, value in d_atoms2.items():
			atoms2.append(value)
			if value not in elements:
				elements.append(value)
		
		# dict of effectif
		atoms_count1 = {}
		atoms_count2 = {}
		for e in elements:
			atoms_count1[e] = atoms1.count(e)
			atoms_count2[e] = atoms2.count(e)

		# Normalize the counts to get the frequencies
		total_atoms1 = len(atoms1)
		total_atoms2 = len(atoms2)
		
		atoms_frequency1 = {}
		atoms_frequency2 = {}
		for atom, count in atoms_count1.items():
			atoms_frequency1[atom] = count/ total_atoms1
		for atom, count in atoms_count2.items():
			atoms_frequency2[atom] = count/total_atoms2

		return {'count':[atoms_count1,atoms_count2], 'frequencies':[atoms_frequency1, atoms_frequency2]}

	def get_bonds_frequency(G1, G2) -> dict:
		"""Get the frequency of bonds in two graphs G1 and G2.

		Args:
			G1 (nx.Graph): The first graph representing the molecule.
			G2 (nx.Graph): The second graph representing the molecule.

		Returns:
			A dictionary with the frequency of atoms in the molecules.
		"""
		# Get the list of bonds in each graph
		d_bonds1 = nx.get_edge_attributes(G1, 'weight')
		d_bonds2 = nx.get_edge_attributes(G2, 'weight')
		bonds1 = []
		bonds2 = []
		weight = []
		for k, value in d_bonds1.items():
			bonds1.append(value)
			if value not in weight:
				weight.append(value)
		for k, value in d_bonds2.items():
			bonds2.append(value)
			if value not in weight:
				weight.append(value)
		
		# dict of effectif
		bonds_count1 = {}
		bonds_count2 = {}
		for w in weight:
			bonds_count1[w] = bonds1.count(w)
			bonds_count2[w] = bonds2.count(w)

		# Normalize the counts to get the frequencies
		total_bonds1 = len(bonds1)
		total_bonds2 = len(bonds2)
		
		bonds_frequency1 = {}
		bonds_frequency2 = {}
		for bond, count in bonds_count1.items():
			bonds_frequency1[bond] = count/ total_bonds1
		for bond, count in bonds_count2.items():
			bonds_frequency2[bond] = count/total_bonds2

		return {'count':[bonds_count1,bonds_count2], 'frequencies':[bonds_frequency1, bonds_frequency2]}
	
	def construct_mcis(G1, G2):
		""" Construct the MCIS graph for 2 graphes.

		Args:
			G1 (nx.Graph): The first graph representing the molecule.
			G2 (nx.Graph): The second graph representing the molecule.

		Returns:
			The Maximum Common induced Subgraph or None.
		"""
		# Use ISMAGS isomorphisme algorithm
		ismags = nx.isomorphism.ISMAGS(G1,G2,node_match=_labels_match, edge_match=_edge_match)
		# extract MCIS from ISMAG result
		largest_common_sub = list(ismags.largest_common_subgraph())
		
		if(largest_common_sub != []):
			# construct the MCIS
			ls_nodes_mcis = largest_common_sub[0].keys()
			g_mcis = G1.subgraph(ls_nodes_mcis)
			return g_mcis
		# if there is no MCIS
		return None

