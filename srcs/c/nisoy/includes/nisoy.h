#include <stdbool.h>
#include "nauty.h"

typedef struct molecule
{   
    char idChebi[10];
    int all;
    int nbAtoms;
    int links;
    graph*  adjGraph;
    graph*  adjGraphWithMultLinks;
    graph* simpleLink;
    graph* multiLink;
    char* hashSimpleLinks;
    char* hashMultiLinks;
   
} molecule;

void genrateGraphFromFileSimpleLinks(molecule *X,char* fileName);

void genrateGraphFromFile(molecule *X,char* fileName);

void genrateGraphFromFileSimpleLinks(molecule *X,char* fileName);

graph* getCanonSimpleLinks(molecule X);

graph* getCanonMultilinks(molecule X);

molecule generateMolecule(char* fileName);

void printMolecule(molecule X);

void hashSimpleLink(molecule X);

void hashMultiLink(molecule X);