#pragma once
#include "nausparse.h"

typedef struct s_molecule
{
	int nbAtoms;
	int all;
	graph* adjGraph;
	graph* adjGraphWithMultLinks;
	graph* simpleLink;
	graph* multiLink;
	char* hashSimpleLinks;
	char* hashMultiLinks;
}	molecule;

/** Free a molecule structure */
void freeMolecule(molecule* m);

/** Generate a molecule from a file.
 * @param path The path to the file
 * @returns -1 if an error occured, 0 otherwise
 */
int generateMolecule(const char *path);

void printMolecule(molecule X);
