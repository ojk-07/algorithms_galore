# -*- coding: utf-8 -*-
"""
Median maintenance algorithm for calculating the median of a stream of numbers.

A program for Stanford Algorithms Specialization 2 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #3 in the Course
https://www.coursera.org/learn/algorithms-graphs-data-structures/home/module/3
"""

import heaptools as ht
import bnodes as bn
import treetools as tt
import time
import sys

def medians_by_heap(numbers):
    """
    Calculate medians from stream of numbers and aggregate into a checksum.

    Two heaps are used, a maximum heap lo and a minimum heap hi.
    Invariants:
        - All numbers in lo must be <= the numbers in hi.
        - The size of hi must be <= the size of lo.
        - The size of lo must <= the size of hi + 1.
    Then, we can always take the maximum element of lo as the median
    (whith the understanding that for N even numbers, the median shall be the
    the N/2-th number).

    Arguments:
        numbers (list):
            List of numbers.

    Returns:
        checksum (int):
            Checksum of medians = sum of all medians mod 10000.
    """

    # Initialize data.
    mod = 10000
    checksum = 0

    # Initialize heaps.
    lo = ht.heap([], mintype=False)
    hi = ht.heap([], mintype=True)

    # Process stream of numbers.
    for i in numbers:
        len_lo, len_hi = len(lo.e), len(hi.e)
        # Add number i to the correct heap.
        if len_hi == 0 or i <= hi.e[0]:
            # Number can be added to heap lo.
            if len_lo <= len_hi:
                # Add number to lo, which is also okay for the balance.
                lo.insert(i)
                len_lo += 1
            else:
                # Heap lo must contain at least 1 number.
                if i >= lo.e[0]:
                    # Number can also be added to heap hi.
                    # We will add to heap hi, to maintain balance.
                    hi.insert(i)
                    len_hi += 1
                else:
                    # Number must be added to heap lo.
                    lo.insert(i)
                    len_lo += 1
        else:
            # Number must be added to heap hi.
            hi.insert(i)
            len_hi += 1
        # Rebalance heaps if necessary.
        if len_lo > len_hi + 1:
            # Shift maximum from heap lo to heap hi.
            m = lo.deletem()
            hi.insert(m)
        elif len_lo < len_hi:
            # Shift minimum from heap hi to heap lo.
            m = hi.deletem()
            lo.insert(m)
        # Get current median from heap lo.
        median = lo.e[0]
        #print('Median =', median)
        # Update checksum.
        checksum = (checksum + median) % mod
    return checksum

def medians_by_tree(numbers):
    """
    Calculate medians from stream of numbers and aggregate into a checksum.

    A binary search tree is used to calculate the median statistic.

    Arguments:
        numbers (list):
            List of numbers.

    Returns:
        checksum (int):
            Checksum of medians = sum of all medians mod 10000.
    """

    # Initialize data.
    mod = 10000
    checksum = 0

    # Initialize btree.
    t = tt.btree(tree_type='avl')

    # Process stream of numbers.
    for i, j in enumerate(numbers):
        t.insert(bn.bnode(j), unique=False)
        status, n = t.select(i//2+1)
        median = n.key
        #print('Median =', median)
        # Update checksum.
        checksum = (checksum + median) % mod
    return checksum

def read_list(file_name):
    """
    Read source data of numbers to calculate the median for.
    Every contains just one number.

    Arguments:
        file_name (str):
            File name to be read.

    Returns:
        status (int):
            '0' indicates successful processing, '1' that an error ocurred.
        numbers (list):
            List of numbers.
    """

    # Initialize structures.
    numbers = []
    # Read list data from file.
    # Each row represents one number of the list.
    try:
        with open(file_name, 'r') as f:
            # Read data from file.
            raw_data = f.readlines()
            n = len(raw_data)
            # Evaluate all lines.
            for i in range(n):   # line number
                # Evaluate current line.
                numbers.append(int(raw_data[i]))
        return 0, numbers
    except:
        return 1, numbers

# Main programm
def runMe():
    file_name = 'Median.txt'

    tic = time.perf_counter()
    sys.stdout.write('\nReading input data for Median Maintenance.\n')
    sys.stdout.flush()
    status, numbers = read_list(file_name)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of numbers: ' + str(len(numbers)) + '\n')
    sys.stdout.flush()
    sys.stdout.write('\nCalculate medians.\n')
    sys.stdout.flush()
    checksum = medians_by_heap(numbers)
    #checksum = medians_by_tree(numbers)
    sys.stdout.write('\nChecksum = ' + str(checksum) + '\n')
    sys.stdout.flush()
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
