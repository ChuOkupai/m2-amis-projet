class CommandNotFoundError(Exception):
	"""The command not found error, raised when the command name is invalid."""

	def __init__(self, name):
		"""Initialize the command not found error.

		Args:
			name: The command name.
		"""
		super().__init__(f'{name}: Command not found')

class InvalidCommandError(Exception):
	"""The invalid command error, raised when the arguments are invalid."""
 
	def __init__(self, name):
		"""Initialize the invalid command error.
		
		Args:
			name: The command name.
		"""
		super().__init__(f'{name}: Invalid arguments')


class InvalidMoleculeError(Exception):
	"""The invalid command error, raised when the arguments are invalid."""
 
	def __init__(self, name):
		"""Initialize the invalid command error.
		
		Args:
			name: The command name.
		"""
		super().__init__(f'{name}: Invalid arguments')