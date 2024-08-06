# -*- coding: utf-8 -*-
"""
Merge Sort algorithm.

A program for Stanford Algorithms Specialization written by Oliver Kroneisen,
oliver@kroneisen.net
"""

import time

def mergesort(a, verbose=False):
    """
    Recursive stable sorting of a list of n numbers in time n*log(n) using the
    Merge Sort algorithm, proposed 1945 by John von Neumann.

    Arguments:
        a (list):
            Unsorted list of numbers.
        verbose (bool):
            More intermediate output is written when True.

    Returns:
        b (list):
            Sorted list of numbers with stable sorting, i.e. the order of
            items with equal sort criterion stays unchanged.
        """

    # Determine length of list to be sorted.
    n = len(a)

    # Split list into 2 parts.
    # The general case is considered here, n can also be odd.
    n2 = (n // 2)

    if n2 == 0:
        # This is the base case, where the list a already contains
        # only 1 number. This list is by definition sorted.
            if verbose:
                print('Base case: {0}'.format(a))
            b = a
            return b
            
    # The first part of the splitted list takes the remaining numbers.
    n1 = n - n2

    # Split the list into smaller parts.
    a1, a2 = a[:n1], a[n1:]
    if verbose:
        print('Split: {0} {1}'.format(a1, a2))

    # Sort the smaller lists recursively.
    b1 = mergesort(a1, verbose=verbose)
    b2 = mergesort(a2, verbose=verbose)
    if verbose:
        print('Interim lists: {0} {1}'.format(b1, b2))

    # Merge the smaller lists into the combined sorted list.
    b = []
    i, j = 0, 0
    for k in range(n):
        if (i < n1 and j < n2 and b1[i] <= b2[j]) or (i < n1 and j >= n2):
            b.append(b1[i])
            i += 1
        else:
            b.append(b2[j])
            j += 1
    if verbose:
        print('Interim list: {0}'.format(b))

    return b

if __name__ == '__main__':

    # Set parameters for calculation.
    verbose = False
    #a = [3, 2, 5, 4]
    a = [3, 9, 2, 7, 7, 5, 4, 6, 9]

    # Sort the list.
    tic = time.perf_counter()
    b = mergesort(a, verbose=verbose)
    toc = time.perf_counter()
    print('The unsorted list a: {0}'.format(a))
    print('The sorted list b:   {0}'.format(b))
    print('Execution time:      {0} ms'.format((toc - tic) * 1000))
