# -*- coding: utf-8 -*-
"""
Knapsack algorithm based on Dynamic Programming for positive weights,
non-negative item values and non-negative Knapsack capacity W.

In this version, it is not necessary that the weights and capacity W are
integer. However, the algorithm is only fast if there are not too many
possible weight combinations not greater than W.
Running time: O(n(W/wmin) log (W/wmin)) instead of O(nW), due to the calculation
of the relevant capacities and finding the relevant capacities during the
DP subproblem calculation.

A program for Stanford Algorithms Specialization 3 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #4 in the Course
https://www.coursera.org/learn/algorithms-greedy/home/module/4
"""

import time
import sys
import bisect
from sortedcontainers import SortedSet

def knapsack_calc(W, values, weights):
    """
    Calculate an optimum Knapsack configuration using Dynamic Programming.
    
    In this optimized version, only the subproblems are calculated and stored
    for capacities that will be visited.
    The determination of relevant capacities is done tracing back from the
    last item and capacity W.
    
    Arguments:
        W (int or float):
            Knapsack capacity.
            We assume that the capacity is non-negative.
        values (list):
            List of values of the Knapsack items.
            We assume that all values are non-negative.
            We assume that there are the items 1 ... n.
        weights (list):
            List of weights of the Knapsack items.
            We assume that all values are positive.
    
    Returns:
        V (int):
            Value of the optimum Knapsack configuration.
        items (list):
            List of items belonging to the optimum Knapsack configuration.
    """

    # Initialize data structures.
    n = len(values)   # number of knapsack items
    V = 0             # value of knapsack configuration
    A     = []        # results for sub-problems A[i][w]
    C     = []        # boolean flags for comparison results
    items = []

    # Base case for W <= 0:
    if W <= 0:   # for non-positive knapsack capacity, the value is 0
        return 0, []

    # Determine relevant capacities for the subproblems using a SortedSet.
    print('Calculating relevant capacities ...')
    capacities = SortedSet([W])   # knapsack capacity
    for i in range(n, 0, -1):   # loop over items
        w1 = weights[i-1]   # weight of item i
        # Combine previous capacities with weight of item i.
        new_capacities = SortedSet([])
        for j in range(len(capacities)):
            w2 = capacities[j] - w1
            if w2 > 0:
                new_capacities.add(w2)
            else:
                continue
        capacities.update(new_capacities)
        print('item =', i, '#capacities =', len(capacities))
    # Convert sorted set into normal list.
    capacities = list(capacities)
    m = len(capacities)   # number of relevant distinct capacities
    wmin, wmax = capacities[0], capacities[m-1]

    # Calculate value of optimum knapsack configuration.
    print('Calculating optimum Knapsack configuration ...')
    for i in range(1, n+1):   # loop over items
        print('item =', i)
        c, a = {}, {}   # dictionaries for subproblems at relevent capacities
        for j in range(m):   # loop over relevant capacities
            w1 = capacities[j]
            # Determine value of subproblem for case 1.
            if i > 1:
                a1 = A[i-2][w1]
            else:
                a1 = 0
            # Determine value of subproblem for case 2.
            w2 = w1 - weights[i-1]
            if w2 >= wmin:
                # Determine largest relevant capacity <= w2.
                k = bisect.bisect_right(capacities, w2) - 1
                w3 = capacities[k]
            elif w2 >= 0:
                w3 = 0
            else:
                w3 = w2
            # Look-up value of subproblem for case 2.
            if w3 < 0:
                a2 = 0
            elif w3 == 0 or i == 1:
                a2 = values[i-1]
            else:
                a2 = A[i-2][w3] + values[i-1]
            # Which case are we in?
            if a2 > a1:
                c[w1] = True
                a[w1] = a2
            else:
                c[w1] = False
                a[w1] = a1
        C.append(c)
        A.append(a)
    V = A[n-1][wmax]

    # Reconstruct optimum knapsack configuration.
    print('Reconstructing optimum Knapsack configuration ...')
    i, w = n, wmax
    while w >= wmin and i > 0:   # loop over items and knapsack capacities
        print('item =', i, 'capacity =', w)
        if C[i-1][w]:
            items.insert(0, i)
            w -= weights[i-1]
            i -= 1
        else:
            i -= 1

    return V, items

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
        capacity (int or float):
            Knapsack capacity.
            We assume that the capacity is non-negative.
        values (list):
            List of values of the Knapsack items.
            We assume that all values are non-negative.
        weights (list):
            List of weights of the Knapsack items.
            We assume that all values are positive.
    """

    # Initialize structures.
    values   = []
    weights  = []
    n_items  = 0
    capacity = 0
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
                # Append the values to the list of values.
                values.append(value)
                # Append the weights to the list of weights.
                weights.append(weight)
        return 0, n_items, capacity, values, weights
    except:
        return 1, n_items, capacity, values, weights

# Main program.
def runMe():
    file_name = 'knapsack1.txt'
    #file_name = 'knapsack_big.txt'

    tic = time.perf_counter()
    sys.stdout.write('\nReading input data for Knapsack Problem.\n')
    sys.stdout.flush()
    status, n_items, capacity, values, weights = read_list(file_name)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of items: ' + str(n_items) +
                     ', Knapsack capacity: ' + str(capacity) + '\n')
    sys.stdout.flush()
    sys.stdout.write('\nCalculate optimum Knapsack configuration.\n')
    sys.stdout.flush()
    value, items = knapsack_calc(capacity, values, weights)
    # Optimum knapsack value according to assignment.
    sys.stdout.write('\nMaximum Knapsack value: ' + str(value) + '\n')
    sys.stdout.flush()
    #sys.stdout.write('Optimum Knapsack contains the items:\n')
    #sys.stdout.write(str(items) + '\n')
    #sys.stdout.flush()
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
