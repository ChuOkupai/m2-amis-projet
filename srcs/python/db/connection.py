from peewee import SqliteDatabase
from python.common import constants

class Connection:
	_instance = None

	@staticmethod
	def get_instance():
		"""Get the database connection instance.

		Returns:
			SqliteDatabase: The database connection instance.
		"""
		if Connection._instance is None:
			Connection._instance = SqliteDatabase(constants.DB_PATH)
		return Connection._instance
