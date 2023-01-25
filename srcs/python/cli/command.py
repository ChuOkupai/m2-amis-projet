from abc import ABC, abstractmethod
from argparse import ArgumentParser

from python.cli.exceptions import InvalidCommandError


class Command(ABC):
	"""The base class for all commands."""

	def __init__(self, args):
		"""Initializes the command.

		The arguments are parsed and stored in self.args as a argparse.Namespace object.
		If the arguments are invalid, an explicit error is printed to the standard error
		and an exception is raised.

		Args:
			args: The splitted arguments from the command line.

		Raises:
			InvalidCommandError: If the arguments are invalid.
		"""
		try:
			self.args = self.parser().parse_args(args[1:])
		except SystemExit:
			raise InvalidCommandError(args[0])

	@staticmethod
	@abstractmethod
	def parser() -> ArgumentParser:
		"""Returns the argument parser for the command.

		Returns:
			The argument parser.
		"""
		pass

	@abstractmethod
	def execute(self) -> int:
		"""Executes the command.

		Returns:
			The exit code of the command.
		"""
		pass
