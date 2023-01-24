#define MAXN 1000    /* Define this before including nauty.h */
#include "nisoy.h"   /* which includes <stdio.h> and other system files */
#include "naugroup.h"
int getFullNumber(char* fileName){
    int nbAtoms;
    int links; 
	FILE * f;
   	f = fopen (fileName, "r");

    char buffer[500];
    
    fscanf(f, "%d %d ", &nbAtoms, &links);


   fgets(buffer,499,f);

    int cpt=0;
    int dep=0;
    int Arr=0;
    int test=0;
    while ( fscanf(f, "%d %d %d", &Arr, &dep, &test) != -1 ){  
            cpt = cpt + test;
    }

    fclose(f);

    return nbAtoms+cpt;

}



void genrateGraphFromFile(molecule *X,char* fileName){
    
    X->all= getFullNumber(fileName);
    DYNALLSTAT(graph,g,g_sz); 
    FILE * f;
    char buffer[500];

    f = fopen (fileName, "r");
    
    fscanf(f, "%d %d ", &X->nbAtoms, &X->links);
    fgets(buffer,499,f);

    int m = SETWORDSNEEDED(X->all);

    
    DYNALLOC2(graph,g,g_sz,m,X->all,"malloc");
    EMPTYGRAPH(g,m,X->all);

    int nexa=X->nbAtoms;

    int Arr=0;
    int dep=0;
    int test=0;
    while ( fscanf(f, "%d %d %d", &dep , &Arr , &test) != -1 )  {  
        if(test == 1)
            {                            
                ADDONEEDGE(g,dep-1,nexa,m);
                ADDONEEDGE(g,nexa,Arr-1,m);
                nexa=nexa+1;
            }
        if (test == 2)
            {

                ADDONEEDGE(g,dep-1,nexa,m);
                ADDONEEDGE(g,nexa,Arr-1,m);
                nexa=nexa+1;
                ADDONEEDGE(g,dep-1,nexa,m);
                ADDONEEDGE(g,nexa,Arr-1,m);
                nexa=nexa+1;
            }
        if (test == 3)
            {

                ADDONEEDGE(g,dep-1,nexa,m);
                ADDONEEDGE(g,nexa,Arr-1,m);
                nexa=nexa+1;
                ADDONEEDGE(g,dep-1,nexa,m);
                ADDONEEDGE(g,nexa,Arr-1,m);
                nexa=nexa+1;
                ADDONEEDGE(g,dep-1,nexa,m);
                ADDONEEDGE(g,nexa,Arr-1,m);
                nexa=nexa+1;

            }   
        if (test == 4)
            { 
                                                

                ADDONEEDGE(g,dep-1,nexa,m);
                ADDONEEDGE(g,nexa,Arr-1,m);
                nexa=nexa+1;
                ADDONEEDGE(g,dep-1,nexa,m);
                ADDONEEDGE(g,nexa,Arr-1,m);
                nexa=nexa+1;
                ADDONEEDGE(g,dep-1,nexa,m);
                ADDONEEDGE(g,nexa,Arr-1,m);
                nexa=nexa+1;
                ADDONEEDGE(g,dep-1,nexa,m);
                ADDONEEDGE(g,nexa,Arr-1,m);
                nexa=nexa+1;

            }   
        }
        
    X->adjGraphWithMultLinks=g;

	fclose(f);

}


void genrateGraphFromFileSimpleLinks(molecule *X,char* fileName){
    
    FILE * f;
    char buffer[500];

    f = fopen (fileName, "r");
    
    fscanf(f, "%d %d ", &X->nbAtoms, &X->links);
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



graph* getCanonMultilinks(molecule X){
        int size;
        size=X.all;
        static DEFAULTOPTIONS_GRAPH(options);
        statsblk stats;
        /* Select option for canonical labelling */

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


graph* getCanonSimpleLinks(molecule X){
        int size;
        size=X.nbAtoms;
        static DEFAULTOPTIONS_GRAPH(options);
        statsblk stats;
        /* Select option for canonical labelling */

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


molecule generateMolecule(char* fileName){
    int size;
    molecule X;
    strcpy(X.idChebi,fileName);

    genrateGraphFromFile(&X,fileName);
    genrateGraphFromFileSimpleLinks(&X,fileName);

    X.simpleLink=getCanonMultilinks(X);
    X.multiLink= getCanonSimpleLinks(X);

    X.hashSimpleLinks = malloc(sizeof(char)* X.nbAtoms * 10 );
    X.hashMultiLinks = malloc(sizeof(char)* X.all * 10 );


    hashSimpleLink(X);
    hashMultiLink(X);
    return X;
}

void printMolecule(molecule X){
    printf("\n id CHebi : %s \n",X.idChebi);
    printf(" nombre d'Atoms: %d \n",X.nbAtoms);
    printf(" nombre de liens :%d \n",X.links);
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



void hashSimpleLink(molecule X){
    char *chaine = malloc(sizeof(char)* X.nbAtoms * 10 );
    memset(chaine, 0, sizeof(chaine));
    for (int i = 0; i < X.nbAtoms; i++) {
        char temp[10];
        sprintf(temp, "%X", X.simpleLink[i]);
        strcat(chaine, temp);
    }
    strcpy(X.hashSimpleLinks,chaine);

}

void hashMultiLink(molecule X){
    char *chaine = malloc(sizeof(char)* X.all * 10 );
    memset(chaine, 0, sizeof(chaine));
    for (int i = 0; i < X.all; i++) {
        char temp[10];
        sprintf(temp, "%X", X.multiLink[i]);
        strcat(chaine, temp);
    }
strcpy(X.hashMultiLinks,chaine);
}
