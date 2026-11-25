# -*- coding: utf-8 -*-
"""
Knapsack algorithm based on Dynamic Programming for positive integer weights
and non-negative item values, and non-negative integer Knapsack capacity W.
Running time: O(nW).

A program for Stanford Algorithms Specialization 3 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #4 in the Course
https://www.coursera.org/learn/algorithms-greedy/home/module/4
"""

import time
import sys

def knapsack_calc(W, values, weights):
    """
    Calculate an optimum Knapsack configuration using Dynamic Programming.
    
    Arguments:
        W (int):
            Knapsack capacity.
            We assume that the capacity is non-negative and integer.
        values (list):
            List of values of the Knapsack items.
            We assume that all values are non-negative.
            We assume that there are the items 1 ... n.
        weights (list):
            List of weights of the Knapsack items.
            We assume that all values are positive and integer.
    
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
    # Base case for sub-problems with zero items (i=0).
    falses = [False for w in range(W+1)]
    zeros  = [0 for w in range(W+1)]
    C.append(falses)   # row for i=0
    A.append(zeros)    # row for i=0

    # Calculate value of optimum knapsack configuration.
    for i in range(1, n+1):   # loop over items
        c = [False]   # comparison flag for w=0 for current i
        a = [0]       # sub-problem result for w=0 for current i
        for w in range(1, W+1):   # loop over knapsack capacities
            a1 = A[i-1][w]
            if w-weights[i-1] < 0:
                a2 = 0
            else:
                a2 = A[i-1][w-weights[i-1]] + values[i-1]
            # Which case are we in?
            if a2 > a1:
                c.append(True)
                a.append(a2)
            else:
                c.append(False)
                a.append(a1)
        C.append(c)
        A.append(a)
    V = A[n][W]

    # Reconstruct optimum knapsack configuration.
    i, w = n, W
    while w > 0 and i > 0:   # loop over items and knapsack capacities
        if C[i][w]:
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
        capacity (int):
            Knapsack capacity.
            We assume that the capacity is non-negative and integer.
        values (list):
            List of values of the Knapsack items.
            We assume that all values are non-negative.
        weights (list):
            List of weights of the knapsack items.
            We assume that all values are positive and integer.
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
    #file_name = 'knapsack_small.txt'
    file_name = 'knapsack.txt'

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
