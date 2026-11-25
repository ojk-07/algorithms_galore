# -*- coding: utf-8 -*-
"""
Knapsack algorithm based on Dynamic Programming for non-negative weights
and positive integer item values, and non-negative Knapsack capacity W
via calculating the minimum weight per expected Knapsack value V.
Running time: O(n² vmax).

A program for Stanford Algorithms Specialization 4 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to module 3 in the Course
https://www.coursera.org/learn/algorithms-npcomplete/home/module/3
"""

import time
import sys
from math import inf as INF

def knapsack_subproblems_calc(vmax, values, weights):
    """
    Calculate an the Dynamic Programming subproblems of the optimum Knapsack
    configuration.
    
    Arguments:
        vmax (int):
            Maximum value per Knapsack item.
            We assume that vmax is positive and integer.
        values (list):
            List of values of the Knapsack items.
            We assume that all values are positive and integer.
            We assume that there are the items 1 ... n.
        weights (list):
            List of weights of the Knapsack items.
            We assume that all values are non-negative.
    
    Returns:
        A (list):
            Subproblem solutions of the Knapsack configuration.
        C (list):
            Boolean flags for comparison results of the Knapsack configuration.
    """

    # Initialize data structures.
    n = len(values)   # number of knapsack items
    A = []            # results for sub-problems A[i][v]
    C = []            # boolean flags for comparison results
    Vmax = n*vmax     # maximum value for subproblem calculation

    # Base case for sub-problems with zero items (i=0).
    falses = [False for v in range(Vmax+1)]
    infins = [INF for v in range(Vmax+1)]
    C.append(falses)   # row for i=0
    A.append(infins)   # row for i=0
    A[0][0] = 0        # with zero items and V=0, minimum weight W=0

    # Calculate minimum weight solutions for the subproblems of the knapsack
    # configuration.
    print(f'Parameter for outer iteration: {n}, for inner iteration {Vmax}')
    for i in range(1, n+1):   # loop over items
        #print(f'outer iteration = {i}')
        c = []   # comparison flag for v=0 for current i
        a = []   # subproblem results for current i
        for v in range(Vmax+1):   # loop over knapsack values
            a1 = A[i-1][v]
            if v-values[i-1] < 0:
                a2 = weights[i-1]
            else:
                a2 = A[i-1][v-values[i-1]] + weights[i-1]
            # Which case are we in?
            if a2 < a1:
                c.append(True)
                a.append(a2)
            else:
                c.append(False)
                a.append(a1)
        C.append(c)
        A.append(a)

    return A, C

def knapsack_weight_calc(V, vmax, values, A, C):
    """
    Calculate an optimum Knapsack configuration using Dynamic Programming,
    based on the already solved subproblems.
    
    Arguments:
        V (int):
            Knapsack value that should be met.
            We assume that the Knapsack value is non-negative and integer.
        vmax (int):
            Maximum value per Knapsack item.
            We assume that vmax is positive and integer.
        values (list):
            List of values of the Knapsack items.
            We assume that all values are positive and integer.
            We assume that there are the items 1 ... n.
        A (list):
            Subproblem solutions of the Knapsack configuration.
        C (list):
            Boolean flags for comparison results of the Knapsack configuration.
    
    Returns:
        w (int):
            Minimum weight of the optimum Knapsack configuration.
        v (int):
            Knapsack value that has been reached with the optimum Knapsack
            configuration.
        items (list):
            List of items belonging to the optimum Knapsack configuration.
    """

    # Initialize data structures.
    n = len(values)   # number of knapsack items
    w = INF           # minimum weight of knapsack configuration
    items = []

    # Base case for V > n*vmax:
    if V > n*vmax:   # a value more than n*vmax is not achievable
        return INF, 0, []
    # Calculate upper bound for values.
    if V < 0:   # treat negative expected value as zero value
        V = 0

    # Calculate minimum weight of optimum knapsack configuration.
    w = A[n][V]

    # Reconstruct optimum knapsack configuration.
    i, x, v = n, V, 0
    while x > 0 and i > 0:   # loop over items and knapsack capacities
        if C[i][x]:
            items.insert(0, i)
            x -= values[i-1]
            v += values[i-1]
            i -= 1
        else:
            i -= 1

    return w, v, items

def read_list(file_name):
    """
    Read source data of Knapsack parameters.
    The first row contains the Knapsack capacity and the number of items.
    Every other row contains the values and weigths of a Knapsack item.
    
    Arguments:
        file_name (str):
            File name to be read.
    
    Returns:
        status (int):
            '0' indicates successful processing, '1' that an error ocurred.
        n_items (int):
            Number of Knapsack items.
            We assume that there are the items 1 ... n.
        capacity (int):
            Knapsack capacity.
            We assume that the capacity is non-negative.
        vmax (int):
            Maximum value per Knapsack item.
            Will be positive and integer, if all values are.
        values (list):
            List of values of the Knapsack items.
            We assume that all values are positive and integer.
        weights (list):
            List of weights of the Knapsack items.
            We assume that all values are non-negative.
    """

    # Initialize structures.
    values   = []
    weights  = []
    n_items  = 0
    capacity = 0
    vmax     = 0
    # Read list data from file.
    # Each row represents 1 item of the list.
    try:
        with open(file_name, 'r') as f:
            # Read data from file.
            raw_data = f.readlines()
            n = len(raw_data)
            n_items = n - 1
            # Evaluate first line.
            row = raw_data[0].split()
            capacity = int(row[0])
            # Evaluate all other lines.
            for i in range(1, n):   # line number
                # Evaluate current line.
                row = raw_data[i].split()
                value  = int(row[0])
                weight = int(row[1])
                # Update maximum value.
                if value > vmax:
                    vmax = value
                # Append the values to the list of values.
                values.append(value)
                # Append the weights to the list of weights.
                weights.append(weight)
        return 0, n_items, capacity, vmax, values, weights
    except:
        return 1, n_items, capacity, vmax, values, weights

# Main programm
def runMe():
    file_name = 'knapsack_small.txt'

    tic = time.perf_counter()
    sys.stdout.write('\nReading input data for Knapsack Problem.\n')
    sys.stdout.flush()
    status, n_items, capacity, vmax, values, weights = read_list(file_name)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of items: ' + str(n_items) +
                     ', Knapsack capacity: ' + str(capacity) + '\n')
    sys.stdout.flush()
    sys.stdout.write('\nCalculate optimum Knapsack configuration.\n')
    sys.stdout.flush()
    # Calculate the subproblems for the knapsack configuration.
    sys.stdout.write('Calculating subproblems.\n')
    sys.stdout.flush()
    A, C = knapsack_subproblems_calc(vmax, values, weights)
    # Test for optimum reachable knapsack value.
    sys.stdout.write('Searching for optimum reachable Knapsack value.\n')
    sys.stdout.flush()
    if capacity <= 0:
        w, items = 0, []
    else:
        found = False
        Vmax = n_items*vmax
        v_2, v_1 = Vmax//2, 0
        while not found:
            w, v, items = knapsack_weight_calc(v_2, vmax, values, A, C)
            print('search value =', v_2, 'weight =', w,
                  'remaining capacity =', capacity-w)
            if w > capacity:
                v_2, v_1 = int(v_2 - abs(v_2-v_1)/2), v_2
            elif abs(v_2-v_1) > 1:
                v_2, v_1 = int(v_2 + abs(v_2-v_1)/2), v_2
                if v_2 > Vmax:
                    v_2 = Vmax
            else:
                found = True
    # Optimum knapsack value according to assignment.
    sys.stdout.write('\nMinimum Knapsack weight: ' + str(w) +
                     ' for value: ' + str(v) + '\n')
    sys.stdout.flush()
    sys.stdout.write('Optimum Knapsack contains the items:\n')
    sys.stdout.write(str(items) + '\n')
    sys.stdout.flush()
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
