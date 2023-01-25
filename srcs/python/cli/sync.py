from argparse import ArgumentParser

import python.api.actions as actions
from python.cli.command import Command


class SyncCommand(Command):
    """The synchronisation command."""

    def __init__(self, args):
        super().__init__(args)

    @staticmethod
    def parser():
        parser = ArgumentParser(
            prog='SYNC',
            description='Synchronize the local database with the online database.',
            usage='SYNCHRONIZATION',
            add_help=False
        )
        return parser

    def execute(self):
            nb_mol = actions.sync_database()
            if (nb_mol>0): print(nb_mol," has been updated")
            else : print("The database is already updated")
        
