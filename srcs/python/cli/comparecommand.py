from argparse import ArgumentParser
from pprint import pprint

from python.api import actions
from python.cli.command import Command
from python.cli.exceptions import InvalidMoleculeError


class CompareCommand(Command):
    """The synchronisation command."""

    def __init__(self, args):
        super().__init__(args)


    @staticmethod
    def parser():
        parser = ArgumentParser(
            prog='COMPARE',
            description='Compare two molecules.',
            usage='compare two molecules in different ways',
            add_help=False
        )
        parser.add_argument('molecule1_id', help='the id of the first molecule')
        parser.add_argument('molecule2_id', help='the id of the second molecule')
        parser.add_argument('-o', '--option', dest='option', help='for the additional command mcis', default=None, choices=['mcis'])
        return parser

    def execute(self):
        mol1_ref = self.args.molecule1_id
        mol2_ref = self.args.molecule2_id
        molecule1=actions.find(mol1_ref)
        molecule2=actions.find(mol2_ref)
        if molecule2 == None or molecule2==None:
            raise InvalidMoleculeError(mol1_ref+" "+mol2_ref)
        atoms_frequency, bonds_frequency = actions.compare_frequency(molecule1.id, molecule2.id)
        if (self.args.option =='mcis'):
            mcis = actions.get_mcis(molecule1.id, molecule2.id)

        print("comparisons between molecule ",mol1_ref ," and molecule ",mol2_ref, " : ")
        print("atoms frequency :",atoms_frequency)
        print("bonds frequency :",bonds_frequency)

        if (self.args.option =='mcis'):
            print("maximum subgraph ratio :", mcis)


