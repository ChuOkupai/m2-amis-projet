from python.cli.command import Command
from argparse import ArgumentParser
import python.cli.commandfactory as cmds

class HelpCommand(Command):
	"""The help command."""

	def __init__(self, args):
		super().__init__(args)

	@staticmethod
	def parser():
		parser = ArgumentParser(
			prog='HELP',
			description='Prints the list of commands.',
			usage='HELP',
			add_help=False
		)
		return parser

	def execute(self):
		print('Commands list:')
		for cmd in cmds.CommandFactory.commands.values():
			parser = cmd.parser()
			print(f'\t{parser.prog}\t{parser.description}')
