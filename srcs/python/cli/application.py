from python.api import Config
from python.cli.commandfactory import CommandFactory, CommandNotFoundError
from python.cli.command import InvalidCommandError
import readline, sys

class Application:
	"""The main application class."""

	def __init__(self, args):
		"""Initializes the application.

		Args:
			args: The arguments from the command line.

		Options:
			-c <path>: The path to the configuration file.
			-e <commands>: Execute the commands and exit.
			-h: Print the help message and exit.
			-v: Print the version and exit. 
 
		Raises:
			IOError: If the configuration file cannot be opened.
			ParseError: If the configuration file cannot be parsed.
		"""
		Config.load()
		readline.set_auto_history(True)
		# TODO: Parse the arguments from args. Command line options still has to be defined.

	def _parse_and_execute(self, args):
		"""Parses the line and executes the command.

		Args:
			args: The splitted arguments from the command line including the command name.

		Returns:
			The exit code of the command.
		"""
		try:
			command = CommandFactory.create(args)
			if command is None:
				return 0
			return command.execute()
		except CommandNotFoundError as e:
			print(e, file=sys.stderr)
			return None
		except InvalidCommandError as e:
			return 1

	def run(self):
		"""Runs the application.
		While running, the application will prompt the user for commands and execute them.
		On EOF (Ctrl+D) or when the user types 'quit', the application will exit.

		Returns:
			The exit code of the application.
		"""
		print('Type "help" for a list of commands.', file=sys.stderr)
		while True:
			args = input('> ').split()
			r = self._parse_and_execute(args)
			if len(args) > 0 and args[0].upper() == 'QUIT' and r == 0:
				break
		return 0
