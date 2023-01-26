from argparse import ArgumentParser
from pprint import pprint

from python.api import actions
from python.cli.command import Command
from tabulate import tabulate


class SearchCommand(Command):
	"""The search command."""

	def __init__(self, args):
		super().__init__(args)


	@staticmethod
	def parser():
		parser = ArgumentParser(
			prog='SEARCH',
			description="Search molecules which contains the argument string",
			usage="Give part of the molecule's name",
			add_help=False
		)
		parser.add_argument('molecule_reference', type=str, help="part of the molecule's name")
		return parser

	def execute(self):

		molecule_reference = self.args.molecule_reference

		molecule_info = actions.search(molecule_reference)
		print("List for : ", molecule_reference, '['+str(len(molecule_info))+']')
		print(tabulate(molecule_info, headers="keys"))
		if len(molecule_info) > 100:
			pprint(molecule_info[:100])
			print("Stop with the 100th molecules")


