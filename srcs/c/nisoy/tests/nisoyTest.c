#define MAXN 1000    /* Define this before including nauty.h */
#include "nisoy.h"

int main(int argc, char *argv[]){
    
    molecule X;

    X=generateMolecule(argv[1]);
    
    printMolecule(X);

    
    exit(1);
}







