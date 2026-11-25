# -*- coding: utf-8 -*-
"""
Maximum-weight independent set of a path graph for non-negative weights,
based on Dynamic Programming.
Running time: O(n).

A program for Stanford Algorithms Specialization 3 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #3 in the Course
https://www.coursera.org/learn/algorithms-greedy/home/module/3
"""

import time
import sys

def mwis_calc(weights):
    """
    Calculate a maximum-weight independent set for a path graph using
    Dynamic Programming.
    
    Arguments:
        weights (list):
            List of weights for vertices.
            We assume that there are the vertices 1 ... n and
            that all weights are non-negative.
    
    Returns:
        wsum (int):
            Weight sum of the maximum-weight independent set.
        mwis (list):
            List of vertices belong to a maximum-weight independent st.
    """

    # Initialize data structures.
    mwis = []                # boolean flags for independent set
    comp = [False, True]     # boolean flags for comparison results
    sums = [0, weights[0]]   # optimal weight sums
    n    = len(weights)      # number of vertices

    # Calculate optimal weight sums.
    for i in range(2, n+1):
        s = sums[i-2] + weights[i-1]
        if s > sums[i-1]:
            comp.append(True)
            sums.append(s)
        else:
            comp.append(False)
            sums.append(sums[i-1])
    wsum = sums[n]

    # Reconstruct independent set.
    i = n
    while i>0:
        if comp[i]:
            mwis.insert(0, True)
            i -= 2
            if i > 0:
                mwis.insert(0, False)
        else:
            mwis.insert(0, False)
            i -= 1
    # Insert flag for element with index 0.
    mwis.insert(0, False)

    return wsum, mwis

def read_list(file_name):
    """
    Read source data of weights for vertices.
    Every row contains the weigth of a vertex.
    
    Arguments:
        file_name (str):
            File name to be read.
    
    Returns:
        status (int):
            '0' indicates successful processing, '1' that an error ocurred.
        n_vertices (int):
            Number of vertices.
            We assume that there are the vertices 1 ... n.
        weights (list):
            List of weights for vertices.
            We assume that all weights are non-negative.
    """

    # Initialize structures.
    weights = []
    n_vertices = 0
    # Read list data from file.
    # Each row represents 1 item of the list.
    try:
        with open(file_name, 'r') as f:
            # Read data from file.
            raw_data = f.readlines()
            n = len(raw_data)
            n_vertices = n - 1
            # Evaluate all lines.
            for i in range(1, n):   # line number
                # Evaluate current line.
                row = raw_data[i].split()
                weight = int(row[0])
                # Append the weight to the list of weights.
                weights.append(weight)
        return 0, n_vertices, weights
    except:
        return 1, n_vertices, weights

# Main programm
def runMe():
    file_name = 'mwis.txt'

    tic = time.perf_counter()
    sys.stdout.write('\nReading input data for path graph.\n')
    sys.stdout.flush()
    status, n_vertices, weights = read_list(file_name)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of vertices: ' + str(n_vertices) + '\n')
    sys.stdout.flush()
    sys.stdout.write('\nCalculate Maximum-Weight Independent Set.\n')
    sys.stdout.flush()
    wsum, mwis = mwis_calc(weights)
    # Calculate bit pattern for independent set.
    pattern = ''
    for i in range(1, n_vertices+1):
        if mwis[i]:
            pattern += '1'
        else:
            pattern += '0'
    # Calculate result bit pattern according to assignment.
    indizes = [1, 2, 3, 4, 17, 117, 517, 997]
    results = ''
    for i in indizes:
        if n_vertices >= i:
            if mwis[i]:
                results += '1'
            else:
                results += '0'
    sys.stdout.write('\nBit pattern for assignment for weight sum = ' +
                     str(wsum) + ': ' + results + '\n')
    sys.stdout.flush()
    #sys.stdout.write('Maximum-Weight Independent Set:\n')
    #sys.stdout.write(pattern + '\n')
    #sys.stdout.flush()
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
