#include "includes/nisoy.h"

int main(int ac, char **av) {
	if (ac != 2) {
		printf("Usage: %s <file>\n", av[0]);
		return 1;
	}
	int r = generateMolecule(av[1]);
	printf("r = %d\n", r);
	//printMolecule(&m);
	return 0;
}
