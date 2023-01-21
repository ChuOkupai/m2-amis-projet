from argparse import ArgumentParser

import python.api.actions as actions
from python.cli.command import Command


class ListIsomorphicSetCommand(Command):
    """The synchronisation command."""

    def __init__(self, args):
        super().__init__(args)


    @staticmethod
    def parser():
        parser = ArgumentParser(
            prog='LIST',
            description="List the isomorphic set, for one molecule please precise the id or name of the molecule",
            usage="List the isomorphic set ",
            add_help=False
        )
        parser.add_argument('-o','--option',dest='molecule_reference', help='the id or name of a molecule',required=False)
        return parser

    def execute(self):
        if(self.args.molecule_reference is not None):

            molecule_reference = self.args.molecule_reference
            list_groupe_isomorphe = actions.list_set_isomorph_mol(molecule_reference)
            print("list of isomorphic groupe for the molecule : ",molecule_reference)
            print("",list_groupe_isomorphe)
        else:
            set_all_isomorphic_groups = actions.list_set_isomorph()
            print("list of all isomorphic sets : ")
            print("",set_all_isomorphic_groups)


