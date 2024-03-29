from argparse import ArgumentParser

from python.api import actions
from python.cli.command import Command


class DistribCommand(Command):
	"""The distribution of set command."""

	def __init__(self, args):
		super().__init__(args)


	@staticmethod
	def parser():
		parser = ArgumentParser(
			prog='DISTRIB',
			description="Show the distribution of molecules in sets",
			usage="Add argument 1 if the type of bound is used, else 0",
			add_help=False
		)
		parser.add_argument('multibound',choices=['0','1'], type=str, help='1 if the type of bound is used, else 0')
		return parser

	def execute(self):

		multibound = self.args.multibound

		distri_info = actions.show_distrib(int(multibound))
		if distri_info["nb_sets"] != 0:
			print("Number of sets :",distri_info["nb_sets"])
			print("Number of molecules :",distri_info["nb_molecules"])
			print("Min size of sets :",min(distri_info["distrib"]))
			print("Max size of sets :",max(distri_info["distrib"]))
		else :
			print("No isomorphism sets in this distribution")


