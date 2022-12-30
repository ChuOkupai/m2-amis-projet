"""Models used in the database."""

from peewee import BooleanField, CharField, CompositeKey, ForeignKeyField, IntegerField, Model
from python.db.connection import Connection

class BaseModel(Model):
	"""A base model that will use our SQLite database."""

	class Meta:
		"""Meta class for the base model."""
		database = Connection.get_instance()

class Molecule(BaseModel):
	"""A molecule."""
	name = CharField(64)
	formula = CharField(128)
	nb_atoms = IntegerField()
	hash = CharField(64)

class IsomorphicSet(BaseModel):
	"""A set of isomorphic molecules."""
	hydrogen = BooleanField()
	mult_bound = BooleanField()
	nauty_sign = CharField(128)
	partition = CharField(256)

class IsIsomorphic(BaseModel):
	"""A relationship between a molecule and a set of isomorphic molecules."""
	id_mol = ForeignKeyField(Molecule)
	id_set = ForeignKeyField(IsomorphicSet)

	class Meta:
		"""Meta class for the is_isomorphic table."""
		primary_key = CompositeKey('id_mol', 'id_set')
