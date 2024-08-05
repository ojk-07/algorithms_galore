# -*- coding: utf-8 -*-
"""
Invert Count algorithm.

A program for Stanford Algorithms Specialization written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #2 in the Course
https://www.coursera.org/learn/algorithms-divide-conquer/home/module/2
"""

import time

def sort_and_count(a, verbose=False):
    """
    Sort a list with n elements and count the number of inversions
    in time n*log(n).

    Arguments:
        a (list):
            List of numbers with inversions.
        verbose (bool):
            More intermediate output is written when True.

    Returns:
        m (int):
            Number of inversions in the list a.
        b (list):
            Sorted list of numbers with stable sorting, i.e. the order of
            items with equal sort criterion stays unchanged.
        """

    # Determine length of list for sorting and counting inversions.
    n = len(a)

    # Split list into 2 parts.
    # The general case is considered here, n can also be odd.
    n2 = (n // 2)

    if n2 == 0:
        # This is the base case, where the list a already contains only
        # 1 number. This list has by definition 0 inversions and is sorted.
            if verbose:
                print('Base case: {0}'.format(a))
            m, b = 0, a
            return m, b
            
    # The first part of the splitted list takes the remaining numbers.
    n1 = n - n2

    # Split the list into smaller parts.
    a1, a2 = a[:n1], a[n1:]
    if verbose:
        print('Split: {0} {1}'.format(a1, a2))

    # Get the number of inversions within the sub lists a1 and a2.
    m1, b1 = sort_and_count(a1, verbose=verbose)
    m2, b2 = sort_and_count(a2, verbose=verbose)
    m = m1 + m2
    if verbose:
        print('Inversions in sub lists: {0} {1}'.format(m1, m2))

    # Merge the smaller lists into the combined sorted list and
    # count split inversions.
    b = []
    i, j = 0, 0
    for k in range(n):
        if (i < n1 and j < n2 and b1[i] <= b2[j]) or (i < n1 and j >= n2):
            b.append(b1[i])
            i += 1
        else:
            b.append(b2[j])
            m += n1 - i
            j += 1
    if verbose:
        print('Inversions in list: {0}'.format(m))

    return m, b

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
    #a = [3, 2, 5, 4]   # 2 inversions
    #a = [3, 9, 2, 7, 7, 5, 4, 6, 9]    # 14 inversions

    # Read the list input from file.
    #file_name = 'TestArray01.txt'   # 14 inversions
    #file_name = 'TestArray02.txt'   # 15 inversions
    file_name = 'IntegerArray.txt'   # 2407905288 inversions
    status, a = read_list(file_name)

    # Sort the list.
    tic = time.perf_counter()
    m, b = sort_and_count(a, verbose=verbose)
    toc = time.perf_counter()
    #print(b)   # for test purposes, should be a sorted list
    print('Number of inversions in the list: {0}'.format(m))
    print('Execution time: {0} ms'.format((toc - tic) * 1000))
