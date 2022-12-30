from python.common import constants

class ParamValue:
	"""A configuration parameter value."""

	def __init__(self, type: type, default: object, value: object):
		"""Creates a configuration parameter.

		Args:
			type: The type of the parameter.
			default: The default value of the parameter.
			value: The value of the parameter.
		"""
		self.type = type
		self.default = default
		self.value = value

class Config:
	"""Configuration class for the API."""
	_params = {}

	@staticmethod
	def load(path=constants.CONFIG_PATH):
		"""Loads the configuration from the configuration file in JSON format.

		Raises:
			IOError: If the file cannot be opened.
			ParseError: If the file cannot be parsed.
		"""
		# TODO: Load the configuration from path. Illegal keys and values should be ignored.

	def all() -> dict:
		"""Gets all configuration parameters.

		Returns:
			A dictionary of all configuration parameters.
		"""
		return Config._params

	@staticmethod
	def get(key: str) -> ParamValue:
		"""Gets a configuration parameter.

		Args:
			key: The key of the parameter.

		Returns:
			The value of the parameter.

		Raises:
			KeyError: If the key is not found.
		"""
		# TODO: Return the value of the parameter.
		return ""

	@staticmethod
	def save():
		"""Saves the configuration to the configuration file in JSON format.

		Raises:
			IOError: If the file cannot be opened.
		"""
		# TODO: Save the configuration to CONFIG_PATH.

	@staticmethod
	def set(key: str, value: object):
		"""Sets a configuration parameter.

		Args:
			key: The key of the parameter.
			value: The value of the parameter.

		Raises:
			KeyError: If the key is not found.
			TypeError: If the type of the value is not correct.
		"""
		# TODO: Set the value of the parameter.
