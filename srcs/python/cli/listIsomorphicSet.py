from argparse import ArgumentParser

import python.api.actions as actions
from python.cli.command import Command
from tabulate import tabulate

class ListIsomorphicSetCommand(Command):
	"""The synchronisation command."""

	def __init__(self, args):
		super().__init__(args)


	@staticmethod
	def parser():
		parser = ArgumentParser(
			prog='LIST',
			description="List the isomorphic set, for one molecule please precise the id or name of the molecule",
			usage="List the isomorphic sets ;\n\t -m='mol_ref' list the isomorph sets of a molecule ;\n\t -s='set_id' list the molecules of the set ",
			add_help=False
		)
		parser.add_argument('-m','--molecule',dest='molecule_reference', help='the id or name of a molecule',required=False)
		parser.add_argument('-s','--set',dest='set_id', help='the id of a set of isomorphs',required=False)
		return parser

	def execute(self):
		if(self.args.molecule_reference is not None and self.args.set_id is None):
			molecule_reference = self.args.molecule_reference
			list_set_isomorphe = actions.list_set_isomorph_of_mol(molecule_reference)
			if len(list_set_isomorphe)>0:
				print("List of isomorphic groupe for the molecule",molecule_reference, ':')
				print(tabulate(list_set_isomorphe, headers="keys"))
			else :
				print("No isomorphic set for the molecule",molecule_reference)
		elif(self.args.molecule_reference is None and self.args.set_id is not None):
			set_id = self.args.set_id
			lsit_molecules = actions.list_mol_of_set_isomorph(set_id)
			if len(lsit_molecules)>0:
				print("List of molecule for the set id",set_id, ':')
				print(tabulate(lsit_molecules, headers="keys"))
			else :
				print("No molecule for the isomorphic set",set_id)
		else:
			list_all_isomorphic_sets = actions.list_set_isomorph()
			if len(list_all_isomorphic_sets)>0:
				print("List of all isomorphic sets : ")
				print(tabulate(list_all_isomorphic_sets, headers="keys"))
			else :
				print("No isomorphic set in database")


