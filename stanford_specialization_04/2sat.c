/*
 * 2SAT satisfaction problem in C99.
 *
 * Method 1: Papadimitriou's randomized algorithm.
 * Method 2: Kosaraju's strongly connected components algorithm.
 *
 * Input format:
 *   First line: number of variables
 *   Remaining lines: two integer literals per clause, e.g. -7 3 means
 *   (!x7 OR x3).
 *
 * Command line:
 *   2sat.exe <method: 1|2> <input-file> [seed]
 *   With no command-line arguments, defaults to method 2 and input file
 *   2sat.txt.
 *
 * Examples (Windows):
 *   .\2sat.exe                    (defaults: method 2, 2sat.txt)
 *   .\2sat.exe 1 2sat6.txt
 *   .\2sat.exe 1 2sat6.txt 42
 *   .\2sat.exe 2 2sat6.txt
 *
 * Examples (Linux):
 *   ./2sat                       (defaults: method 2, 2sat.txt)
 *   ./2sat 1 2sat6.txt
 *   ./2sat 1 2sat6.txt 42
 *   ./2sat 2 2sat6.txt
 *
 * The optional seed is used only by method 1. If omitted, the program seeds
 * the pseudo-random number generator from the current time.
 *
 * Compile:
 *   GCC/Clang: gcc -O2 -std=c99 -Wall -Wextra -pedantic 2sat.c -o 2sat.exe
 *   MSVC:      cl /O2 /W4 2sat.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <errno.h>
#include <limits.h>
#include <stdint.h>
#include <stddef.h>

/* Dynamic integer array, used for adjacency lists and clause indexes. */
typedef struct {
    int *data;
    int size;
    int capacity;
} IntVec;

static void vec_init(IntVec *v) {
    v->data = NULL;
    v->size = 0;
    v->capacity = 0;
}

static int vec_push(IntVec *v, int value) {
    if (v->size == v->capacity) {
        int new_capacity = v->capacity == 0 ? 4 : v->capacity * 2;
        int *new_data;
        if (new_capacity < v->capacity || (size_t)new_capacity > SIZE_MAX / sizeof(int))
            return 0;
        new_data = (int *)realloc(v->data, (size_t)new_capacity * sizeof(int));
        if (!new_data) return 0;
        v->data = new_data;
        v->capacity = new_capacity;
    }
    v->data[v->size++] = value;
    return 1;
}

static void vec_free(IntVec *v) {
    free(v->data);
    v->data = NULL;
    v->size = v->capacity = 0;
}

typedef struct {
    int a;
    int b;
} Clause;

typedef struct {
    int n_vars;
    int n_clauses;
    Clause *clauses;
} Formula;

/* Literal mapping: -n..-1 -> 0..n-1; +1..+n -> n..2n-1. */
static int lit_index(int lit, int n_vars) {
    return lit < 0 ? lit + n_vars : lit + n_vars - 1;
}

static int read_formula(const char *filename, Formula *f) {
    FILE *fp = fopen(filename, "r");
    int n, a, b, capacity = 0;
    char line[4096];
    if (!fp) {
        fprintf(stderr, "Cannot open input file '%s': %s\n", filename, strerror(errno));
        return 0;
    }
    f->n_vars = 0;
    f->n_clauses = 0;
    f->clauses = NULL;

    /* Read the first non-empty line as the variable count. */
    while (fgets(line, sizeof(line), fp)) {
        char *p = line;
        while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') ++p;
        if (*p == '\0' || *p == '#') continue;
        if (sscanf(p, "%d", &n) != 1 || n < 0) {
            fprintf(stderr, "Invalid number of variables in '%s'.\n", filename);
            fclose(fp);
            return 0;
        }
        f->n_vars = n;
        break;
    }
    if (feof(fp) && f->n_vars == 0) {
        /* Empty file and a legitimate zero-variable file are indistinguishable;
           detect emptiness by checking whether any line was read. */
        rewind(fp);
        if (!fgets(line, sizeof(line), fp)) {
            fprintf(stderr, "Input file '%s' is empty.\n", filename);
            fclose(fp);
            return 0;
        }
    }

    while (fgets(line, sizeof(line), fp)) {
        char *p = line;
        while (*p == ' ' || *p == '\t' || *p == '\r' || *p == '\n') ++p;
        if (*p == '\0' || *p == '#') continue;
        if (sscanf(p, "%d %d", &a, &b) != 2) {
            fprintf(stderr, "Invalid clause line: %s", line);
            free(f->clauses);
            f->clauses = NULL;
            fclose(fp);
            return 0;
        }
        if (a == 0 || b == 0 || a > f->n_vars || a < -f->n_vars ||
            b > f->n_vars || b < -f->n_vars) {
            fprintf(stderr, "Literal out of range in clause (%d, %d); expected +/-1..%d.\n",
                    a, b, f->n_vars);
            free(f->clauses);
            f->clauses = NULL;
            fclose(fp);
            return 0;
        }
        if (f->n_clauses == capacity) {
            int new_capacity = capacity == 0 ? 256 : capacity * 2;
            Clause *tmp;
            if (new_capacity < capacity || (size_t)new_capacity > SIZE_MAX / sizeof(Clause)) {
                fprintf(stderr, "Too many clauses.\n");
                free(f->clauses);
                f->clauses = NULL;
                fclose(fp);
                return 0;
            }
            tmp = (Clause *)realloc(f->clauses, (size_t)new_capacity * sizeof(Clause));
            if (!tmp) {
                fprintf(stderr, "Out of memory while reading clauses.\n");
                free(f->clauses);
                f->clauses = NULL;
                fclose(fp);
                return 0;
            }
            f->clauses = tmp;
            capacity = new_capacity;
        }
        f->clauses[f->n_clauses].a = a;
        f->clauses[f->n_clauses].b = b;
        ++f->n_clauses;
    }
    fclose(fp);
    return 1;
}

static int literal_value(int lit, const unsigned char *values) {
    int value = values[abs(lit) - 1] != 0;
    return lit < 0 ? !value : value;
}

static int validate_solution(const Formula *f, const unsigned char *values) {
    int i;
    for (i = 0; i < f->n_clauses; ++i) {
        if (!literal_value(f->clauses[i].a, values) &&
            !literal_value(f->clauses[i].b, values)) return 0;
    }
    return 1;
}

/* SplitMix64 pseudo-random number generator. */
static uint64_t rng_next(uint64_t *state) {
    uint64_t z = (*state += UINT64_C(0x9e3779b97f4a7c15));
    z = (z ^ (z >> 30)) * UINT64_C(0xbf58476d1ce4e5b9);
    z = (z ^ (z >> 27)) * UINT64_C(0x94d049bb133111eb);
    return z ^ (z >> 31);
}

/* One RNG call yields both random choices of a walk step:
   - an unbiased index in [0, bound) via Lemire's multiply-shift method on the
     low 32 bits (no division except in the rare rejection case);
   - a fair coin from the top bit, used to pick one of the clause's literals. */
static uint32_t rng_pick(uint64_t *state, uint32_t bound, unsigned *coin) {
    uint64_t r = rng_next(state);
    uint64_t prod = (uint64_t)(uint32_t)r * bound;
    uint32_t low = (uint32_t)prod;
    if (low < bound) {
        uint32_t threshold = (uint32_t)(0u - bound) % bound;
        while (low < threshold) {
            r = rng_next(state);
            prod = (uint64_t)(uint32_t)r * bound;
            low = (uint32_t)prod;
        }
    }
    *coin = (unsigned)(r >> 63);
    return (uint32_t)(prod >> 32);
}

/* Encoded literal: 2 * (variable index) + (1 if negated). Literal code l is
   true under assignment values iff values[l >> 1] != (l & 1). */
static int lit_code(int lit) {
    return ((abs(lit) - 1) << 1) | (lit < 0);
}

/*
 * Pure-literal elimination. A variable that occurs with only one polarity in
 * the remaining clauses can be set so that literal is true; all its clauses are
 * then satisfied and removed, which may make further variables pure. The
 * reduced formula is satisfiable iff the original one is, and any satisfying
 * assignment of the reduced formula extends to the original one.
 *
 * Runs in O(n + m). On return, alive[c] marks the clauses that remain, and
 * fixed[v] is 0/1 for eliminated variables and 2 for all others.
 */
static int pure_literal_reduction(const Formula *f, unsigned char *alive,
                                  unsigned char *fixed) {
    int n = f->n_vars, m = f->n_clauses, i;
    int n_lits = 2 * n;
    int *count = (int *)calloc((size_t)n_lits, sizeof(int));
    int *start = (int *)calloc((size_t)n_lits + 1, sizeof(int));
    int *occ = (int *)malloc((size_t)(2 * (size_t)m + 1) * sizeof(int));
    int *queue = (int *)malloc((size_t)n * sizeof(int));
    int head = 0, tail = 0;

    if (!count || !start || !occ || !queue) {
        free(count); free(start); free(occ); free(queue);
        return 0;
    }

    /* Literal -> clause occurrence lists (CSR). Tautologies (x OR !x) are
       always satisfied and are dropped right away. */
    for (i = 0; i < m; ++i) {
        int a = lit_code(f->clauses[i].a), b = lit_code(f->clauses[i].b);
        alive[i] = (unsigned char)((a ^ b) != 1);
        if (!alive[i]) continue;
        ++start[a + 1];
        if (b != a) ++start[b + 1];
    }
    for (i = 0; i < n_lits; ++i) {
        start[i + 1] += start[i];
        count[i] = start[i + 1] - start[i];
    }
    {
        int *fill = (int *)malloc((size_t)n_lits * sizeof(int));
        if (!fill) {
            free(count); free(start); free(occ); free(queue);
            return 0;
        }
        memcpy(fill, start, (size_t)n_lits * sizeof(int));
        for (i = 0; i < m; ++i) {
            int a, b;
            if (!alive[i]) continue;
            a = lit_code(f->clauses[i].a);
            b = lit_code(f->clauses[i].b);
            occ[fill[a]++] = i;
            if (b != a) occ[fill[b]++] = i;
        }
        free(fill);
    }

    for (i = 0; i < n; ++i) {
        fixed[i] = 2;
        if ((count[2 * i] == 0) != (count[2 * i + 1] == 0)) queue[tail++] = i;
    }

    while (head < tail) {
        int v = queue[head++], pure, q;
        if (fixed[v] != 2) continue;
        if (count[2 * v] > 0 && count[2 * v + 1] > 0) continue;
        if (count[2 * v] == 0 && count[2 * v + 1] == 0) continue;
        pure = count[2 * v] > 0 ? 2 * v : 2 * v + 1;
        fixed[v] = (unsigned char)!(pure & 1);

        for (q = start[pure]; q < start[pure + 1]; ++q) {
            int c = occ[q], a, b, other;
            if (!alive[c]) continue;
            alive[c] = 0;
            a = lit_code(f->clauses[c].a);
            b = lit_code(f->clauses[c].b);
            --count[pure];
            if (a == b) continue;
            other = (a == pure) ? b : a;
            if (--count[other] == 0 && count[other ^ 1] > 0 &&
                fixed[other >> 1] == 2) {
                queue[tail++] = other >> 1;
            }
        }
    }

    free(count); free(start); free(occ); free(queue);
    return 1;
}

static void progress(const char *what, uint64_t k, clock_t tic) {
    printf("%s = %llu, dt = %.3f s\n", what, (unsigned long long)k,
           (double)(clock() - tic) / CLOCKS_PER_SEC);
    fflush(stdout);
}

/*
 * Method 1: Papadimitriou's randomized local search.
 *
 * Optimizations for large instances (n, m >= 200000):
 *   1. Pure-literal elimination shrinks the instance first. The walk then runs
 *      on the reduced formula with n' variables, so the iteration bound
 *      log2(n') * 2 n'^2 applies to n' instead of n. On the course data sets
 *      this removes the vast majority of variables.
 *   2. Literals are pre-encoded (no abs()/branching), and occurrence lists are
 *      flat CSR arrays instead of per-variable heap vectors.
 *   3. Each clause keeps a count of its true literals (0..2), so a flip only
 *      updates counters; the unsatisfied set is a swap-remove array, so
 *      picking a random unsatisfied clause and the termination check are O(1).
 *   4. One SplitMix64 call per step supplies both random choices; the bounded
 *      draw uses Lemire's method instead of a 64-bit modulo.
 *   5. Random restarts draw 64 assignment bits per RNG call, and progress
 *      reporting uses a countdown instead of a modulo in the hot loop.
 */
static int solve_randomized(const Formula *f, unsigned char *solution, uint64_t seed) {
    int n = f->n_vars, m = f->n_clauses;
    int i, nr = 0, mr = 0;
    unsigned char *alive = NULL, *fixed = NULL, *values = NULL, *n_true = NULL;
    int *new_index = NULL, *orig_var = NULL, *cl = NULL;
    int *occ_start = NULL, *occ = NULL;
    uint32_t *unsat = NULL, *unsat_pos = NULL;
    uint64_t rng_state = seed;
    uint64_t n_outer, n_inner, report_every;
    int result = 0;
    clock_t tic = clock();

    if (n < 0 || m < 0) {
        fprintf(stderr, "Invalid solver input.\n");
        return 0;
    }
    if (n == 0) return m == 0;
    if (m > (INT_MAX >> 1) - 1) {
        fprintf(stderr, "Too many clauses for the randomized solver.\n");
        return 0;
    }

    alive = (unsigned char *)malloc((size_t)m + 1);
    fixed = (unsigned char *)malloc((size_t)n);
    new_index = (int *)malloc((size_t)n * sizeof(int));
    if (!alive || !fixed || !new_index ||
        !pure_literal_reduction(f, alive, fixed)) {
        fprintf(stderr, "Memory allocation failed in randomized solver.\n");
        goto done;
    }

    /* Compact the surviving clauses and variables. */
    for (i = 0; i < n; ++i) new_index[i] = -1;
    for (i = 0; i < m; ++i) {
        if (!alive[i]) continue;
        ++mr;
        if (new_index[abs(f->clauses[i].a) - 1] < 0) new_index[abs(f->clauses[i].a) - 1] = nr++;
        if (new_index[abs(f->clauses[i].b) - 1] < 0) new_index[abs(f->clauses[i].b) - 1] = nr++;
    }
    printf("Pure-literal reduction: %d -> %d variables, %d -> %d clauses (%.3f s).\n",
           n, nr, m, mr, (double)(clock() - tic) / CLOCKS_PER_SEC);
    fflush(stdout);

    /* Eliminated variables take their pure value; unconstrained ones get 0. */
    for (i = 0; i < n; ++i) solution[i] = (unsigned char)(fixed[i] == 1);
    if (mr == 0) { result = 1; goto done; }

    orig_var = (int *)malloc((size_t)nr * sizeof(int));
    cl = (int *)malloc((size_t)mr * 2 * sizeof(int));
    occ_start = (int *)calloc((size_t)nr + 1, sizeof(int));
    occ = (int *)malloc((size_t)mr * 2 * sizeof(int));
    values = (unsigned char *)malloc((size_t)nr + 8);
    n_true = (unsigned char *)malloc((size_t)mr);
    unsat = (uint32_t *)malloc((size_t)mr * sizeof(uint32_t));
    unsat_pos = (uint32_t *)malloc((size_t)mr * sizeof(uint32_t));
    if (!orig_var || !cl || !occ_start || !occ || !values || !n_true ||
        !unsat || !unsat_pos) {
        fprintf(stderr, "Memory allocation failed in randomized solver.\n");
        goto done;
    }

    for (i = 0; i < n; ++i) if (new_index[i] >= 0) orig_var[new_index[i]] = i;
    {
        int c = 0;
        for (i = 0; i < m; ++i) {
            int a, b;
            if (!alive[i]) continue;
            a = f->clauses[i].a;
            b = f->clauses[i].b;
            cl[2 * c] = (new_index[abs(a) - 1] << 1) | (a < 0);
            cl[2 * c + 1] = (new_index[abs(b) - 1] << 1) | (b < 0);
            ++c;
        }
    }

    /* Variable -> occurrence list. Entry = 2 * clause + (1 if the literal is
       negated). A clause (x OR x) contributes two entries, which keeps the
       true-literal counter consistent. */
    for (i = 0; i < 2 * mr; ++i) ++occ_start[(cl[i] >> 1) + 1];
    for (i = 0; i < nr; ++i) occ_start[i + 1] += occ_start[i];
    {
        int *fill = (int *)malloc((size_t)nr * sizeof(int));
        if (!fill) {
            fprintf(stderr, "Memory allocation failed in randomized solver.\n");
            goto done;
        }
        memcpy(fill, occ_start, (size_t)nr * sizeof(int));
        for (i = 0; i < 2 * mr; ++i)
            occ[fill[cl[i] >> 1]++] = ((i >> 1) << 1) | (cl[i] & 1);
        free(fill);
    }
    printf("Variables to clauses lists created.\n");
    fflush(stdout);

    /* floor(log2(n')) + 1 restarts of 2 n'^2 steps each. */
    n_outer = 0;
    for (uint64_t x = (uint64_t)nr; x > 0; x >>= 1) ++n_outer;
    n_inner = 2 * (uint64_t)nr * (uint64_t)nr;
    report_every = n_inner / 100 ? n_inner / 100 : n_inner;

    for (uint64_t outer = 0; outer < n_outer; ++outer) {
        uint32_t n_unsat = 0;
        uint64_t k, report = report_every;

        progress("outer iteration", outer + 1, tic);

        for (i = 0; i < nr; i += 64) {
            uint64_t bits = rng_next(&rng_state);
            int j, lim = nr - i < 64 ? nr - i : 64;
            for (j = 0; j < lim; ++j) values[i + j] = (unsigned char)((bits >> j) & 1);
        }

        for (i = 0; i < mr; ++i) {
            int a = cl[2 * i], b = cl[2 * i + 1];
            n_true[i] = (unsigned char)((values[a >> 1] != (a & 1)) +
                                        (values[b >> 1] != (b & 1)));
            if (n_true[i] == 0) {
                unsat_pos[i] = n_unsat;
                unsat[n_unsat++] = (uint32_t)i;
            }
        }

        for (k = 0; k < n_inner && n_unsat > 0; ++k) {
            unsigned coin, val;
            uint32_t c;
            int v, q, q_end;

            if (--report == 0) {
                report = report_every;
                /*progress("inner iteration", k + 1, tic);*/
            }

            /* Pick a random unsatisfied clause and flip one of its variables. */
            c = unsat[rng_pick(&rng_state, n_unsat, &coin)];
            v = cl[2 * c + coin] >> 1;
            val = values[v] ^= 1;

            /* Update only clauses containing v. */
            for (q = occ_start[v], q_end = occ_start[v + 1]; q < q_end; ++q) {
                uint32_t e = (uint32_t)occ[q], ci = e >> 1;
                if (val != (e & 1)) {           /* literal became true */
                    if (n_true[ci]++ == 0) {
                        uint32_t pos = unsat_pos[ci], last = unsat[--n_unsat];
                        unsat[pos] = last;
                        unsat_pos[last] = pos;
                    }
                } else if (--n_true[ci] == 0) {  /* literal became false */
                    unsat_pos[ci] = n_unsat;
                    unsat[n_unsat++] = ci;
                }
            }
        }

        if (n_unsat == 0) {
            printf("Satisfying assignment found after %llu flips in outer iteration %llu.\n",
                   (unsigned long long)k, (unsigned long long)(outer + 1));
            for (i = 0; i < nr; ++i) solution[orig_var[i]] = values[i];
            result = 1;
            goto done;
        }
    }
    /* Failure to find a solution is not proof of UNSAT. */

done:
    free(alive); free(fixed); free(new_index); free(orig_var); free(cl);
    free(occ_start); free(occ); free(values); free(n_true);
    free(unsat); free(unsat_pos);
    return result;
}

/* DFS frame used to preserve recursive DFS successor-iteration state. */
typedef struct {
    int vertex;
    int next_edge;
} DfsFrame;

static int build_graph(const Formula *f, IntVec **graph_out, IntVec **reverse_out) {
    int vertices = 2 * f->n_vars, i;
    IntVec *g = vertices ? (IntVec *)malloc((size_t)vertices * sizeof(IntVec)) : NULL;
    IntVec *rg = vertices ? (IntVec *)malloc((size_t)vertices * sizeof(IntVec)) : NULL;
    if (vertices && (!g || !rg)) { free(g); free(rg); return 0; }
    for (i = 0; i < vertices; ++i) { vec_init(&g[i]); vec_init(&rg[i]); }
    for (i = 0; i < f->n_clauses; ++i) {
        int a = f->clauses[i].a, b = f->clauses[i].b;
        int na = lit_index(-a, f->n_vars), nb = lit_index(-b, f->n_vars);
        int ia = lit_index(a, f->n_vars), ib = lit_index(b, f->n_vars);
        /* Original graph: !a -> b and !b -> a. */
        if (!vec_push(&g[na], b) || !vec_push(&g[nb], a) ||
            /* Reverse graph: b -> !a and a -> !b. */
            !vec_push(&rg[ib], -a) || !vec_push(&rg[ia], -b)) {
            int j; for (j = 0; j < vertices; ++j) { vec_free(&g[j]); vec_free(&rg[j]); }
            free(g); free(rg); return 0;
        }
    }
    *graph_out = g;
    *reverse_out = rg;
    return 1;
}

static void free_graph(IntVec *g, IntVec *rg, int vertices) {
    int i;
    for (i = 0; i < vertices; ++i) { vec_free(&g[i]); vec_free(&rg[i]); }
    free(g); free(rg);
}

/* Iterative Kosaraju: first pass records vertices in descending finish time;
   second pass assigns component IDs. */
static int solve_scc(const Formula *f, unsigned char *solution) {
    int n = f->n_vars, count = 2 * n, i, order_count = 0, component = 0;
    IntVec *g = NULL, *rg = NULL;
    unsigned char *seen = NULL;
    int *order = NULL, *component_id = NULL;
    DfsFrame *stack = NULL;
    if (n == 0) return f->n_clauses == 0;
    printf("Build implication graph.\n");
    fflush(stdout);
    if (!build_graph(f, &g, &rg)) { fprintf(stderr, "Could not build implication graph (out of memory).\n"); return 0; }
    seen = (unsigned char *)calloc((size_t)count, 1);
    order = (int *)malloc((size_t)count * sizeof(int));
    component_id = (int *)malloc((size_t)count * sizeof(int));
    stack = (DfsFrame *)malloc((size_t)count * sizeof(DfsFrame));
    if (!seen || !order || !component_id || !stack) {
        fprintf(stderr, "Out of memory in SCC solver.\n");
        free(seen); free(order); free(component_id); free(stack); free_graph(g, rg, count); return 0;
    }
    for (i = 0; i < count; ++i) component_id[i] = -1;

    /* Pass 1 on reversed graph. */
    printf("Calculating pass 1.\n");
    fflush(stdout);
    for (i = 0; i < count; ++i) {
        int top;
        if (seen[i]) continue;
        top = 0; stack[top++] = (DfsFrame){i, 0}; seen[i] = 1;
        while (top > 0) {
            DfsFrame *frame = &stack[top - 1];
            int v = frame->vertex;
            if (frame->next_edge < rg[v].size) {
                int w_lit = rg[v].data[frame->next_edge++];
                int w = lit_index(w_lit, n);
                if (!seen[w]) { seen[w] = 1; stack[top++] = (DfsFrame){w, 0}; }
            } else {
                order[order_count++] = v;
                --top;
            }
        }
    }

    /* Pass 2 on original graph in reverse finishing order. */
    printf("Calculating pass 2.\n");
    fflush(stdout);
    memset(seen, 0, (size_t)count);
    while (order_count > 0) {
        int root = order[--order_count], top;
        if (seen[root]) continue;
        ++component;
        top = 0; stack[top++] = (DfsFrame){root, 0}; seen[root] = 1;
        component_id[root] = component;
        while (top > 0) {
            DfsFrame *frame = &stack[top - 1];
            int v = frame->vertex;
            if (frame->next_edge < g[v].size) {
                int w_lit = g[v].data[frame->next_edge++];
                int w = lit_index(w_lit, n);
                if (!seen[w]) {
                    seen[w] = 1; component_id[w] = component;
                    stack[top++] = (DfsFrame){w, 0};
                }
            } else --top;
        }
    }

    printf("Construct 2SAT assignment.\n");
    fflush(stdout);
    for (i = 1; i <= n; ++i) {
        int pos = lit_index(i, n), neg = lit_index(-i, n);
        if (component_id[pos] == component_id[neg]) {
            free(seen); free(order); free(component_id); free(stack); free_graph(g, rg, count);
            return 0;
        }
        /* Components are numbered in the order discovered by the second pass;
           with this pass ordering, the earlier component literal is set true. */
        solution[i - 1] = (unsigned char)(component_id[pos] < component_id[neg]);
    }
    free(seen); free(order); free(component_id); free(stack); free_graph(g, rg, count);
    return 1;
}

static void print_usage(const char *program) {
    fprintf(stderr,
        "Usage: %s <method: 1|2> <input-file> [seed]\n"
        "  With no arguments: method 2 and input file 2sat.txt\n"
        "  method 1 = Papadimitriou randomized algorithm\n"
        "  method 2 = Kosaraju SCC algorithm\n"
        "  seed is optional and applies to method 1 only\n\n"
        "Examples:\n"
        "  %s                         (defaults: method 2, 2sat.txt)\n"
        "  %s 1 2sat6.txt\n"
        "  %s 1 2sat6.txt 42\n"
        "  %s 2 2sat6.txt\n", program, program, program, program, program);
}

int main(int argc, char **argv) {
    Formula f;
    int method, solvable, i;
    unsigned int seed;
    int seed_supplied = 0;
    unsigned char *solution;
    clock_t start, end;

    /* Defaults apply only when the program is called without any arguments. */
    if (argc == 1) {
        method = 2;
        /* Copy the default filename into argv-independent storage below. */
    } else {
        if (argc < 3 || argc > 4) { print_usage(argv[0]); return EXIT_FAILURE; }
        if (strcmp(argv[1], "1") == 0) method = 1;
        else if (strcmp(argv[1], "2") == 0) method = 2;
        else { fprintf(stderr, "Invalid method '%s'; choose 1 or 2.\n", argv[1]); print_usage(argv[0]); return EXIT_FAILURE; }
    }
    seed = (unsigned int)time(NULL);
    if (argc == 4) {
        char *endptr;
        unsigned long parsed;
        errno = 0;
        parsed = strtoul(argv[3], &endptr, 10);
        if (errno || *argv[3] == '\0' || *endptr != '\0' || parsed > UINT_MAX) {
            fprintf(stderr, "Invalid seed '%s'; expected an integer from 0 to %u.\n", argv[3], UINT_MAX);
            return EXIT_FAILURE;
        }
        seed = (unsigned int)parsed;
        seed_supplied = 1;
    }

    start = clock();
    printf("\nReading input data for 2SAT problem.\n");
    if (argc == 1) {
        if (!read_formula("2sat.txt", &f)) return EXIT_FAILURE;
    } else {
        if (!read_formula(argv[2], &f)) return EXIT_FAILURE;
    }
    printf("No. of variables: %d, no. of clauses: %d\n", f.n_vars, f.n_clauses);
    printf("\nCalculate 2SAT assignment using method %d.\n", method);
    solution = f.n_vars ? (unsigned char *)calloc((size_t)f.n_vars, 1) : NULL;
    if (f.n_vars && !solution) {
        fprintf(stderr, "Out of memory allocating solution.\n");
        free(f.clauses);
        return EXIT_FAILURE;
    }
    if (method == 1) {
        printf("Random seed: %u%s\n", seed, seed_supplied ? " (provided)" : " (current time)");
        solvable = solve_randomized(&f, solution, seed);
    } else {
        solvable = solve_scc(&f, solution);
    }

    if (solvable) {
        if (validate_solution(&f, solution)) {
            printf("\nThis 2SAT instance is satisfiable.\n");
            if (f.n_vars <= 100) {
                printf("Satisfying assignment (x1..xn; 1=true, 0=false):\n[");
                for (i = 0; i < f.n_vars; ++i) printf("%s%d", i ? ", " : "", solution[i] ? 1 : 0);
                printf("]\n");
            }
        } else {
            printf("\nCalculated assignment is not valid.\n");
            free(solution); free(f.clauses); return EXIT_FAILURE;
        }
    } else if (method == 1) {
        printf("\nNo satisfying assignment found by the randomized algorithm.\n"
               "This is not a proof that the instance is unsatisfiable.\n");
    } else {
        printf("\nThis 2SAT instance is not satisfiable.\n");
    }
    end = clock();
    printf("\nExecution time: %.3f ms\n", 1000.0 * (double)(end - start) / CLOCKS_PER_SEC);
    free(solution);
    free(f.clauses);
    return EXIT_SUCCESS;
}
