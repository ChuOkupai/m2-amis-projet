from argparse import ArgumentParser

from python.api import actions
from python.cli.command import Command
from python.cli.exceptions import InvalidTableError


class CompareCommand(Command):
	"""The compare command."""

	def __init__(self, args):
		super().__init__(args)


	@staticmethod
	def parser():
		parser = ArgumentParser(
			prog='COMPARE',
			description='Compare two molecules.',
			usage='Give the references for two molecules ; option -m=1 for mcis',
			add_help=False
		)
		parser.add_argument('molecule1_id', help='the ref of the first molecule')
		parser.add_argument('molecule2_id', help='the ref of the second molecule')
		parser.add_argument('-m', '--mcis', dest='option', help='for the additional command mcis', default='0', choices=['0','1'])
		return parser

	def execute(self):
		mol1_ref = self.args.molecule1_id
		mol2_ref = self.args.molecule2_id
		molecule1=actions.find(mol1_ref)
		molecule2=actions.find(mol2_ref)
		if molecule2 == None or molecule2==None:
			raise InvalidTableError(mol1_ref+" "+mol2_ref)
		atoms_frequency, bonds_frequency = actions.compare_frequency(molecule1.id, molecule2.id)
		if (self.args.option =='1'):
			g_mcis, mcis_value = actions.get_mcis(molecule1.id, molecule2.id)

		print("comparisons between molecule ",mol1_ref ," and molecule ",mol2_ref, " : ")
		print("atoms frequency :",atoms_frequency)
		print("bonds frequency :",bonds_frequency)

		if (self.args.option =='1'):
			print("maximum subgraph ratio :", mcis_value)
			actions.show_mcis(g_mcis)


