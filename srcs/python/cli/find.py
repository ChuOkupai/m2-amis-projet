from argparse import ArgumentParser

from python.api import actions
from python.cli.command import Command


class FindCommand(Command):
    """The synchronisation command."""

    def __init__(self, args):
        super().__init__(args)


    @staticmethod
    def parser():
        parser = ArgumentParser(
            prog='FIND',
            description="Get a molecule's informations",
            usage="Get a molecule's informations",
            add_help=False
        )
        parser.add_argument('molecule_reference', help='the id or name of the molecule')
        return parser

    def execute(self):

        molecule_reference = self.args.molecule_reference

        molecule_info = actions.find(molecule_reference)
        print("molecule id : ",molecule_info.id)
        print("molecule name : ",molecule_info.name)
        print("number of atoms : ",molecule_info.nb_atoms)


