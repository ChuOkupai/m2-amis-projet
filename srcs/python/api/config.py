from python.common import constants

import json
from os.path import exists
from parser import ParserError

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
			IOError: If the file cannot be opened. TODO : problem in test to catch error instead of exception
			ParseError: If the file cannot be parsed.
		"""
		jsonFile = None
		# TODO: Complete the test. Illegal keys and values should be ignored.
		try :
			if exists(path) :
				jsonFile = open(path, "r")
			else :
				raise FileNotFoundError
			data = json.load(jsonFile)
			for key, param in data.items():
				if not isinstance(param, dict):
					raise ParserError
				Config._params[key] = ParamValue(type(param["value"]), param["default"], param["value"])
		except (FileNotFoundError, OSError) :
			raise Exception("IOError") from None
		except (ParserError, KeyError, Exception):
			raise Exception("ParserError")
		finally :
			if jsonFile:
				jsonFile.close()

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
		if key in Config._params.keys():
			return Config._params.get(key)
		else :
			raise Exception("KeyError")

	@staticmethod
	def save():
		"""Saves the configuration to the configuration file in JSON format.

		Raises:
			IOError: If the file cannot be opened.
		"""
		try :
			jsonFile = open(constants.CONFIG_PATH, "w")
		except (OSError, Exception):
			raise Exception("IOError")
		else :
			data = {}
			for key, param in Config._params.items():
				data[key] = {"default": param.default, "value": param.value}
			json.dump(data, jsonFile)
			jsonFile.close()
		

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
		if key in Config._params.keys():
			old_param = Config._params.get(key)
			if isinstance(value, old_param.type):
				Config._params[key] = ParamValue(type=type(value), default=old_param.default, value=value)
			else : 
				raise Exception("TypeError")
		else :
			raise Exception("KeyError")
