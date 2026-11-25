#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "union_find.h"

/*
Compilieren unter Windows mit MinGW:
gcc -O2 -Wall -Wextra -std=c11 cluster_big.c union_find.c -o cluster_big.exe
*/


/*
 * Ein Vertex besteht aus einer Folge von Bytes.
 */
typedef struct {
    unsigned char *data;
    size_t nbytes;
} Vertex;


/*
 * Ein für das Clustering verwendetes Edge.
 */
typedef struct {
    int v;
    int w;
} Edge;


/*
 * Speicher für einen Vertex freigeben.
 */
void free_vertex(Vertex *v)
{
    free(v->data);
    v->data = NULL;
    v->nbytes = 0;
}


/*
 * Hamming-Distanz zweier Vertices.
 *
 * Die Python-Version berechnet:
 *
 *     c = bytes(x ^ y for x, y in zip(...))
 *     d = sum(x.bit_count() for x in c)
 *
 * Da beide Bitcodes dieselbe Länge haben, können wir direkt
 * die XOR-Bytes bilden und deren gesetzte Bits zählen.
 */
int hamming_distance(const Vertex *a, const Vertex *b)
{
    int distance = 0;

    size_t n = a->nbytes;

    if (b->nbytes < n) {
        n = b->nbytes;
    }

    for (size_t i = 0; i < n; ++i) {
        unsigned char x = a->data[i] ^ b->data[i];

        /*
         * Anzahl gesetzter Bits in einem Byte.
         */
        while (x != 0) {
            distance += x & 1;
            x >>= 1;
        }
    }

    return distance;
}


/*
 * Liest die Bitcodes aus der Eingabedatei.
 *
 * Die erste Zeile wird wie im Python-Programm übersprungen.
 *
 * Beispiel:
 *
 *     24  0 1 0 0 0 ...
 *
 * Die Leerzeichen werden entfernt.
 */
int read_list(const char *file_name,
             Vertex **vertices,
             size_t *n_vertices)
{
    FILE *file = fopen(file_name, "r");

    if (file == NULL) {
        return 1;
    }

    *vertices = NULL;
    *n_vertices = 0;

    char line[10000];

    /*
     * Erste Zeile überspringen.
     */
    if (fgets(line, sizeof(line), file) == NULL) {
        fclose(file);
        return 1;
    }

    while (fgets(line, sizeof(line), file) != NULL) {

        /*
         * Länge der Bitfolge bestimmen.
         */
        size_t bit_count = 0;

        for (size_t i = 0; line[i] != '\0'; ++i) {
            if (line[i] == '0' || line[i] == '1') {
                bit_count++;
            }
        }

        if (bit_count == 0) {
            continue;
        }

        /*
         * Anzahl Bytes:
         *
         * (bit_count + 7) / 8
         */
        size_t nbytes = (bit_count + 7) / 8;

        unsigned char *data =
            calloc(nbytes, sizeof(unsigned char));

        if (data == NULL) {
            fclose(file);
            return 1;
        }

        /*
         * Bitfolge in Bytes umwandeln.
         *
         * Die Python-Version verwendet byteorder='big'.
         */
        size_t bit_index = 0;

        for (size_t i = 0; line[i] != '\0'; ++i) {

            if (line[i] != '0' && line[i] != '1') {
                continue;
            }

            if (line[i] == '1') {

                size_t byte_index = bit_index / 8;
                size_t bit_in_byte = 7 - (bit_index % 8);

                data[byte_index] |=
                    (unsigned char)(1u << bit_in_byte);
            }

            bit_index++;
        }

        /*
         * Vertex hinzufügen.
         */
        Vertex *tmp =
            realloc(*vertices,
                    (*n_vertices + 1) * sizeof(Vertex));

        if (tmp == NULL) {
            free(data);
            fclose(file);
            return 1;
        }

        *vertices = tmp;

        (*vertices)[*n_vertices].data = data;
        (*vertices)[*n_vertices].nbytes = nbytes;

        (*n_vertices)++;
    }

    fclose(file);

    return 0;
}


/*
 * Single-Link Clustering mit Hamming-Distanzen.
 *
 * min_dist:
 *     Ziel-Mindestabstand.
 *
 * vertices:
 *     Array der Vertices.
 *
 * n_vertices:
 *     Anzahl der Vertices.
 *
 * n_clusters:
 *     Rückgabe: Anzahl der Cluster.
 *
 * T:
 *     Rückgabe: verwendete Merge-Kanten.
 *
 * n_edges:
 *     Rückgabe: Anzahl der Merge-Kanten.
 */
int slc_hamming(int min_dist,
                const Vertex *vertices,
                size_t n_vertices,
                size_t *n_clusters,
                Edge **T,
                size_t *n_edges)
{
    /*
     * Speicher für die Merge-Kanten.
     *
     * Maximal n_vertices - 1 Kanten können einen Baum bilden.
     */
    Edge *edges = NULL;

    if (n_vertices > 1) {
        edges = malloc((n_vertices - 1) * sizeof(Edge));

        if (edges == NULL) {
            return 1;
        }
    }

    /*
     * Union-Find initialisieren.
     *
     * Die Python-Version benutzt:
     *
     *     parents = [1, 2, ..., n]
     *     ranks   = [0, 0, ..., 0]
     */
    UnionFind uf;

    if (uf_init(&uf, n_vertices) != 0) {
        free(edges);
        return 1;
    }

    *n_clusters = n_vertices;
    *n_edges = 0;

    /*
     * Alle möglichen Paare von Vertices durchlaufen.
     *
     * Python:
     *
     *     i = 0
     *     while i < len(vertices) - 1:
     *
     *         j = i + 1
     *         while j < len(vertices):
     */
    for (size_t i = 0; i < n_vertices - 1; ++i) {

        printf("i = %zu, #clusters = %zu\n",
               i, *n_clusters);

        for (size_t j = i + 1;
             j < n_vertices;
             ++j) {

            /*
             * Hamming-Distanz berechnen.
             */
            int d =
                hamming_distance(&vertices[i],
                                 &vertices[j]);

            /*
             * Python verwendet:
             *
             *     if d < min_dist:
             */
            if (d < min_dist) {

                /*
                 * Python:
                 *
                 *     si = u.find(i)
                 *     sj = u.find(j)
                 *
                 * Da Python hier intern 1-basierte Union-Find-
                 * Elemente verwendet, müssen wir i und j um 1
                 * erhöhen.
                 */
                int si = uf_find(&uf, (int)i + 1);
                int sj = uf_find(&uf, (int)j + 1);

                if (si != sj) {

                    /*
                     * Cluster vereinigen.
                     */
                    uf_union(&uf,
                             si,
                             sj);

                    /*
                     * Edge speichern.
                     *
                     * Die Vertex-Nummerierung bleibt 0-basiert,
                     * wie im Python-Programm T.append((i,j)).
                     */
                    edges[*n_edges].v = (int)i;
                    edges[*n_edges].w = (int)j;

                    (*n_edges)++;

                    /*
                     * Anzahl Cluster reduzieren.
                     */
                    (*n_clusters)--;
                }
            }
        }
    }

    uf_free(&uf);

    *T = edges;

    return 0;
}


/*
 * Speicher für alle Vertices freigeben.
 */
void free_vertices(Vertex *vertices,
                   size_t n_vertices)
{
    if (vertices == NULL) {
        return;
    }

    for (size_t i = 0; i < n_vertices; ++i) {
        free_vertex(&vertices[i]);
    }

    free(vertices);
}


/*
 * Hauptprogramm.
 */
int main(void)
{
    /*
     * Testdateien:
     *
     * const char *file_name = "test-hamming-01.txt";
     * const char *file_name = "test-hamming-02.txt";
     */

    const char *file_name = "clustering_big.txt";

    /*
     * Ziel-Mindestdistanz.
     */
    int min_dist = 3;

    /*
     * Startzeit messen.
     */
    clock_t tic = clock();

    printf("\n");
    printf("Reading input data for Single-Link Clustering.\n");

    /*
     * Eingabedaten lesen.
     */
    Vertex *vertices = NULL;
    size_t n_vertices = 0;

    int status =
        read_list(file_name,
                  &vertices,
                  &n_vertices);

    if (status != 0) {
        printf("Error reading input data, stop.\n");
        return EXIT_FAILURE;
    }

    printf("No. of vertices: %zu\n",
           n_vertices);

    printf("\n");
    printf("Calculate clustering.\n");

    /*
     * Single-Link Clustering.
     */
    size_t n_clusters = 0;
    Edge *T = NULL;
    size_t n_edges = 0;

    status =
        slc_hamming(min_dist,
                    vertices,
                    n_vertices,
                    &n_clusters,
                    &T,
                    &n_edges);

    if (status != 0) {
        printf("Error calculating clustering.\n");

        free_vertices(vertices,
                      n_vertices);

        return EXIT_FAILURE;
    }

    /*
     * Ergebnis ausgeben.
     */
    printf("\n");
    printf("Number of clusters for minimum distance = %d: %zu\n",
           min_dist,
           n_clusters);

    /*
     * T wird im ursprünglichen Python-Programm nicht ausgegeben.
     */

    /*
     * Laufzeit.
     */
    clock_t toc = clock();

    double elapsed_ms =
        ((double)(toc - tic) / CLOCKS_PER_SEC) * 1000.0;

    printf("\n");
    printf("Execution time: %.3f ms\n",
           elapsed_ms);

    /*
     * Speicher freigeben.
     */
    free(T);

    free_vertices(vertices,
                  n_vertices);

    return EXIT_SUCCESS;
}