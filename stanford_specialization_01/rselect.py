# -*- coding: utf-8 -*-
"""
RSelect algorithm.

A program for Stanford Algorithms Specialization written by Oliver Kroneisen,
oliver@kroneisen.net

"""

import time
import random as rd

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
    ip = il + int(rd.random()*(ir + 1 - il))
    return ip

    # Middle element.
    #ip = (ir + il) // 2
    #return ip

    # Median of three.
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
            # Swap a[j] with current a[i], if necessary.
            if j > i:
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

def select(a, il, ir, istat, verbose=False):
    """
    Select the ith statistic from the list a between index il (inclusive) and
    index ir (inclusive).
    The operations on list a run in-place.

    Arguments:
        a (list):
            List of numbers to be sorted.
            Will be changed in-place during the method.
        il (int):
            Left index of the segment to process.
        ir (int):
            Right index of the segment to process.
        istat (int):
            The ith statistic to be selected.
        verbose (bool):
            More intermediate output is written when True.

    Returns:
        value (int):
            The value of the ith statistic.
            The list a will be changed in-place during this method.
        """

    if ir == il:
        # This is the base case, when the segment of the list to select from
        # already contains only 1 number. This is the correct statistic.
            value = a[il]
            if verbose:
                print('Base case: {0}'.format(a[il:ir + 1]))
            return value

    # Choose a pivot index and number.
    ip = choose_pivot(a, il, ir, verbose=verbose)
    if verbose:
        print('Pivot index: {0}, Pivot number {1}'.format(ip, a[ip]))

    # Partition list a in the segment [il, ir].
    ip = partion(a, ip, il, ir, verbose=verbose)

    # Select the correct segment for the next selection.
    # Keep in mind that all index values are counted with respect to the
    # size of the original list, not the reduced lists!
    if ip + 1 == istat:
        # The ith statistic has been found.
        value = a[ip]
    elif ip + 1 > istat:
        # The ith statistic is in the left segment.
        value = select(a, il, ip - 1, istat, verbose=verbose)
    else:
        # The ith statistic is in the right segment.
        value = select(a, ip + 1, ir, istat, verbose=verbose)

    return value

def rselect(a, istat, verbose=False):
    """
    Recursive selection of the ith statistic from a list of n numbers in
    average time n using the RSelect algorithm.
    In the worst case, the algorithm runs in time n^2.
    A very positive feature of RSelect is that the factor to the asymptotic
    time is small, and that the selection happens in-place without requiring
    addtitional memory.

    Arguments:
        a (list):
            List of numbers to be sorted.
        istat (int):
            The ith statistic to be selected.
        verbose (bool):
            More intermediate output is written when True.

    Returns:
        value (int):
            The value of the ith statistic.
            The list a will be changed in-place during this method.
        """

    # Initialize index values.
    il, ir = 0, len(a) - 1

    # Ensure that the list contains at least 1 number.
    assert ir >= 0

    # Select from the entire list, i.e. in the segment [il, ir].
    value = select(a, il, ir, istat, verbose=verbose)

    return value

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
    istat = 4711

    # Read the list input from file.
    file_name = 'IntegerArray.txt'
    status, a = read_list(file_name)

    # Sort the list.
    #print('Initial list: {0}'.format(a))   # for test purposes
    tic = time.perf_counter()
    value = rselect(a, istat, verbose=verbose)
    toc = time.perf_counter()
    print('The value of the {0}th statistic is {1}'.format(istat, value))
    print('Execution time: {0} ms'.format((toc - tic) * 1000))