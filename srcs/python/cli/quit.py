from argparse import ArgumentParser

from python.cli.command import Command


class QuitCommand(Command):
	"""The exit command."""

	def __init__(self, args):
		super().__init__(args)

	@staticmethod
	def parser():
		parser = ArgumentParser(
			prog='QUIT',
			description='Exits the application.',
			add_help=False)
		return parser

	def execute(self) -> int:
		return 0
