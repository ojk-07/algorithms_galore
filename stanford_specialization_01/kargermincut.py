# -*- coding: utf-8 -*-
"""
Karger Min Cut algorithm.

A program for Stanford Algorithms Specialization written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #4 in the Course
https://www.coursera.org/learn/algorithms-divide-conquer/home/module/4
"""

import time
import sys
import random as rd
import numpy  as np

def karger(adj_list, adj_dict, adj_matrix, seed=1, verbose=False):
    """
    Caluclation of the min cut for a given graph with n vertices and m edges
    using Karger's randomized algorithm proposed in the 1990's.
    With a single run, the probability to find the targeted min cut
    is >= 2/(n*(n-1)) >= 1/n^2.
    Each run requires O(n^2) time.

    Arguments:
        adj_list (list):
            Adjacency list of uncontracted vertices.
        adj_dict (dict):
            Dictionary matching a vertex number to the internal index
            in adj_mat.
        adj_matrix (np.ndarray):
            Adjacency matrix with the connections between vertices.
        verbose (bool):
            More intermediate output is written when True.

    Returns:
        k (int):
            Number of cuts of the contracted graph.
        i1v (int):
            Number of one of the remaining vertices.
        i2v (int):
            Number of one of the remaining vertices.
        contr_list (list):
            List of contractions that have happened.
            First number is the vertex beig contracted into the vertex with
            the second number.
        """

    # Calculate number of vertices.
    n_graph = len(adj_list)
    n_dim = adj_matrix.shape[0]
    assert n_dim == n_graph

    # The adjacency matrix for an undirected graph must be symmetric.
    #assert (adj_matrix - adj_matrix.T).all() == 0

    # The adjacency matrix shall not contain self-loops.
    #assert np.diag(adj_matrix).all() == 0

    # Initialize the random seed.
    rd.seed(seed)

    # Loop over number of vertices until all but just 2 got contracted.
    #print(adj_matrix)
    contr_list = []
    for n in reversed(range(3, n_graph + 1)):
        # Randomly select one vertex for contraction.
        # Vertices are indexed from 0 to n - 1 in adj_list.
        i1 = int(rd.random() * n)

        # Identify the vertex numbers from adj_list.
        i1v = adj_list[i1]
        # Identify the matrix index of this vertex. 
        i1m = adj_dict[i1v]

        # Randomly select one vertex among the neighbouring vertices
        # to get contracted.
        neighbours_list = []
        for i2v in adj_list:
            i2m = adj_dict[i2v]
            if adj_matrix[i1m, i2m] > 0:
                neighbours_list.append(i2v)
        n_neighbours = len(neighbours_list)
        i2 = int(rd.random() * n_neighbours)

        # Identify the vertex number from neighbours_list.
        i2v = neighbours_list[i2]
        # Identify the matrix index of this vertex. 
        i2m = adj_dict[i2v]

        # Add contraction to contraction list.
        contr_list.append((i2v, i1v))
        if verbose:
            print('{0} vertices, will contract: {1}->{2}'.format(n, i2v, i1v))

        # Contract selected vertices.
        # Vertex i2v is contracted into i1v, vertex i1v becomes a super vertex.
        # Remove i2v from adj_list.
        adj_list.remove(i2v)
        if verbose:
            print('New vertex list adj_list:\n{0}'.format(adj_list))

        # All edges containing i2v become an edge with i1v.
        for j in range(n_dim):
            # Vertex iv1 inherits all connections from i2v.
            # Since there are no self-loops in adj_matrix, a special
            # treatment of adj_matrix[i2m, i2m] is not necessary.
            if adj_matrix[i2m, j] > 0:
                adj_matrix[i1m, j] += adj_matrix[i2m, j]
                adj_matrix[i2m, j] = 0
            if adj_matrix[j, i2m] > 0:
                adj_matrix[j, i1m] += adj_matrix[j, i2m]
                adj_matrix[j, i2m] = 0
        # Remove eventual self-loops for i1v.
        adj_matrix[i1m, i1m] = 0
        if verbose:
            print('New adjacency matrix adj_matrix:\n{0}'.format(adj_matrix))

    # The adjacency matrix for an undirected graph must be symmetric.
    #assert (adj_matrix - adj_matrix.T).all() == 0

    # The adjacency matrix shall not contain self-loops.
    #assert np.diag(adj_matrix).all() == 0

    # Count the remaining edges between the last 2 vertices.
    i1v = adj_list[0]
    i2v = adj_list[1]
    i1m = adj_dict[i1v]
    i2m = adj_dict[i2v]
    k = 0
    for j in range(n_dim):
        k += int(adj_matrix[i1m, j])

    return k, i1v, i2v, contr_list

def karger_calculate_cut(i1v, i2v, contr_list):
    """
    Caluclation of the point sets A and B of a provided cut.

    Arguments:
        i1v (int):
            Number of one of the remaining vertices.
        i2v (int):
            Number of one of the remaining vertices.
        contr_list (list):
            List of contractions that have happened.
            First number is the vertex beig contracted into the vertex with
            the second number.

    Returns:
        A, B (lists):
            Points sets seperated by the provided cut.
        """

    # Initialize point sets A and B.
    A = [i1v]
    B = [i2v]

    # Add the contracted points from the contraction list backwards.
    for i in reversed(contr_list):
        if i[1] in A:
            # Last contracted points belongs to set A.
            A.append(i[0])
        else:
            # Last contracted points belongs to set B.
            B.append(i[0])

    # Sort lists.
    A = sorted(A)
    B = sorted(B)

    return A, B

def karger_iterations(alpha, n):
    """
    Caluclation of the minimum number of iterations needed to reach a
    probability p >= alpha of finding the min cut with Kager's algorithm.

    Arguments:
        alpha (float):
            Required probability of finding the min cut in the graph.
        n (int):
            Number of vertices in the graph.

    Returns:
        i_min (int):
            Minmum number of iterations needed.
        """

    x = np.log(1 - alpha) / np.log(1 - 2/(n*(n - 1)))
    i_min = int(x) + 1

    return i_min

def read_list(file_name):
    # Read list data from file.
    # Each row represents 1 item of the list.
    try:
        with open(file_name, 'r') as f:
            # Read data from file.
            raw_data = f.readlines()
            n = len(raw_data)
            # Initialize structures.
            # List of all vertices.
            # adj_vert just contains the vertex numbers.
            # adj_list contains the vertex numbers and connections.
            adj_vert = []
            adj_list = []
            # Dict matching a vertex number to the internal index in adj_mat.
            adj_dict = {}
            # Initialize adjacency matrix to store the connections.
            adj_matrix = np.zeros((n, n))
            # Fill lists.
            for i in range(n):
                row_list = []
                for j in enumerate(raw_data[i].split()):
                    iv = int(j[1])
                    row_list.append(iv)
                    if j[0] == 0:
                        # First column is the vertex number.
                        adj_vert.append(iv)
                        adj_dict[iv] = i
                adj_list.append(row_list)
            # Fill adjacency matrix.
            # A second pass is necessary if we assume that the row numbers
            # in the input file might not be identical to the vertex number.
            for i in adj_list:
                for j in enumerate(i):
                    if j[0] == 0:
                        # Vertex number.
                        iv_matrix = adj_dict[j[1]]
                    else:
                        # Connections.
                        jv_matrix = adj_dict[j[1]]
                        adj_matrix[iv_matrix, jv_matrix] = 1
        return 0, adj_vert, adj_list, adj_dict, adj_matrix
    except:
        adj_vert = []
        adj_list = []
        adj_dict = {}
        adj_matrix = np.zeros((0, 0))
        return 1, adj_vert, adj_list, adj_dict, adj_matrix

if __name__ == '__main__':

    # Set parameters for calculation.
    verbose = False
    #n_iter  = 1000
    #n_iter  = 13794    # guarantees 50% probability of success for n = 200
    #n_iter  = 45821    # guarantees 90% probability of success for n = 200
    #n_iter  = 91641    # guarantees 99% probability of success for n = 200
    n_iter  = 137461   # guarantees 99.9% probability of success for n = 200
    seed_offset = 1

    # Read the list input from file.
    file_name = 'kargerMinCut.txt'   #min_cut = 17
    status, adj_vert, adj_list, adj_dict, adj_matrix = read_list(file_name)

    # Randomly calculate a contracted graph.
    tic = time.perf_counter()
    contr_list_min = []
    k_min = len(adj_vert)
    i = 0
    while i < n_iter:
        adj_vertc   = adj_vert.copy()
        adj_matrixc = adj_matrix.copy()
        k, i1v, i2v, contr_list = karger(adj_vertc, adj_dict, adj_matrixc,
                                         seed=seed_offset + i, verbose=verbose)
        if k < k_min:
            k_min, i1v_min, i2v_min, contr_list_min = k, i1v, i2v, contr_list
            A, B = karger_calculate_cut(i1v_min, i2v_min, contr_list_min)
            sys.stdout.write('\nCalculated contracted graph with vertices '
                +'{0}, {1} with {2} cuts'.format(i1v_min, i2v_min, k_min))
            sys.stdout.write('\nContraction list:\n{0}'.format(contr_list_min))
            sys.stdout.write('\nPoints sets A and B:\n{0}\n{1}'.format(A, B))
            sys.stdout.write('\n')
            sys.stdout.flush()
        sys.stdout.write('\rIteration: {0}'.format(i + 1))
        sys.stdout.flush()
        i += 1
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))