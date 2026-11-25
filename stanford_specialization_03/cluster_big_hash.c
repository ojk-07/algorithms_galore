#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <inttypes.h>
#include <string.h>
#include <time.h>

#include "union_find.h"

/*
Compilieren unter Windows mit MinGW:
gcc -O3 -Wall -Wextra -std=c11 cluster_big_hash.c union_find.c -o cluster_big_hash.exe
*/

/*
 * Die Stanford-Datei clustering_big.txt enthält 24-Bit-Labels.
 */
#define N_BITS 24

/*
 * Load Factor der Hash-Tabelle.
 *
 * Wir wählen die Größe so, dass ungefähr höchstens 70 %
 * der Tabelle belegt werden.
 */
#define HASH_LOAD_FACTOR 0.70


/*
 * Ein Hash-Tabellen-Eintrag.
 *
 * key:
 *     24-Bit-Bitstring, gespeichert als uint32_t.
 *
 * vertex:
 *     Index des zugehörigen Vertex.
 *
 * vertex == -1 bedeutet: Tabellenplatz ist frei.
 */
typedef struct {
    uint32_t key;
    int vertex;
} HashEntry;


/*
 * Hash-Tabelle.
 */
typedef struct {
    HashEntry *entries;
    size_t capacity;
    size_t size;
} HashTable;


/*
 * ------------------------------------------------------------
 * Hash-Funktion
 * ------------------------------------------------------------
 *
 * Wir benutzen eine 32-Bit-Mixing-Funktion.
 *
 * Die 24-Bit-Werte werden dadurch gut über die Hash-Tabelle
 * verteilt.
 */
static uint32_t hash_uint32(uint32_t x)
{
    x ^= x >> 16;
    x *= 0x7feb352dU;
    x ^= x >> 15;
    x *= 0x846ca68bU;
    x ^= x >> 16;

    return x;
}


/*
 * Nächste Zweierpotenz >= n.
 */
static size_t next_power_of_two(size_t n)
{
    size_t result = 1;

    while (result < n) {
        result <<= 1;
    }

    return result;
}


/*
 * ------------------------------------------------------------
 * Hash-Tabelle initialisieren
 * ------------------------------------------------------------
 */
static int hash_init(HashTable *table, size_t expected_elements)
{
    /*
     * Benötigte Kapazität aus dem gewünschten Load Factor.
     */
    size_t required =
        (size_t)((double)expected_elements /
                 HASH_LOAD_FACTOR) + 1;

    table->capacity =
        next_power_of_two(required);

    table->size = 0;

    table->entries =
        malloc(table->capacity * sizeof(HashEntry));

    if (table->entries == NULL) {
        return 1;
    }

    for (size_t i = 0; i < table->capacity; ++i) {
        table->entries[i].vertex = -1;
    }

    return 0;
}


/*
 * Hash-Tabelle freigeben.
 */
static void hash_free(HashTable *table)
{
    free(table->entries);

    table->entries = NULL;
    table->capacity = 0;
    table->size = 0;
}


/*
 * ------------------------------------------------------------
 * Hash Lookup
 * ------------------------------------------------------------
 *
 * Rückgabewert:
 *
 *     >= 0    Vertex wurde gefunden
 *     -1      nicht gefunden
 */
static int hash_find(const HashTable *table, uint32_t key)
{
    size_t mask = table->capacity - 1;

    size_t position =
        hash_uint32(key) & mask;

    while (table->entries[position].vertex != -1) {

        if (table->entries[position].key == key) {
            return table->entries[position].vertex;
        }

        position = (position + 1) & mask;
    }

    return -1;
}


/*
 * ------------------------------------------------------------
 * Hash Insert
 * ------------------------------------------------------------
 *
 * Fügt einen Key ein.
 *
 * Falls der Key bereits vorhanden ist, wird der vorhandene
 * Vertex-Index zurückgegeben.
 *
 * Rückgabewert:
 *
 *     >= 0    bereits vorhandener Vertex
 *     -1      neuer Eintrag wurde eingefügt
 *     -2      Fehler
 */
static int hash_insert(HashTable *table,
                       uint32_t key,
                       int vertex)
{
    size_t mask = table->capacity - 1;

    size_t position =
        hash_uint32(key) & mask;

    while (table->entries[position].vertex != -1) {

        if (table->entries[position].key == key) {
            return table->entries[position].vertex;
        }

        position = (position + 1) & mask;
    }

    table->entries[position].key = key;
    table->entries[position].vertex = vertex;

    table->size++;

    return -1;
}


/*
 * ------------------------------------------------------------
 * Bitstring einer Zeile einlesen
 * ------------------------------------------------------------
 *
 * Beispiel:
 *
 *     0 1 1 0 1 0 ...
 *
 * wird zu:
 *
 *     011010...
 *
 * und anschließend als uint32_t gespeichert.
 */
static int parse_bitstring(const char *line,
                           uint32_t *value)
{
    uint32_t result = 0;
    int bits = 0;

    for (size_t i = 0; line[i] != '\0'; ++i) {

        if (line[i] == '0') {

            result <<= 1;
            bits++;
        }
        else if (line[i] == '1') {

            result <<= 1;
            result |= 1U;
            bits++;
        }
    }

    if (bits != N_BITS) {
        return 1;
    }

    *value = result;

    return 0;
}


/*
 * ------------------------------------------------------------
 * Eingabedatei lesen
 * ------------------------------------------------------------
 *
 * Rückgabe:
 *
 *     values
 *     n_vertices
 *
 * Die erste Zeile der Datei enthält typischerweise:
 *
 *     200000 24
 *
 * und wird daher übersprungen.
 */
static int read_vertices(const char *filename,
                         uint32_t **values,
                         size_t *n_vertices)
{
    FILE *file = fopen(filename, "r");

    if (file == NULL) {
        return 1;
    }


    /*
     * Erste Zeile lesen.
     */
    char line[4096];

    if (fgets(line, sizeof(line), file) == NULL) {
        fclose(file);
        return 1;
    }


    /*
     * Anzahl Vertices aus Header bestimmen.
     *
     * Beispiel:
     *
     *     200000 24
     */
    size_t expected = 0;
    int bits = 0;

    if (sscanf(line, "%zu %d",
               &expected,
               &bits) != 2) {

        fclose(file);
        return 1;
    }


    if (bits != N_BITS) {
        fprintf(stderr,
                "Error: expected %d bits, got %d.\n",
                N_BITS,
                bits);

        fclose(file);
        return 1;
    }


    /*
     * Speicher reservieren.
     */
    uint32_t *data =
        malloc(expected * sizeof(uint32_t));

    if (data == NULL) {
        fclose(file);
        return 1;
    }


    size_t count = 0;


    /*
     * Restliche Zeilen lesen.
     */
    while (fgets(line, sizeof(line), file) != NULL) {

        if (count >= expected) {
            fprintf(stderr,
                    "Error: more vertices than expected.\n");

            free(data);
            fclose(file);

            return 1;
        }


        uint32_t value;

        if (parse_bitstring(line, &value) != 0) {

            fprintf(stderr,
                    "Error parsing vertex at line %zu.\n",
                    count + 2);

            free(data);
            fclose(file);

            return 1;
        }


        data[count] = value;
        count++;
    }


    fclose(file);


    /*
     * Anzahl tatsächlich gelesener Vertices zurückgeben.
     */
    *values = data;
    *n_vertices = count;

    return 0;
}


/*
 * ------------------------------------------------------------
 * Single-Link Clustering für Hamming-Distanz < 3
 * ------------------------------------------------------------
 *
 * Für jeden Vertex v werden erzeugt:
 *
 *     v
 *
 *     v XOR (1 << i)
 *
 *     v XOR (1 << i) XOR (1 << j)
 *
 * für alle i < j.
 *
 * Damit werden alle Bitmuster mit Hamming-Distanz
 *
 *     0, 1 oder 2
 *
 * gefunden.
 */
static size_t clustering_hamming_3(
    const uint32_t *values,
    size_t n_vertices)
{
    /*
     * Union-Find.
     */
    UnionFind uf;

    if (uf_init(&uf, n_vertices) != 0) {
        fprintf(stderr,
                "Error allocating Union-Find.\n");

        return 0;
    }


    /*
     * Anfangs ist jeder Vertex ein eigener Cluster.
     */
    size_t n_clusters = n_vertices;


    /*
     * Hash-Tabelle.
     */
    HashTable table;

    if (hash_init(&table, n_vertices) != 0) {

        fprintf(stderr,
                "Error allocating hash table.\n");

        uf_free(&uf);

        return 0;
    }


    /*
     * --------------------------------------------------------
     * Phase 1:
     *
     * Alle vorhandenen Bitmuster in die Hash-Tabelle eintragen.
     * --------------------------------------------------------
     */
    for (size_t i = 0; i < n_vertices; ++i) {

        int existing =
            hash_insert(&table,
                        values[i],
                        (int)i);

        if (existing >= 0) {

            /*
             * Gleiches Bitmuster bereits vorhanden.
             *
             * Hamming-Distanz = 0.
             */
            int root_i = uf_find(&uf, (int)i);
            int root_e = uf_find(&uf, existing);

            if (root_i != root_e) {

                uf_union(&uf,
                         root_i,
                         root_e);

                n_clusters--;
            }
        }

        if ((i % 10000) == 0) {

            printf("Hashing: %zu / %zu\n",
                   i,
                   n_vertices);
        }
    }


    printf("Hash table contains %zu unique bit patterns.\n",
           table.size);


    /*
     * --------------------------------------------------------
     * Phase 2:
     *
     * Distanz 1 und 2 suchen.
     * --------------------------------------------------------
     */
    for (size_t i = 0; i < n_vertices; ++i) {

        uint32_t value = values[i];


        /*
         * ----------------------------------------------------
         * Hamming-Distanz 1
         * ----------------------------------------------------
         */
        for (int bit1 = 0;
             bit1 < N_BITS;
             ++bit1) {

            uint32_t candidate =
                value ^ (1U << bit1);

            int j =
                hash_find(&table,
                          candidate);

            if (j >= 0) {

                int root_i =
                    uf_find(&uf, (int)i);

                int root_j =
                    uf_find(&uf, j);

                if (root_i != root_j) {

                    uf_union(&uf,
                             root_i,
                             root_j);

                    n_clusters--;
                }
            }
        }


        /*
         * ----------------------------------------------------
         * Hamming-Distanz 2
         * ----------------------------------------------------
         *
         * Genau zwei Bits flippen.
         */
        for (int bit1 = 0;
             bit1 < N_BITS - 1;
             ++bit1) {

            for (int bit2 = bit1 + 1;
                 bit2 < N_BITS;
                 ++bit2) {

                uint32_t candidate =
                    value
                    ^ (1U << bit1)
                    ^ (1U << bit2);

                int j =
                    hash_find(&table,
                              candidate);

                if (j >= 0) {

                    int root_i =
                        uf_find(&uf, (int)i);

                    int root_j =
                        uf_find(&uf, j);

                    if (root_i != root_j) {

                        uf_union(&uf,
                                 root_i,
                                 root_j);

                        n_clusters--;
                    }
                }
            }
        }


        /*
         * Fortschrittsanzeige.
         */
        if ((i % 1000) == 0) {

            printf("Clustering: %zu / %zu, "
                   "clusters = %zu\n",
                   i,
                   n_vertices,
                   n_clusters);
        }
    }


    hash_free(&table);
    uf_free(&uf);

    return n_clusters;
}


/*
 * ------------------------------------------------------------
 * Main
 * ------------------------------------------------------------
 */
int main(void)
{
    const char *file_name =
        "clustering_big.txt";


    printf("\n");
    printf("Single-Link Clustering "
           "using Hamming-distance hashing\n");
    printf("--------------------------------------------------\n");


    /*
     * Zeitmessung starten.
     */
    clock_t tic = clock();


    /*
     * Eingabedaten lesen.
     */
    uint32_t *values = NULL;
    size_t n_vertices = 0;


    printf("\nReading input data...\n");


    if (read_vertices(file_name,
                      &values,
                      &n_vertices) != 0) {

        fprintf(stderr,
                "Error reading input data.\n");

        return EXIT_FAILURE;
    }


    printf("No. of vertices: %zu\n",
           n_vertices);

    printf("Bits per vertex: %d\n",
           N_BITS);


    /*
     * Clustering.
     */
    printf("\n");
    printf("Calculate clustering...\n");


    size_t n_clusters =
        clustering_hamming_3(values,
                             n_vertices);


    /*
     * Ergebnis.
     */
    printf("\n");
    printf("Number of clusters for "
           "minimum distance = 3: %zu\n",
           n_clusters);


    /*
     * Laufzeit.
     */
    clock_t toc = clock();

    double elapsed_ms =
        ((double)(toc - tic)
         / CLOCKS_PER_SEC)
        * 1000.0;


    printf("\n");
    printf("Execution time: %.3f ms\n",
           elapsed_ms);


    /*
     * Speicher freigeben.
     */
    free(values);


    return EXIT_SUCCESS;
}