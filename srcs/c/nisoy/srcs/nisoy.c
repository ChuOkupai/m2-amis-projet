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

/** Loads the edges of a molecule from a file.
 * @param f The file
 * @param edgesCount The expected number of edges
 * @returns The edges or NULL if an error occured
*/
static t_edge *loadEdges(FILE *f, size_t edgesCount) {
	t_edge *edges = malloc(edgesCount * sizeof(t_edge)), *e;
	if (!edges)
		return NULL;
	for (size_t i = 0; i < edgesCount; ++i) {
		e = edges + i;
		if (fscanf(f, "%hd %hd %hhd", &e->from, &e->to, &e->type) < 3
		|| e->from < 1 || e->to < 1 || e->type < 1 || e->type > 8) {
			free(edges);
			break ;
		}
		--e->from, --e->to, --e->type;
	}
	return edges;
}

/** Construct a graph from an array of edges.
 * @param g The graph
 * @param edges The edges
 * @returns -1 if an error occured, 0 otherwise
*/
static int constructGraph(sparsegraph *g, t_edge *edges) {
	size_t *neighborsIndex = malloc(g->nv * sizeof(size_t));
	if (!neighborsIndex)
		return -1;
	SG_ALLOC(*g, g->nv, g->nde, "malloc");
	bzero(g->d, g->dlen * sizeof(*g->d));
	for (size_t i = 0; i < g->nde / 2; ++i) {
		++g->d[edges[i].from];
		++g->d[edges[i].to];
	}
	if (g->vlen) {
		g->v[0] = 0;
		neighborsIndex[0] = 0;
	}
	for (int i = 1; i < g->nv; ++i) {
		g->v[i] = g->v[i - 1] + g->d[i - 1];
		neighborsIndex[i] = g->v[i];
	}
	for (size_t i = 0; i < g->nde / 2; ++i) {
		g->e[neighborsIndex[edges[i].from]++] = edges[i].to;
		g->e[neighborsIndex[edges[i].to]++] = edges[i].from;
	}
	free(neighborsIndex);
	return 0;
}

/** Construct a graph from an array of edges considering bounds.
 * @param g The graph
 * @param edges The edges
 * @returns -1 if an error occured, 0 otherwise
*/
static int constructGraphWithBounds(sparsegraph *g, t_edge *edges) {
	static const int avTable[] = { 0, 1, 2, 3, 1, 3, 3, 1 };
	size_t av = 0; /* Additional vertices */
	size_t ae = 0; /* Additional edges */
	for (size_t i = 0; i < g->nde / 2; ++i) {
		av += avTable[edges[i].type];
		ae += 4 * avTable[edges[i].type];
	}
	int nv = g->nv, nde = g->nde;
	size_t *neighborsIndex = malloc(nv * sizeof(size_t));
	if (!neighborsIndex)
		return -1;
	SG_ALLOC(*g, nv + av, nde + ae, "malloc");
	bzero(g->d, g->dlen * sizeof(*g->d));
	for (int i = 0; i < nde / 2; ++i) {
		int avi = avTable[edges[i].type];
		if (!avi)
			avi = 1;
		g->d[edges[i].from] += avi;
		g->d[edges[i].to] += avi;
	}
	for (int i = nv; i < g->nv; ++i)
		g->d[i] = 2;
	if (g->vlen) {
		g->v[0] = 0;
		neighborsIndex[0] = 0;
	}
	for (int i = 1; i < g->nv; ++i) {
		g->v[i] = g->v[i - 1] + g->d[i - 1];
		if (i < nv)
			neighborsIndex[i] = g->v[i];
	}
	for (int i = 0, j = g->nde - 2 * av, k = nv; i < nde / 2; ++i) {
		int avi = avTable[edges[i].type];
		if (avi) {
			while (avi--) {
				g->e[neighborsIndex[edges[i].from]++] = k;
				g->e[neighborsIndex[edges[i].to]++] = k;
				g->e[j++] = edges[i].from;
				g->e[j++] = edges[i].to;
			}
		} else {
			g->e[neighborsIndex[edges[i].from]++] = edges[i].to;
			g->e[neighborsIndex[edges[i].to]++] = edges[i].from;
		}
	}
	free(neighborsIndex);
	return 0;
}

/** Outputs the canonical form of a molecule.
 * @param g The graph of the molecule
*/
static void serializeGraph(const sparsegraph *g) {
	printf("%d,%lu", g->nv, g->nde);
	for (int i = 0; i < g->nv; ++i)
		printf(",%d", g->d[i]);
	for (int i = 0; i < g->nv; ++i)
		printf(",%lu", g->v[i]);
	for (size_t i = 0; i < g->nde; ++i)
		printf(",%d", g->e[i]);
	putchar('\n');
}

/** Gets the canonical form of a graph.
 * @param g The graph
*/
static void getCanonicalGraph(sparsegraph *g) {
	DYNALLSTAT(int, lab, lab_sz);
	DYNALLSTAT(int, ptn, ptn_sz);
	DYNALLSTAT(int, orbits, orbits_sz);
	static DEFAULTOPTIONS_SPARSEGRAPH(options);
	statsblk stats;
	int n = g->nv, m;
	options.getcanon = TRUE;
	m = SETWORDSNEEDED(n);
	nauty_check(WORDSIZE, m, n, NAUTYVERSIONID);
	DYNALLOC1(int, lab, lab_sz, n, "malloc");
	DYNALLOC1(int, ptn, ptn_sz, n, "malloc");
	DYNALLOC1(int, orbits, orbits_sz, n, "malloc");
	SG_DECL(cg);
	sparsenauty(g, lab, ptn, orbits, &options, &stats, &cg);
	DYNFREE(lab, lab_sz);
	DYNFREE(ptn, ptn_sz);
	DYNFREE(orbits, orbits_sz);
	serializeGraph(&cg);
	SG_FREE(cg);
}

int generateMolecule(const char *path) {
	FILE *f = fopen(path, "r");
	if (!f)
		return -1;
	SG_DECL(g);
	if (fscanf(f, "%d %lu", &g.nv, &g.nde) < 2)
		return parseError(f, INVALID_FORMAT);
	if (g.nv < 1)
		return parseError(f, INVALID_NB_ATOMS);
	g.nde *= 2;
	fscanf(f, "\n%*[^\n]\n"); // skip atoms line
	t_edge *edges = loadEdges(f, g.nde / 2);
	fclose(f);
	if (!edges)
		return parseError(f, INVALID_FORMAT);
	if (constructGraph(&g, edges)) {
		free(edges);
		return parseError(f, INVALID_FORMAT);
	}
	getCanonicalGraph(&g);
	SG_FREE(g);
	if (constructGraphWithBounds(&g, edges)) {
		free(edges);
		return parseError(f, INVALID_FORMAT);
	}
	getCanonicalGraph(&g);
	SG_FREE(g);
	free(edges);
	return 0;
}
