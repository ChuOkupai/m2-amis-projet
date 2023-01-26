#include "nisoy.h"

int main(int ac, char **av) {
	if (ac != 2) {
		printf("Usage: %s <path>\n", av[0]);
		return 1;
	}
	return generateMolecule(av[1]) < 0;
}
