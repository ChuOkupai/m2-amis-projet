#pragma once
#include "nausparse.h"

/** Generate a molecule from a file.
 * @param path The path to the file
 * @returns -1 if an error occured, 0 otherwise
 */
int generateMolecule(const char *path);
