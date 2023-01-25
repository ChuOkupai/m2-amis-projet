#include "nisoy.h"   /* which includes <stdio.h> and other system files */
#include "naugroup.h"
#include "utils.h"

static const char *getErrorMessage(t_error_code code) {
	static const char *m[] = {
		"Success",
		"Invalid atom",
		"Invalid format",
		"Invalid link",
		"Invalid number of atoms",
		"Invalid number of nbLinks"
	};
	return m[code];
}

/** Handles an error while parsing a file.
 * @param f The file
 * @param msg The error message
 * @returns -1
*/
static int parseError(FILE *f, const t_error_code code) {
	if (f)
		fclose(f);
	fprintf(stderr, "Error: %s\n", getErrorMessage(code));
	return -1;
}

static int freeEdgesCache(t_edge *edges, size_t *neighborsIndex, sparsegraph *g) {
	free(edges);
	free(neighborsIndex);
	SG_FREE(*g);
	return -1;
}

/** Loads graph from file.
 * @param f The file
 * @param edgesCount The number of edges
 * @returns -1 if an error occured, 0 otherwise
*/
static int loadGraph(FILE *f, sparsegraph *g) {
	size_t ne = g->nde / 2;
	t_edge *edges = malloc(ne * sizeof(t_edge));
	size_t *neighborsIndex = malloc(g->nv * sizeof(size_t));
	if (!edges || !neighborsIndex)
		return freeEdgesCache(edges, neighborsIndex, g);
	SG_ALLOC(*g, g->nv, g->nde, "malloc");
	bzero(g->d, g->dlen * sizeof(int));
	for (size_t i = 0; i < ne; ++i) {
		t_edge *e = edges + i;
		if (fscanf(f, "%hd %hd %hhd", &e->from, &e->to, &e->type) < 3
		|| e->from < 1 || e->to < 1 || e->type < 1 || e->type > 8)
			return freeEdgesCache(edges, neighborsIndex, g);
		++g->d[e->from - 1];
		++g->d[e->to - 1];
	}
	if (g->vlen) {
		g->v[0] = 0;
		neighborsIndex[0] = 0;
	}
	for (size_t i = 1; i < g->nv; ++i) {
		g->v[i] = g->v[i - 1] + g->d[i - 1];
		neighborsIndex[i] = g->v[i];
	}
	for (size_t i = 0; i < ne; ++i) {
		t_edge *e = edges + i;
		g->e[neighborsIndex[e->from - 1]++] = e->to - 1;
		g->e[neighborsIndex[e->to - 1]++] = e->from - 1;
	}
	free(edges);
	free(neighborsIndex);
	return 0;
}

static getCanonicalGraph(sparsegraph *g) {
	DYNALLSTAT(int,lab,lab_sz);
	DYNALLSTAT(int,ptn,ptn_sz);
	DYNALLSTAT(int,orbits,orbits_sz);
	static DEFAULTOPTIONS_SPARSEGRAPH(options);
	statsblk stats;
	int n = g->nv, m;
	options.getcanon = TRUE;
	m = SETWORDSNEEDED(n);
	nauty_check(WORDSIZE,m,n,NAUTYVERSIONID);
	DYNALLOC1(int,lab,lab_sz,n,"malloc");
	DYNALLOC1(int,ptn,ptn_sz,n,"malloc");
	DYNALLOC1(int,orbits,orbits_sz,n,"malloc");
	SG_DECL(cg);
	sparsenauty(g,lab,ptn,orbits,&options,&stats,&cg);
	put_sg(stdout,g, 1, 1);
	DYNFREE(lab,lab_sz);
	DYNFREE(ptn,ptn_sz);
	DYNFREE(orbits,orbits_sz);
}

/*
static void generateGraphFromFileSimpleLinks(molecule *X,char* fileName){
	
	FILE * f;
	char buffer[500];

	f = fopen (fileName, "r");
	
	fscanf(f, "%d %d ", &X->nbAtoms, &X->nbLinks);
	fgets(buffer,499,f);

	int m = SETWORDSNEEDED(X->nbAtoms);

	DYNALLSTAT(graph,g,g_sz); 

	DYNALLOC2(graph,g,g_sz,m,X->nbAtoms,"malloc");
	EMPTYGRAPH(g,m,X->nbAtoms);


	int Arr=0;
	int dep=0;
	int test=0;
	while ( fscanf(f, "%d %d %d", &Arr, &dep, &test) != -1 )  {  
		ADDONEEDGE(g,dep-1,Arr-1,m);
		}
	X->adjGraph=g;
	fclose(f);

}

static graph* getCanonMultiLinks(molecule X){
		int size;
		size=X.all;
		static DEFAULTOPTIONS_GRAPH(options);
		statsblk stats;

		options.getcanon = TRUE;
		
		DYNALLSTAT(int,lab,lab_sz); // Lab2 et ptn pour le coloriage du graphe 1
		DYNALLSTAT(int,ptn,ptn_sz);
		DYNALLSTAT(int,orbits,orbits_sz); // un tableau d'orbits



		DYNALLOC1(int,lab,lab_sz,size,"malloc");
		DYNALLOC1(int,ptn,ptn_sz,size,"malloc");
		DYNALLOC1(int,orbits,orbits_sz,size,"malloc");

		DYNALLSTAT(graph,cg,cg_sz);
		DYNALLOC2(graph,cg,cg_sz,size,SETWORDSNEEDED(size),"malloc");

		

		densenauty(X.adjGraphWithMultLinks,lab,ptn,orbits,&options,&stats,SETWORDSNEEDED(size),size,cg);

		return cg;
}


static graph* getCanonSimpleLinks(molecule X){
		int size;
		size=X.nbAtoms;
		static DEFAULTOPTIONS_GRAPH(options);
		statsblk stats;

		options.getcanon = TRUE;
		
		DYNALLSTAT(int,lab,lab_sz); // Lab2 et ptn pour le coloriage du graphe 1
		DYNALLSTAT(int,ptn,ptn_sz);
		DYNALLSTAT(int,orbits,orbits_sz); // un tableau d'orbits



		DYNALLOC1(int,lab,lab_sz,size,"malloc");
		DYNALLOC1(int,ptn,ptn_sz,size,"malloc");
		DYNALLOC1(int,orbits,orbits_sz,X.all,"malloc");


		int m=SETWORDSNEEDED(size);
		DYNALLSTAT(graph,cg,cg_sz);
		DYNALLOC2(graph,cg,cg_sz,size,m,"malloc");
		printf(" \n taille  =:  %d \n",cg_sz);

		densenauty(X.adjGraph,lab,ptn,orbits,&options,&stats,m,size,cg);
		printf(" \n  la taille est : %d \n et le m est %d \n",cg_sz,m);

		return cg;
}

static void hashSimpleLink(molecule X){
	char *chaine = malloc(sizeof(char)* X.nbAtoms * 10 );
	memset(chaine, 0, sizeof(chaine));
	for (int i = 0; i < X.nbAtoms; i++) {
		char temp[10];
		sprintf(temp, "%X", X.simpleLink[i]);
		strcat(chaine, temp);
	}
	strcpy(X.hashSimpleLinks,chaine);
	free(chaine);

}

static void hashMultiLink(molecule X){
	char *chaine = malloc(sizeof(char)* X.all * 10 );
	memset(chaine, 0, sizeof(chaine));
	for (int i = 0; i < X.all; i++) {
		char temp[10];
		sprintf(temp, "%X", X.multiLink[i]);
		strcat(chaine, temp);
	}
	strcpy(X.hashMultiLinks,chaine);
	free(chaine);
}
*/
void freeMolecule(molecule *m) {
	/* TODO: free graph using nauty utilities */
	free(m->hashSimpleLinks);
	free(m->hashMultiLinks);
}

int generateMolecule(const char *path) {
	FILE *f = fopen(path, "r");
	if (!f)
		return -1;
	SG_DECL(g);
	if (fscanf(f, "%d %d", &g.nv, &g.nde) < 2)
		return parseError(f, INVALID_FORMAT);
	if (g.nv < 1)
		return parseError(f, INVALID_NB_ATOMS);
	if (g.nde < 0)
		return parseError(f, INVALID_NB_LINKS);
	g.nde *= 2;
	fscanf(f, "\n%*[^\n]\n"); // skip atoms line
	if (loadGraph(f, &g))
		return parseError(f, INVALID_FORMAT);
	fclose(f);
	put_sg(stdout, &g, 1, 80);
	getCanonicalGraph(&g);
	return 0;
}
/*
void printMolecule(molecule X){
	printf(" nombre d'Atoms: %d \n",X.nbAtoms);
	printf(" nombre de liens :%d \n",X.nbLinks);
	printf(" son graph canonique :  \n");

	for (int k = 0; k < X.nbAtoms; ++k) {
		printf(" %X ",X.simpleLink[k]);
	}
	
	printf(" \n son graph canonique avec modelisation des liaisons mutiples :  \n");

	printf(" %X  ",X.multiLink);
	for (int k = 0; k < X.all ; ++k) {
			printf("  %X   ",X.multiLink[k]);

	}

	hashSimpleLink(X);
	hashMultiLink(X);

	printf("\n\n%s", X.hashMultiLinks);
	printf("\n\n%s", X.hashSimpleLinks);    

}
*/
