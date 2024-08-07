# -*- coding: utf-8 -*-
"""
Quicksort algorithm.

A program for Stanford Algorithms Specialization written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #3 in the Course
https://www.coursera.org/learn/algorithms-divide-conquer/home/module/3
"""

import time
import random as rd
#import numpy as np

def choose_pivot(a, il, ir, verbose=False):
    """
    Select the index ip of the pivot number within the list segment between
    index il (inclusive) and index ir (inclusive).

    Arguments:
        a (list):
            List of numbers to be sorted.
        il (int):
            Left index of the segment to process.
        ir (int):
            Right index of the segment to process.
        verbose (bool):
            More intermediate output is written when True.

    Returns:
        ip (int):
            Index of the privot number. il <= ip <= ir.
        """

    # Ensure that the list segment contains at least 1 number.
    assert ir >= il

    # Select the pivot index.
    # Note that random.random is 20 times faster than random.randint, and
    # numpy.random.randint would be even much slower.
    ip = il + int(rd.random()*(ir + 1 - il))
    #ip = rd.randint(il, ir)
    #ip = np.random.randint(il, ir)
    #return ip

    # Middle element.
    ip = (ir + il) // 2
    #return ip
    # Direction for excercise 1. (= 162085)
    ip = il
    #return ip
    # Direction for excercise 2. (= 164123)
    ip = ir
    #return ip
    # Direction for excercise 3, median of three. (= 138382)
    im = (ir + il) // 2
    if a[il] <= a[im] <= a[ir] or a[ir] <= a[im] <= a[il]:
        ip = im
    elif a[im] <= a[il] <= a[ir] or a[ir] <= a[il] <= a[im]:
        ip = il
    else:
        ip = ir
    return ip

def partion(a, ip, il, ir, verbose=False):
    """
    Partition a list of numbers around a pivot number p within the list segment
    between index il (inclusive) and index ir (inclusive), so that all numbers
    to the left of p in the result list are smaller than p, and all numbers
    to the right of p are bigger or equal to p.
    The rountine is linear in time, and runs in-place.

    Arguments:
        a (list):
            List of numbers to be sorted.
            Will be changed in-place during the method.
        ip (int):
            Index of the privot number. il <= ip <= ir.
        il (int):
            Left index of the segment to process.
        ir (int):
            Right index of the segment to process.
        verbose (bool):
            More intermediate output is written when True.

    Returns:
        ip_new (int):
            New Index of the privot number. il <= ip <= ir.
        """

    # Ensure that the pivot number is within the segment [il, ir].
    assert il <= ip and ip <= ir
    if verbose:
        print('List for partitioning: {0}'.format(a[il:ir + 1]))

    # Swap the pivot number to the left of the segment [il, ir] if necessary.
    p = a[ip]
    ip_new = ip
    if ip > il:
        t      = a[il]
        a[il]  = a[ip]
        a[ip]  = t
        ip_new = il
        if verbose:
            print('After preprocessing:   {0}'.format(a[il:ir + 1]))

    # Scan the list from left to right for elements that are not partitioned.
    i = il + 1
    for j in range(il + 1, ir + 1):
        if a[j] < p:
            # Swap a[j] with current a[i]. 
            # This could be unnecessary, if j = i, but we ignore this here.
            t    = a[i]
            a[i] = a[j]
            a[j] = t
            # Advance i by 1.
            i += 1
        if verbose:
            print('After step {0}: i={1}, j={2} {3}'.format(j - il, i, j + 1,
                                                            a[il:ir + 1]))

    # Finally, swap the pivot number a[il] with a[i-1].
    if i - 1 > il:
        t        = a[i - 1]
        a[i - 1] = a[il]
        a[il]    = t
        ip_new   = i - 1
    if verbose:
        print('After final step:      {0}'.format(a[il:ir + 1]))

    return ip_new

def sort(a, il, ir, verbose=False):
    """
    Sort the list a between index il (inclusive) and index ir (inclusive).
    The operations on list a run in-place.

    Arguments:
        a (list):
            List of numbers to be sorted.
            Will be changed in-place during the method.
        il (int):
            Left index of the segment to process.
        ir (int):
            Right index of the segment to process.
        verbose (bool):
            More intermediate output is written when True.

    Returns:
        nc (int):
            Number of comparisions that have happened.
            The list a will be changed in-place during this method.
        """

    # Initialize the count of number nc of comparisons.
    nc = 0

    if ir == il:
        # This is the base case, where the to be sorted segment of the list
        # already contains only 1 number. This segment is by definition sorted.
            if verbose:
                print('Base case: {0}'.format(a[il:ir + 1]))
            return nc

    # Choose a pivot index and number.
    ip = choose_pivot(a, il, ir, verbose=verbose)
    if verbose:
        print('Pivot index: {0}, Pivot number {1}'.format(ip, a[ip]))

    # Partition list a in the segment [il, ir].
    ip = partion(a, ip, il, ir, verbose=verbose)
    nc += ir - il

    # Sort the segment left of the new pivot number, if necessary.
    if ip > il:
        ncl = sort(a, il, ip - 1, verbose=verbose)
        nc += ncl

    # Sort the segment right of the new pivot number, if necessary.
    if ip < ir:
        ncr = sort(a, ip + 1, ir, verbose=verbose)
        nc += ncr

    return nc

def quicksort(a, verbose=False):
    """
    Recursive unstable sorting of a list of n numbers in average time n*log(n)
    using the Quick Sort algorithm, proposed 1960 by Tony Hoare.
    In the worst case, the algorithm runs in time n^2.
    A very positive feature of Quick Sort is that the factor to the asymptotic
    time is small, and that the sorting happens in-place without requiring
    addtitional memory.

    Arguments:
        a (list):
            List of numbers to be sorted.
        verbose (bool):
            More intermediate output is written when True.

    Returns:
        a (list):
            The list a will be changed in-place during this method.
        """

    # Initialize index values.
    il, ir = 0, len(a) - 1

    # Ensure that the list contains at least 1 number.
    assert ir >= 0

    # Sort the entire list, i.e. in the segment [il, ir].
    nc = sort(a, il, ir, verbose=verbose)
    print('Number of comparisions: {0}'.format(nc))

    return a

def read_list(file_name):
    # Read list data from file.
    # Each row represents 1 item of the list.
    try:
        with open(file_name, 'r') as f:
            raw_data = f.read()
            int_list = [int(x) for x in raw_data.split()]
        return 0, int_list
    except:
        int_list = []
        return 1, int_list

if __name__ == '__main__':

    # Set parameters for calculation.
    verbose = False
    #a = [3, 2, 5, 4]
    #a = [3, 9, 2, 7, 7, 5, 4, 6, 9]
    #a = [3, 9, 2, 1, 7, 5, 4, 6, 8]

    # Read the list input from file.
    #file_name = 'TestArray01.txt'
    #file_name = 'TestArray02.txt'
    #file_name = 'IntegerArray.txt'
    file_name = 'QuickSort.txt'
    status, a = read_list(file_name)

    # Sort the list.
    #print('Initial list: {0}'.format(a))   # for test purposes
    tic = time.perf_counter()
    a = quicksort(a, verbose=verbose)
    toc = time.perf_counter()
    #print('Sorted list: {0}'.format(a))
    print('Execution time: {0} ms'.format((toc - tic) * 1000))