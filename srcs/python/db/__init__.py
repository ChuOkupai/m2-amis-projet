from python.db.connection import Connection
from python.db.models import *
from python.db.options import *
from python.db.queries import *

# Create the tables if they do not exist
_conn = Connection.get_instance()
_conn.create_tables([Molecule, IsIsomorphic, IsomorphicSet])
_conn.close()
