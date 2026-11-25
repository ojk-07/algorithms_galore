# -*- coding: utf-8 -*-
"""
Traveling Salesman algorithm based on Dynamic Programming for edge weights
based on Euklidian distances.
Running time: O(n² 2**n).

A program for Stanford Algorithms Specialization 4 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #3 in the Course
https://www.coursera.org/learn/algorithms-npcomplete/home/module/3
"""

import time
import sys
import os       # for memory analysis
import psutil   # for memory analysis
import numpy   as np
from itertools import combinations
from numba     import njit

process = psutil.Process(os.getpid())

def report_memory(label):
    """
    Report memory allocation of Python process.
    
    Arguments:
        label (str):
            Label of the memory report to be printed.
    
    Returns:
        None
    """

    memory_gb = process.memory_info().rss / 1024**3
    print(f'{label}: {memory_gb:.2f} GB')

@njit(cache=True)
def dp_layer(subsets, subset_masks, row_lookup, A, A_new, D, C):
    """
    Compute one TSP DP layer.
    All loops execute as compiled machine code.
    """

    n_subsets, width = subsets.shape

    # Loop over subsets, city 1 is excluded.
    for row in range(n_subsets):
        s_bin = subset_masks[row]
        # Register the row of this subset.
        row_lookup[s_bin] = row
        # Loop over all elements of subset.
        for j_col in range(width):
            j = subsets[row, j_col]
            sj_bin = s_bin & ~(1 << (j-2))   # set s \ {j}
            c_col = j-2   # global city-based column in C
            if sj_bin == 0:
                # Base case: predecessor is city 1.
                A_new[row, j_col] = D[1, j]
                C[s_bin, c_col] = 1
            else:
                # Row of the previous-layer subset S \ {j}.
                prev = row_lookup[sj_bin]
                # Calculate value of DP subproblem.
                best = np.inf
                best_k = 0
                # Loop over all elements of s except for k=j.
                for k_col in range(width):
                    if k_col == j_col:
                        continue
                    k = subsets[row, k_col]
                    # Determine column of k after removing j from the subset.
                    prev_col = k_col - (j_col < k_col)
                    candidate = A[prev, prev_col] + D[k, j]
                    if candidate < best:
                        best = candidate
                        best_k = k
                # Store results of subproblem.
                A_new[row, j_col] = best
                C[s_bin, c_col] = best_k

def tsp_calc(cities):
    """
    Calculate an optimum Traveling Salesman tour using Dynamic Programming.
    
    In this version, the solutions of the subproblems are stored in
    matrices A and A_new for the previous and current iteration.
    The storage is optimzed to only hold the values A[(S, j)] for the values
    of j that are currently needed.
    The cities leading to the new solutions of subproblems are stored in
    matrix C.
    The DP layer is compiled by Numba.
    
    Arguments:
        cities (dictionary):
            Dictionary of cities to be visited with their x and y coordinates.
    
    Returns:
        length (int or float):
            Length of the optimum TSP tour.
        tour (list):
            List of the cities visited in the optimum TSP tour.
    """

    # Memory report at startup.
    report_memory('Memory usage at start of tsp_calc')
    # Initialize data structures.
    tic    = time.perf_counter()
    n      = len(cities)   # number of cities
    length = np.inf        # length of TSP tour
    tour   = []            # TSP tour

    # Handle simple cases.
    if n == 0:   # no cities
        return 0, []
    if n == 1:   # only city 1
        return 0, [1]

    # Array for distances.
    D = np.zeros((n+1, n+1), dtype=np.float32)
    #D = np.zeros((n+1, n+1), dtype=np.float64)
    for i in range(1, n+1):
        for j in range(1, n+1):
            if i != j:
                D[i, j] = dist(i, j, cities)
    # Array A for results for sub-problems A[(S, j)].
    A = np.empty((0, 0), dtype=D.dtype)
    # Maps subset bitmasks to row indices.
    row_lookup = np.full(1 << (n-1), -1, dtype=np.int32)
    # Array to store which city created A[(S, j)].
    C = np.zeros((1 << (n-1), n-1), dtype=np.uint8)
    # Memory report after initialization of matrices A, C and D.
    report_memory('Memory usage after initialization of matrices A, C and D')

    # Base cases for sub-problems with j=1:
    # A[{1}, 1] = 0, A[S, 1] = np.inf for S != {1}.

    # Calculate values of optimum TSP tours.
    S = range(2, n+1)   # set of cities without city 1
    for m in range(2, n+1):   # loop over subproblem size
        # Create subsets of S with m elements.
        subsets = list(combinations(S, m-1))
        # Prepare call to DP layer.
        subsets_arr = np.asarray(subsets, dtype=np.int32)
        subset_masks = np.asarray(
            [sum(1 << (j-2) for j in s) for s in subsets], dtype=np.int64)
        n_subsets = len(subsets)
        A_new = np.full((n_subsets, m-1), np.inf, dtype=D.dtype)
        # Call DP layer.
        dp_layer(subsets_arr, subset_masks, row_lookup, A, A_new, D, C)
        # Print performance and memory statistics.
        toc = time.perf_counter()
        memory_gb = process.memory_info().rss / 1024**3
        print(f'm = {m}, #subsets = {n_subsets}, ' +
              f'#calcs = {(m-1)*(m-1)*n_subsets}, ' +
              f'{memory_gb:.3f} GB, Δt = {toc-tic:.3f} s')
        A = A_new

    # Complete the tour back to city 1.
    c_last = -1   # no city yet associated as last city on TSP tour
    s_last_bin = (1 << (n-1)) - 1   # all cities 2, ..., n
    prev = row_lookup[s_last_bin]
    for j in range(2, n+1):   # loop over all cities except city 1
        aj = A[prev, j-2] + D[j, 1]
        if aj < length:
            length = aj
            c_last = j

    # Reconstruct optimum TSP tour.
    tour = [c_last, 1]   # initialization of TSP tour
    while s_last_bin != 0:
        c_before   = int(C[s_last_bin, c_last-2])
        s_last_bin &= ~(1 << (c_last-2))   # set s \ {c_last}
        c_last     = c_before
        tour.insert(0, c_before)

    return length, tour

def tsp_heuristic(cities):
    """
    Calculate a Traveling Salesman tour using a simple heuristic.
    
    In this version, the heuristic always chooses the next-neighbour city as
    the next city to visit.
    
    Arguments:
        cities (dictionary):
            Dictionary of cities to be visited with their x and y coordinates.
    
    Returns:
        length (int or float):
            Length of the optimum TSP tour.
        tour (list):
            List of the cities visited in the optimum TSP tour.
    """

    # Initialize data structures.
    tic    = time.perf_counter()
    n      = len(cities)   # number of cities
    msg    = 100           # parameter for number of messages
    length = 0             # length of TSP tour
    tour   = []            # TSP tour

    # Handle simple cases.
    if n == 0:   # no cities
        return 0, []
    if n == 1:   # only city 1
        return 0, [1]

    # Build queue.
    queue = set(cities.keys())   # using a set for fast remove()

    # Loop over cities to be processd.
    s = 1   # city 1 is the start city
    v = s   # start tour with start city
    tour.append(v)   # add current city to tour
    iteration = 1
    while queue:
        # Make next city the new current city.
        u = v
        # Remove current city from queue.
        queue.remove(u)
        # Print performance statistics.
        if n <= msg or iteration % (n//msg) == 1 or iteration == n:
            toc = time.perf_counter()
            print(f'iter = {iteration}, city = {u}, length = {length:.3f}, ' +
                  f'Δt = {toc-tic:.3f} s')
        # Assess distance of remaining queue elements to current city.
        best_dist = np.inf
        v = None
        # Get coordinates of city u.
        coords_u = cities[u]
        for q in queue:
            # Get coordinates of city q.
            coords_q = cities[q]
            # Calculate squared Euklidian distance without function call.
            dx = coords_q[0] - coords_u[0]
            dy = coords_q[1] - coords_u[1]
            d2 = dx*dx + dy*dy
            if d2 < best_dist:
                best_dist = d2
                v = q
        # Add next city to tour.
        if v != None:
            tour.append(v)
            # Update tour length.
            length += best_dist**0.5   # square root to get Eukilidian distance
        iteration += 1
    # Add start city to end of tour.
    tour.append(s)
    length += dist(u, s, cities)

    return length, tour

def dist(i, j, cities):
    """
    Calculate the Euklidian distance between cities i and j.
    
    Arguments:
        i (int):
            First city for distance calculation.
        j (int):
            Second city for distance calculation.
        cities (dictionary):
            Dictionary of cities to be visited with their x and y coordinates.
    
    Returns:
        dist (float):
            Euklidian distance between cities i and j.
    """

    # Get coordinates of cities i and j.
    xi, yi = cities[i]
    xj, yj = cities[j]
    # Calculate Euklidian distance.
    d = ((xj - xi)*(xj - xi) + (yj - yi)*(yj - yi))**0.5
    return d

def read_list(file_name):
    """
    Read source data of city locations.
    The first row contains the number of cities.
    Every other row contains the x and y coordinates of the cities.
    
    Arguments:
        file_name (str):
            File name to be read.
    
    Returns:
        status (int):
            '0' indicates successful processing, '1' that an error ocurred.
        n_items (int):
            Number of cities.
            We assume that there are the items 1 ... n.
        cities (dictionary):
            Dictionary of cities to be visited with their x and y coordinates.
    """

    # Initialize structures.
    cities   = {}
    n_cities  = 0
    # Read list data from file.
    # Each row represents 1 item of the list.
    try:
        with open(file_name, 'r') as f:
            # Read data from file.
            raw_data = f.readlines()
            n = len(raw_data)
            # Evaluate first line.
            row = raw_data[0].split()
            n_cities = int(row[0])
            # Evaluate all other lines.
            for i in range(1, n):   # line number
                # Evaluate current line.
                row = raw_data[i].split()
                x = float(row[0])
                y = float(row[1])
                # Add the x and y coordinates to the dictionary of cities.
                cities[i] = (x, y)
            # Check data consistency.
            assert n_cities == n-1
        return 0, n_cities, cities
    except:
        n_cities, cities = 0, {}
        return 1, n_cities, cities

def read_list_with_ids(file_name):
    """
    Read source data of city locations.
    The first row contains the number of cities.
    Every other row contains the id and the x and y coordinates of the cities.
    
    Arguments:
        file_name (str):
            File name to be read.
    
    Returns:
        status (int):
            '0' indicates successful processing, '1' that an error ocurred.
        n_items (int):
            Number of cities.
            We assume that there are the items 1 ... n.
        cities (dictionary):
            Dictionary of cities to be visited with their x and y coordinates.
    """

    # Initialize structures.
    cities   = {}
    n_cities  = 0
    # Read list data from file.
    # Each row represents 1 item of the list.
    try:
        with open(file_name, 'r') as f:
            # Read data from file.
            raw_data = f.readlines()
            n = len(raw_data)
            # Evaluate first line.
            row = raw_data[0].split()
            n_cities = int(row[0])
            # Evaluate all other lines.
            for i in range(1, n):   # line number
                # Evaluate current line.
                row = raw_data[i].split()
                c = int(row[0])
                x = float(row[1])
                y = float(row[2])
                # Add the x and y coordinates to the dictionary of cities.
                cities[c] = (x, y)
            # Check data consistency.
            assert n_cities == n-1
        return 0, n_cities, cities
    except:
        n_cities, cities = 0, {}
        return 1, n_cities, cities

# Main programm
def runMe():
    file_name = 'tsp.txt'
    #file_name = 'nn.txt'

    tic = time.perf_counter()
    sys.stdout.write('\nReading input data for Traveling Salesman Problem.\n')
    sys.stdout.flush()
    status, n_cities, cities = read_list(file_name)
    #status, n_cities, cities = read_list_with_ids(file_name)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of cities: ' + str(n_cities) + '\n')
    sys.stdout.flush()
    if n_cities > 27:
        sys.stdout.write('\nCalculate heuristic TSP tour.\n')
        sys.stdout.flush()
        length, tour = tsp_heuristic(cities)
        # Heuristic TSP tour length according to assignment.
        sys.stdout.write('\nHeuristic TSP tour length: ' + str(length) + '\n')
        sys.stdout.flush()
        if n_cities <= 100:
            sys.stdout.write('Heuristic TSP tour:\n')
            sys.stdout.write(str(tour) + '\n')
            sys.stdout.flush()
    else:
        sys.stdout.write('\nCalculate optimum TSP tour.\n')
        sys.stdout.flush()
        length, tour = tsp_calc(cities)
        # Optimum TSP tour length according to assignment.
        sys.stdout.write('\nOptimum TSP tour length: ' + str(length) + '\n')
        sys.stdout.flush()
        sys.stdout.write('Optimum TSP tour:\n')
        sys.stdout.write(str(tour) + '\n')
        sys.stdout.flush()
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
