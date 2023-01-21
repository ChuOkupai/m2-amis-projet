from python.cli.command import Command
from python.cli.comparecommand import CompareCommand
from python.cli.exceptions import CommandNotFoundError
from python.cli.find import FindCommand
from python.cli.help import HelpCommand
from python.cli.listIsomorphicSet import ListIsomorphicSetCommand
from python.cli.quit import QuitCommand
from python.cli.sync import SyncCommand


class CommandFactory:
	"""The command factory."""

	commands = {
		'HELP': HelpCommand,
		'QUIT': QuitCommand,
		'SYNC': SyncCommand,
		'COMPARE' : CompareCommand,
		'FIND': FindCommand,
		'LIST' : ListIsomorphicSetCommand
	}

	@staticmethod
	def create(args) -> Command:
		"""Create a command from the given arguments.

		Args:
			args: The splitted arguments from the command line (including the command name)

		Returns:
			The command to execute or None if the command name is empty.

		Raises:
			CommandNotFoundError: If the command name is invalid.
			InvalidCommandError: If the arguments are invalid.
		"""
		if len(args) == 0:
			return None
		name = args[0]
		args[0] = args[0].upper()
		if args[0] in CommandFactory.commands:
			return CommandFactory.commands[args[0]](args)
		raise CommandNotFoundError(name)
