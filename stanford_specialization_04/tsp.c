#include <errno.h>
#include <inttypes.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

/*
 * C port of the supplied Python TSP program.
 *
 * Input formats (first line is the number of cities):
 *   x y       (cities are assigned IDs 1..n by row order)
 *   id x y    (coordinates are stored by explicit ID)
 *
 * Exact Held-Karp dynamic programming is used for n <= 27; the
 * nearest-neighbour heuristic is used for n > 27, matching the Python code.

 Compile on Windows with:
 gcc -O3 -std=c11 -Wall -Wextra tsp.c -lm -o tsp.exe
 */

typedef struct { double x, y; } Point;

static double elapsed_seconds(struct timespec start, struct timespec end) {
    return (double)(end.tv_sec - start.tv_sec) +
           1e-9 * (double)(end.tv_nsec - start.tv_nsec);
}

static double distance_between(const Point *p, int i, int j) {
    double dx = p[i].x - p[j].x;
    double dy = p[i].y - p[j].y;
    return sqrt(dx * dx + dy * dy);
}

static long long read_line(char **line, size_t *cap, FILE *fp)
{
    size_t len = 0;
    int ch;

    if (*line == NULL || *cap == 0) {
        *cap = 256;
        *line = malloc(*cap);
        if (*line == NULL)
            return -2;
    }

    while ((ch = fgetc(fp)) != EOF) {
        if (len + 1 >= *cap) {
            size_t new_cap = *cap * 2;
            char *tmp = realloc(*line, new_cap);
            if (tmp == NULL)
                return -2;

            *line = tmp;
            *cap = new_cap;
        }

        (*line)[len++] = (char)ch;

        if (ch == '\n')
            break;
    }

    if (len == 0 && ch == EOF)
        return -1;

    (*line)[len] = '\0';
    return (long long)len;
}

static int read_cities(const char *filename, Point **points_out, int *n_out) {
    FILE *fp = fopen(filename, "r");
    if (!fp) {
        fprintf(stderr, "Cannot open '%s': %s\n", filename, strerror(errno));
        return 0;
    }

    char *line = NULL;
    size_t cap = 0;
    ssize_t len;
    int n = 0;
    do {
        len = read_line(&line, &cap, fp);
    } while (len >= 0 && line[0] == '\0');

    if (len < 0) {
        fprintf(stderr, "Input file is empty.\n");
        free(line); fclose(fp); return 0;
    }
    char *endptr;
    errno = 0;
    long nl = strtol(line, &endptr, 10);
    if (errno || endptr == line || nl < 1 || nl > 1000000) {
        fprintf(stderr, "Invalid city count on first line.\n");
        free(line); fclose(fp); return 0;
    }
    n = (int)nl;
    Point *points = calloc((size_t)n + 1, sizeof(*points));
    unsigned char *seen = calloc((size_t)n + 1, sizeof(*seen));
    if (!points || !seen) {
        fprintf(stderr, "Not enough memory for city coordinates.\n");
        free(points); free(seen); free(line); fclose(fp); return 0;
    }

    int row = 0, format_cols = 0;
    while ((len = read_line(&line, &cap, fp)) >= 0) {
        char *p = line;
        while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') ++p;
        if (*p == '\0') continue;

        double a, b, c;
        char extra;
        int fields = sscanf(p, "%lf %lf %lf %c", &a, &b, &c, &extra);
        if (fields != 2 && fields != 3) {
            fprintf(stderr, "Invalid data on city row %d.\n", row + 1);
            free(points); free(seen); free(line); fclose(fp); return 0;
        }
        if (format_cols == 0) format_cols = fields;
        if (fields != format_cols) {
            fprintf(stderr, "Mixed input formats: expected %d fields per city row.\n", format_cols);
            free(points); free(seen); free(line); fclose(fp); return 0;
        }

        int id;
        double x, y;
        if (fields == 2) {
            id = row + 1;
            x = a; y = b;
        } else {
            double rounded = nearbyint(a);
            if (!isfinite(a) || fabs(a - rounded) > 1e-9 || rounded < 1 || rounded > n) {
                fprintf(stderr, "Invalid city ID on row %d.\n", row + 1);
                free(points); free(seen); free(line); fclose(fp); return 0;
            }
            id = (int)rounded;
            x = b; y = c;
        }
        if (id < 1 || id > n || seen[id]) {
            fprintf(stderr, "City ID %d is out of range or duplicated.\n", id);
            free(points); free(seen); free(line); fclose(fp); return 0;
        }
        if (!isfinite(x) || !isfinite(y)) {
            fprintf(stderr, "Non-finite coordinate for city %d.\n", id);
            free(points); free(seen); free(line); fclose(fp); return 0;
        }
        points[id] = (Point){x, y};
        seen[id] = 1;
        ++row;
    }

    if (row != n) {
        fprintf(stderr, "City count mismatch: header says %d, found %d rows.\n", n, row);
        free(points); free(seen); free(line); fclose(fp); return 0;
    }
    for (int i = 1; i <= n; ++i) {
        if (!seen[i]) {
            fprintf(stderr, "Missing city ID %d.\n", i);
            free(points); free(seen); free(line); fclose(fp); return 0;
        }
    }

    free(seen); free(line); fclose(fp);
    *points_out = points;
    *n_out = n;
    return 1;
}

static void print_tour(const int *tour, int n) {
    for (int i = 0; i <= n; ++i)
        printf("%s%d", i ? " " : "", tour[i]);
    putchar('\n');
}

static int nearest_neighbour(const Point *points, int n, double *length_out,
                             int **tour_out) {
    int *tour = malloc(((size_t)n + 1) * sizeof(*tour));
    unsigned char *visited = calloc((size_t)n + 1, sizeof(*visited));
    if (!tour || !visited) {
        fprintf(stderr, "Not enough memory for heuristic.\n");
        free(tour); free(visited); return 0;
    }
    if (n == 0) { *length_out = 0.0; *tour_out = tour; free(visited); return 1; }
    if (n == 1) { tour[0] = tour[1] = 1; *length_out = 0.0; *tour_out = tour; free(visited); return 1; }

    struct timespec tic, toc;
    clock_gettime(CLOCK_MONOTONIC, &tic);
    double length = 0.0;
    int current = 1;
    tour[0] = current;
    visited[current] = 1;
    int stride = n > 100 ? n / 100 : 1;

    for (int iteration = 1; iteration < n; ++iteration) {
        double best_d2 = INFINITY;
        int best_city = -1;
        for (int q = 1; q <= n; ++q) {
            if (visited[q]) continue;
            double dx = points[q].x - points[current].x;
            double dy = points[q].y - points[current].y;
            double d2 = dx * dx + dy * dy;
            if (d2 < best_d2) {
                best_d2 = d2;
                best_city = q;
            }
        }
        if (best_city < 0) {
            fprintf(stderr, "Internal error in nearest-neighbour search.\n");
            free(tour); free(visited); return 0;
        }
        length += sqrt(best_d2);
        current = best_city;
        visited[current] = 1;
        tour[iteration] = current;

        if (n <= 100 || iteration % stride == 0 || iteration == n - 1) {
            clock_gettime(CLOCK_MONOTONIC, &toc);
            printf("iter = %d, city = %d, length = %.3f, dt = %.3f s\n",
                   iteration, current, length, elapsed_seconds(tic, toc));
        }
    }
    length += distance_between(points, current, 1);
    tour[n] = 1;
    free(visited);
    *length_out = length;
    *tour_out = tour;
    return 1;
}

static size_t choose_size(int n, int k) {
    if (k < 0 || k > n) return 0;
    if (k > n - k) k = n - k;
    size_t result = 1;
    for (int i = 1; i <= k; ++i) {
        /* For n <= 27, this multiplication is safe in size_t. */
        result = result * (size_t)(n - k + i) / (size_t)i;
    }
    return result;
}

static int exact_tsp(const Point *points, int n, double *length_out,
                     int **tour_out) {
    if (n > 27) {
        fprintf(stderr, "Exact solver is configured for at most 27 cities.\n");
        return 0;
    }
    int *tour = malloc(((size_t)n + 1) * sizeof(*tour));
    if (!tour) { fprintf(stderr, "Not enough memory for tour.\n"); return 0; }
    if (n == 0) { *length_out = 0.0; *tour_out = tour; return 1; }
    if (n == 1) { tour[0] = tour[1] = 1; *length_out = 0.0; *tour_out = tour; return 1; }

    struct timespec tic, toc;
    clock_gettime(CLOCK_MONOTONIC, &tic);

    double *D = calloc(((size_t)n + 1) * ((size_t)n + 1), sizeof(*D));
    if (!D) { fprintf(stderr, "Not enough memory for distance matrix.\n"); free(tour); return 0; }
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= n; ++j)
            if (i != j) D[(size_t)i * (n + 1) + j] = distance_between(points, i, j);

    const size_t mask_count = (size_t)1 << (n - 1);
    const size_t c_count = mask_count * (size_t)(n - 1);
    if (c_count > SIZE_MAX / sizeof(uint8_t)) {
        fprintf(stderr, "Predecessor matrix size overflows size_t.\n");
        free(D); free(tour); return 0;
    }
    uint8_t *C = calloc(c_count, sizeof(*C));
    int32_t *row_lookup = malloc(mask_count * sizeof(*row_lookup));
    if (!C || !row_lookup) {
        fprintf(stderr, "Not enough memory for exact-solver predecessor/lookup arrays.\n");
        free(D); free(C); free(row_lookup); free(tour); return 0;
    }
    for (size_t i = 0; i < mask_count; ++i) row_lookup[i] = -1;

    double *A = NULL;
    size_t prev_rows = 0;
    int prev_width = 0;

    for (int m = 2; m <= n; ++m) {
        int width = m - 1;
        size_t n_subsets = choose_size(n - 1, width);
        if (n_subsets > SIZE_MAX / (size_t)width / sizeof(int) ||
            n_subsets > SIZE_MAX / (size_t)width / sizeof(double)) {
            fprintf(stderr, "DP layer size overflows size_t.\n");
            free(A); free(D); free(C); free(row_lookup); free(tour); return 0;
        }
        int *subsets = malloc(n_subsets * (size_t)width * sizeof(*subsets));
        double *A_new = malloc(n_subsets * (size_t)width * sizeof(*A_new));
        if (!subsets || !A_new) {
            fprintf(stderr, "Not enough memory for DP layer m=%d.\n", m);
            free(subsets); free(A_new); free(A); free(D); free(C); free(row_lookup); free(tour); return 0;
        }

        /* Generate lexicographically ordered combinations of cities 2..n. */
        int *comb = malloc((size_t)width * sizeof(*comb));
        if (!comb) {
            fprintf(stderr, "Not enough memory for combination generator.\n");
            free(subsets); free(A_new); free(A); free(D); free(C); free(row_lookup); free(tour); return 0;
        }
        for (int i = 0; i < width; ++i) comb[i] = i + 2;
        size_t row = 0;
        for (;;) {
            for (int j = 0; j < width; ++j)
                subsets[row * (size_t)width + j] = comb[j];
            ++row;
            int pos = width - 1;
            while (pos >= 0 && comb[pos] == n - width + pos + 1) --pos;
            if (pos < 0) break;
            ++comb[pos];
            for (int j = pos + 1; j < width; ++j) comb[j] = comb[j - 1] + 1;
        }
        free(comb);

        for (row = 0; row < n_subsets; ++row) {
            size_t mask = 0;
            for (int j_col = 0; j_col < width; ++j_col) {
                int city = subsets[row * (size_t)width + j_col];
                mask |= (size_t)1 << (city - 2);
            }
            row_lookup[mask] = (int32_t)row;

            for (int j_col = 0; j_col < width; ++j_col) {
                int j = subsets[row * (size_t)width + j_col];
                size_t prev_mask = mask & ~((size_t)1 << (j - 2));
                size_t c_index = mask * (size_t)(n - 1) + (size_t)(j - 2);
                if (prev_mask == 0) {
                    A_new[row * (size_t)width + j_col] = D[(size_t)1 * (n + 1) + j];
                    C[c_index] = 1;
                } else {
                    int32_t prev_row = row_lookup[prev_mask];
                    if (prev_row < 0 || (size_t)prev_row >= prev_rows) {
                        fprintf(stderr, "Internal error: missing previous DP row.\n");
                        free(subsets); free(A_new); free(A); free(D); free(C); free(row_lookup); free(tour); return 0;
                    }
                    double best = INFINITY;
                    int best_k = 0;
                    for (int k_col = 0; k_col < width; ++k_col) {
                        if (k_col == j_col) continue;
                        int k = subsets[row * (size_t)width + k_col];
                        int prev_col = k_col - (j_col < k_col ? 1 : 0);
                        double candidate = A[(size_t)prev_row * (size_t)prev_width + (size_t)prev_col]
                                         + D[(size_t)k * (n + 1) + j];
                        if (candidate < best) { best = candidate; best_k = k; }
                    }
                    A_new[row * (size_t)width + j_col] = best;
                    C[c_index] = (uint8_t)best_k;
                }
            }
        }

        clock_gettime(CLOCK_MONOTONIC, &toc);
        printf("m = %d, #subsets = %zu, #calcs = %zu, dt = %.3f s\n",
               m, n_subsets, (size_t)width * (size_t)width * n_subsets,
               elapsed_seconds(tic, toc));
        free(subsets);
        free(A);
        A = A_new;
        prev_rows = n_subsets;
        prev_width = width;
    }

    size_t all_mask = mask_count - 1;
    int32_t last_row = row_lookup[all_mask];
    if (last_row < 0) {
        fprintf(stderr, "Internal error: full subset was not generated.\n");
        free(A); free(D); free(C); free(row_lookup); free(tour); return 0;
    }
    double best_length = INFINITY;
    int last_city = -1;
    for (int j = 2; j <= n; ++j) {
        double candidate = A[(size_t)last_row * (size_t)prev_width + (size_t)(j - 2)]
                         + D[(size_t)j * (n + 1) + 1];
        if (candidate < best_length) { best_length = candidate; last_city = j; }
    }

    /* Reconstruct the tour backwards using C[subset_mask, last_city]. */
    tour[n] = 1;
    tour[n - 1] = last_city;
    size_t mask = all_mask;
    int current = last_city;
    int pos = n - 1;
    while (mask != 0) {
        size_t c_index = mask * (size_t)(n - 1) + (size_t)(current - 2);
        int predecessor = C[c_index];
        mask &= ~((size_t)1 << (current - 2));
        current = predecessor;
        --pos;
        tour[pos] = current;
    }

    free(A); free(D); free(C); free(row_lookup);
    *length_out = best_length;
    *tour_out = tour;
    return 1;
}

int main(int argc, char **argv) {
    const char *filename = argc > 1 ? argv[1] : "tsp.txt";
    struct timespec start, finish;
    clock_gettime(CLOCK_MONOTONIC, &start);

    printf("\nReading input data for Traveling Salesman Problem.\n");
    Point *points = NULL;
    int n = 0;
    if (!read_cities(filename, &points, &n)) return EXIT_FAILURE;
    printf("No. of cities: %d\n", n);

    double length;
    int *tour = NULL;
    int ok;
    if (n > 27) {
        printf("\nCalculate heuristic TSP tour.\n");
        ok = nearest_neighbour(points, n, &length, &tour);
        if (ok) printf("\nHeuristic TSP tour length: %.12g\n", length);
        if (ok && n <= 100) {
            printf("Heuristic TSP tour:\n");
            print_tour(tour, n);
        }
    } else {
        printf("\nCalculate optimum TSP tour.\n");
        ok = exact_tsp(points, n, &length, &tour);
        if (ok) {
            printf("\nOptimum TSP tour length: %.12g\n", length);
            printf("Optimum TSP tour:\n");
            print_tour(tour, n);
        }
    }
    clock_gettime(CLOCK_MONOTONIC, &finish);
    if (ok) printf("\nExecution time: %.3f ms\n", elapsed_seconds(start, finish) * 1000.0);
    free(tour);
    free(points);
    return ok ? EXIT_SUCCESS : EXIT_FAILURE;
}
