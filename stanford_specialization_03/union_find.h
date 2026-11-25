#ifndef UNION_FIND_H
#define UNION_FIND_H

#include <stddef.h>

typedef struct {
    int *parents;
    int *ranks;
    size_t size;
} UnionFind;

/* Initialisierung */
int uf_init(UnionFind *uf, size_t n);

/* Freigabe */
void uf_free(UnionFind *uf);

/* Neues Element hinzufügen */
int uf_make_set(UnionFind *uf, int parent, int rank);

/* Repräsentanten einer Menge bestimmen */
int uf_find(UnionFind *uf, int element);

/* Zwei Mengen vereinigen */
void uf_union(UnionFind *uf, int i, int j);

#endif