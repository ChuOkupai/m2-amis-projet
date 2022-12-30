from python.cli.command import Command
from argparse import ArgumentParser, SUPPRESS
from typing import List

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
