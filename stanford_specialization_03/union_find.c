#include "union_find.h"
#include <stdlib.h>

/*
 * Initialisiert eine Union-Find-Datenstruktur mit n Elementen.
 *
 * Die Elemente werden intern mit 1 ... n bezeichnet,
 * entsprechend der Python-Implementierung.
 */
int uf_init(UnionFind *uf, size_t n)
{
    uf->parents = malloc(n * sizeof(int));
    uf->ranks   = malloc(n * sizeof(int));

    if (uf->parents == NULL || uf->ranks == NULL) {
        free(uf->parents);
        free(uf->ranks);
        uf->parents = NULL;
        uf->ranks = NULL;
        uf->size = 0;
        return 1;
    }

    uf->size = n;

    for (size_t i = 0; i < n; ++i) {
        uf->parents[i] = (int)i + 1;
        uf->ranks[i] = 0;
    }

    return 0;
}


/*
 * Gibt die Union-Find-Datenstruktur frei.
 */
void uf_free(UnionFind *uf)
{
    free(uf->parents);
    free(uf->ranks);

    uf->parents = NULL;
    uf->ranks = NULL;
    uf->size = 0;
}


/*
 * Fügt ein neues Element hinzu.
 *
 * parent == -1:
 *     Das neue Element wird sein eigener Parent.
 */
int uf_make_set(UnionFind *uf, int parent, int rank)
{
    size_t n = uf->size;

    int *new_parents =
        realloc(uf->parents, (n + 1) * sizeof(int));

    int *new_ranks =
        realloc(uf->ranks, (n + 1) * sizeof(int));

    if (new_parents == NULL || new_ranks == NULL) {
        return 1;
    }

    uf->parents = new_parents;
    uf->ranks = new_ranks;

    if (parent == -1) {
        uf->parents[n] = (int)n + 1;
    } else {
        uf->parents[n] = parent;
    }

    uf->ranks[n] = rank;
    uf->size++;

    return 0;
}


/*
 * Bestimmt den Repräsentanten der Menge.
 *
 * Zusätzlich wird Path Compression durchgeführt.
 */
int uf_find(UnionFind *uf, int element)
{
    int s = element;

    /* Zunächst zur Wurzel laufen */
    while (uf->parents[s - 1] != s) {
        s = uf->parents[s - 1];
    }

    /* Path Compression */
    int e = element;

    while (uf->parents[e - 1] != e) {
        int next = uf->parents[e - 1];
        uf->parents[e - 1] = s;
        e = next;
    }

    return s;
}


/*
 * Vereinigt die Mengen, zu denen i und j gehören.
 *
 * Union by Rank.
 */
void uf_union(UnionFind *uf, int i, int j)
{
    int si = uf_find(uf, i);
    int sj = uf_find(uf, j);

    int ri = uf->ranks[si - 1];
    int rj = uf->ranks[sj - 1];

    if (ri > rj) {
        /* Menge sj wird unter si gehängt */
        uf->parents[sj - 1] = si;
    }
    else if (ri == rj) {
        /* Menge si wird unter sj gehängt */
        uf->parents[si - 1] = sj;
        uf->ranks[sj - 1]++;
    }
    else {
        /* Menge si wird unter sj gehängt */
        uf->parents[si - 1] = sj;
    }
}