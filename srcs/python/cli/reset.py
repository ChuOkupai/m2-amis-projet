from argparse import ArgumentParser

from python.api import actions
from python.cli.command import Command


class ResetCommand(Command):
	"""The rest command."""

	def __init__(self, args):
		super().__init__(args)


	@staticmethod
	def parser():
		parser = ArgumentParser(
			prog='RESET',
			description="Erase the database, molecule's files and downloaded files",
			usage="RESET programm data",
			add_help=False
		)
		return parser

	def execute(self):
		res = input("Are you sure to reset the database?(y/n) ")
		if res.upper() in ['Y', 'YES']:
			actions.clean()
			print("Programm is reset. Need a synchronisation.")
		else :
			print("Programm is not reset.")