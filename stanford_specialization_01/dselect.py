# -*- coding: utf-8 -*-
"""
DSelect algorithm.

A program for Stanford Algorithms Specialization written by Oliver Kroneisen,
oliver@kroneisen.net
"""

import time, copy

class Elem:
    """
    Class to represent elements to be sorted.
    
    Attributes:
        key (int): key value for sorting, does not have to be unique
        label (str): element label, e.g. external name
        index (int): index of element, e.g. in an array
    """

    def __init__(self, key, label, index, index2):
        self.key = key         # key or value of the element
        self.label = label     # label of the element
        self.index = index     # index in the parent list
        self.index2 = index2   # index in the current list
    
    def __copy__(self):
        return Elem(self.key, self.label, self.index, self.index2)

    def __repr__(self):
        return str(self)

    def __str__(self):
        if self.label == '':
            #s = '{0}'.format(self.key)   # simple output
            s = '{0}|{1}|{2}'.format(self.key, self.index, self.index2)
        else:
            #s = '{0}|{1}'.format(self.key, self.label)   # simple output
            s = '{0}|{1}|'.format(self.key, self.label)
            s += '{0}|{1}'.format(self.index, self.index2)
        return s

    def __lt__(self, other):
        return self.key < other.key

    def __gt__(self, other):
        return self.key > other.key

    def __le__(self, other):
        return self.key <= other.key

    def __ge__(self, other):
        return self.key >= other.key

    def __eq__(self, other):
        return self.key == other.key

    def __ne__(self, other):
        return self.key != other.key


def mergesort(a, verbose=False):
    """
    Recursive stable sorting of a list of n numbers in time O(n*log(n))
    using the Merge Sort algorithm, proposed 1945 by John von Neumann.
    
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

def findx(a, il, ir):
    """
    Provides the index of a non-minimal element within the list segment
    between index il (inclsuive) and index ir (inclsuive), if it exists,
    and -1 otherwise.
    So, in case of identical key values in the list segment, -1 is returned.
    
    Arguments:
        a (list):
            List of elements to be searched.
        il (int):
            Left index of the segment to process.
        ir (int):
            Right index of the segment to process.
    
    Returns:
        i (int):
            The index of a non-minimal key, it it exists, and -1 otherwise.
    """
    
    # Search for non-minimal element.
    i = il + 1
    while i <= ir and a[i] == a[i - 1]: i += 1
    if i > ir:
        # Impossible to find a non-minimal element, also if il == ir.
        return -1
    elif a[i - 1] < a[i]: return i
    else: return i - 1
    

def partionFU(a, il, ir, p, track=False, verbose=False):
    """
    Partition a list of numbers around a pivot p within the list segment
    between index il (inclusive) and index ir (inclusive), so that all
    numbers to the left of index l in the result list are smaller than p,
    and all numbers at l and to the right of index l are larger or equal to p.
    
    This version of partitioning does not need to know the index where the
    pivot has been stored, just the key value of the pivot is sufficient.
    Note that the pivot will in general not be in the 'right place' in the
    changed list a, which would be at index l.
    Therefore, this partition function cannot be used for DSelect.
    
    It is required that pivot p is a non-minimum element in the list segment!
    
    The rountine is linear in time, i.e. O(n), and runs in-place.
    
    Arguments:
        a (list):
            List of elements to be searched.
            Will be changed in-place during the method.
        il (int):
            Left index of the segment to process.
        ir (int):
            Right index of the segment to process.
        p (int):
            Value of the pivot element.
        verbose (bool):
            More intermediate output is written when True.
    
    Returns:
        l (int):
            The index seperating the list segment into numbers < p
            (to the left of l) and numbers >= p (at l and to the right of l).
        
        List a will be changed in-place during this method.
        Global counter gc is updated each time function partion is called.
    """
    
    # Udate global counter gc.
    global gc
    gc += 1
    
    if verbose: print('List for partitioning: {0}'.format(a[il:ir + 1]))
    
    c = 0           # counter for steps
    l, r = il, ir   # pointer
    
    # Examine a[il:ir + 1] until the pointers l and r meet, or r < 0.
    while l < r and r >= il:
        while(a[l] < p): l += 1
        while(a[r] >= p and r >= il): r -= 1
        if l < r and r >= il:
            # Swap a[l] and a[l].
            if track:
                a[l].index, a[r].index = a[r].index, a[l].index
                a[l], a[r] = a[r], a[l]
            else:
                a[l], a[r] = a[r], a[l]            
        if verbose:
            c += 1
            print('After step {0}: '.format(c) +
                  'l={0}, r={1} {2}'.format(l, r, a[il:ir + 1]))
    
    assert r >= il   # p was the smallest value in the list segememt!
    
    if verbose:
        print('After final step:      {0}'.format(a[il:ir + 1]))
    
    return l

def partion(a, il, ir, ip, track=False, verbose=False):
    """
    Partition a list of numbers around a pivot p within the list segment
    between index il (inclusive) and index ir (inclusive), so that all
    elements to the left of index ip in the result list are smaller than p,
    and all elements to the right of ip are larger or equal to p.
    
    The rountine is linear in time, i.e. O(n), and runs in-place.
    
    With option opt, we allow elements to the left of index ip to be less or
    equal to p, and elements to the right to be larger or equal to p.
    Every second time, when a[j] is compared with p, we switch the elements.
    This speeds up execution significantly in case of many identical numbers
    in the list segment, but does not slow down execution in situations where
    all numbers are unique.
    
    Arguments:
        a (list):
            List of elements to be searched.
            Will be changed in-place during the method.
        il (int):
            Left index of the segment to process.
        ir (int):
            Right index of the segment to process.
        ip (int):
            Index of the privot. il <= ip <= ir.
        track (bool):
            Adjust the index attribute index2 of swapped elements,
            so that index2 reflects the position of the element in
            current list a.
            The attribute index, which reflects the index in the parent list,
            stays unchanged.
        verbose (bool):
            More intermediate output is written when True.
    
    Returns:
        ip_new (int):
            New Index of the privot number. il <= ip <= ir.
        
        List a will be changed in-place during this method.
        Global counter gc is updated each time function partion is called.
    """
    
    # Set optimization parameters.
    opt  = True   # if True, pivot p will be moved amidst same numbers
    
    # Udate global counter gc.
    global gc
    gc += 1
    
    # Ensure that the pivot is within the segment [il, ir].
    assert il <= ip and ip <= ir
    if verbose: print('List for partitioning: {0}'.format(a[il:ir + 1]))
    
    # Swap the pivot to the left of the segment [il, ir] if necessary.
    p = a[ip]
    ip_new = ip
    if ip > il:
        if track:
            a[il].index2, a[ip].index2 = a[ip].index2, a[il].index2
            a[il], a[ip] = a[ip], a[il]
        else:
            a[il], a[ip] = a[ip], a[il]
        ip_new = il
        if verbose:
            print('After preprocessing:   {0}'.format(a[il:ir + 1]))
    
    # Scan the list from left to right for elements that are not partitioned.
    if opt:
        # Every second time, swaps shall also happen when a[j] <= p.
        flag = True
    else:
        flag = False
    i = il + 1
    for j in range(il + 1, ir + 1):
        if (opt and a[j] <= p):
            flag = not flag   # reverse flag
        if a[j] < p or (flag and a[j] <= p):
            # Swap a[j] with current a[i], if necessary.
            if j > i:
                if track:
                    a[i].index2, a[j].index2 = a[j].index2, a[i].index2
                    a[i], a[j] = a[j], a[i]
                else:
                    a[i], a[j] = a[j], a[i]
            # Advance i by 1.
            i += 1
        if verbose:
            print('After step {0}: '.format(j - il) +
                  'i={0}, j={1} {2}'.format(i, j + 1, a[il:ir + 1]))

    # Finally, swap the pivot a[il] with a[i-1].
    if i - 1 > il:
        if track:
            a[i - 1].index2, a[il].index2 = a[il].index2, a[i - 1].index2
            a[i - 1], a[il] = a[il], a[i - 1]
        else:
            a[i - 1], a[il] = a[il], a[i - 1]
        ip_new = i - 1
    if verbose:
        print('After final step:      {0}'.format(a[il:ir + 1]))

    return ip_new

def select(a, il, ir, istat, nred, verbose=False):
    """
    Select the ith statistic from the list a between index il (inclusive) and
    index ir (inclusive).
    
    For the algorithm to work, each element a[i] needs to hold its current
    position in the overall master list (or a value from which this position
    can be derived) in a[i].index.
    In case of nred > 0, the position in the current list can be calculated
    by integer dividing the index value by 5**nred.
    
    Operations on list a run in-place, but additional memory is required
    for internal lists c.
    
    Arguments:
        a (list):
            List of elements to be searched.
            Will be changed in-place during the method.
        il (int):
            Left index of the segment to process.
        ir (int):
            Right index of the segment to process.
        istat (int):
            The ith statistic to be selected.
        nred (int):
            The reduction level, in case select is called for medians
            (level 1), medians of medians (level 2), etc.
            Level 0 is for when called on the original list a.
            This attribute is NOT necessary for the algorithm, it is just
            used in verbose mode to make the output easier to understand.
        verbose (bool):
            More intermediate output is written when True.
    
    Returns:
        ip (int):
            The index of an element whose key value is the ith statistic.
        
        List a will be changed in-place during this method.
    """
    
    # Declare global counter gca for partionings on parent list.
    global gca
    
    if verbose:
        print('*** Select called with istat = {0}, '.format(istat) +
              'nred = {0}'.format(nred))
    if ir == il:
        # This is the base case, when the segment of the list to select from
        # already contains only 1 number. This is then the correct statistic.
        if verbose:
            print('Base case: {0}'.format(a[il:ir + 1]))
        return il
    
    if verbose: print('Input list segment: {0}'.format(a[il:ir + 1]))
    
    # Initialize the additional list of medians.
    c = []

    # Break a into groups of 5, sort each group and select its median.
    ngroups = (ir - il + 1) // 5   # full groups of 5 elements
    ngrest  = (ir - il + 1) %  5   # remaining elements
    # Loop over full groups:
    for k in range(ngroups):
        ik = il + 5 * k
        ak = mergesort(a[ik:ik + 5], verbose=False)
        el = ak[2]   # chosen element
        ck = copy.copy(el)   # shallow copy
        ck.index  = el.index2   # index of parent in parent element's list
        ck.index2 = k   # index of element in new list c
        # Append the median to list c.
        c.append(ck)
    # Special handling of remaining elements.
    if ngrest > 0:
        ik = il + 5 * ngroups
        ak = mergesort(a[ik:ik + ngrest], verbose=False)
        el = ak[(ngrest - 1) // 2]   # chosen element
        ck = copy.copy(el)   # shallow copy
        ck.index  = el.index2   # index of parent in parent element's list
        ck.index2 = ngroups   # index of element in new list c
        # Append the median to list c.
        c.append(ck)
    if verbose:
        print('Medians list: {0}'.format(c))

    # Recursively select the median of medians from list c and use it as pivot.
    ilc = 0
    irc = ngroups - 1
    if ngrest > 0:
        irc += 1
    assert len(c) > 0
    # Get index ic of chosen element in child list c.
    ic = select(c, ilc, irc, (len(c) - 1) // 2 + 1, nred + 1, verbose=verbose)
    # Determine the index of the pivot in the current list a.
    if verbose:
        print('Table c after select(c), istat = {0}, '.format(istat) +
                  'nred = {0}, ic = {1} '.format(nred, ic))
        print('Table c: {0}'.format(c[ilc:irc + 1]))
    ip = (c[ic].index)   # index in current list a
    if verbose:
        print('Pivot from list c: {0}'.format(c[ic]))
        print('Pivot index: {0}, Pivot value {1}'.format(ip, a[ip].key))
        print('Current total list a: {0}'.format(a))
    
    # Partition list a in the segment [il, ir].
    if verbose:
        print('Before partion, current list segment: ', a[il:ir + 1])
    ip = partion(a, il, ir, ip, track=True, verbose=False)
    # For statistics, only.
    if nred == 0: gca += 1
    if verbose:
        print('After partion, pivot index: {0}'.format(ip))
        print('Current list segment: {0}'.format(a[il:ir + 1]))

    # Select the correct segment for the next selection.
    if ip == istat - 1:
        # The ith statistic has been found.
        if verbose:
            print('>>> Statistic i = {0} is at index {1}'.format(istat, ip))
    elif ip > istat - 1:
        # The ith statistic is in the left segment.
        if verbose:
            print('>>> Statistic i = {0} is in: {1}'.format(istat, a[il:ip]))
        ip = select(a, il, ip - 1, istat, nred, verbose=verbose)
    elif ip < istat - 1:
        # The ith statistic is in the right segment.
        if verbose:
            print('>>> Statistic i = {0} '.format(istat) +
                  'is in: {0}'.format(a[ip+1:ir+1]))
        ip = select(a, ip + 1, ir, istat, nred, verbose=verbose)

    if verbose:
        print('--- Returning from select with istat = {0}, '.format(istat) +
              'nred = {0}'.format(nred))
        print('--- Output list segment: {0}'.format(a[il:ir + 1]))

    return ip

def dselect(a, istat, verbose=False):
    """
    Recursive selection of the ith statistic from a list of n elements in
    time O(n) using the DSelect algorithm, proposed 1973 by Manuel Blum,
    Robert Floyd, Vaughan Pratt, Ronald Rivest and Robert Tarjan.
    DSelect has a larger factor to the asymptotic time, and it does not run
    in-place, i.e. requiring addtitional memory.
    
    Arguments:
        a (list):
            List of elements to be searched.
        istat (int):
            The ith statistic to be selected.
        verbose (bool):
            More intermediate output is written when True.
    
    Returns:
        value (int):
            The value of the ith statistic.
        
        List a will be changed in-place during this method.
    """

    # Initialize index values.
    il, ir = 0, len(a) - 1

    # Ensure that the list contains at least istat >= 1 numbers.
    # (As long as list a contains 1 number and istat >= 1, DSelect will
    # return a result. In case istat is larger than length of list a,
    # the value of the largest item would be returned.)
    assert istat >= 1 and ir >= istat - 1
    
    # Select from the entire list, i.e. in the segment [il, ir].
    ip = select(a, il, ir, istat, nred=0, verbose=verbose)

    return a[ip].key

def read_list(file_name):
    """
    Read list data from file and create elements.
    Each row represents 1 item of the list.
    
    Elements carry their value in the attribute 'key'.
    Elements have the position in their parent list stored in index,
    and the position in their current list in index2.
    Since we are starting a new parent list here, both numbers are the same.
    The atttribute label is not needed in DSelect and left empty.
    
    Arguments:
        file_name (str):
            File name containing the data to be read.
    
    Returns:
        err (int):
            Indicator 0 for success and 1 for errors.
        list (list):
            List with elements.
    """
    
    try:
        with open(file_name, 'r') as f:
            raw_data = f.read()
            list = [Elem(int(x), '', i, i) 
                    for i, x in enumerate(raw_data.split())]
        return 0, list
    except:
        list = []
        return 1, list

if __name__ == '__main__':
    
    gc  = 0   # global counter for number of calls to function partion
    gca = 0   # global counter for number of calls to partion on parent list

    # Set parameters for calculation.
    verbose = False
    istat = 10305

    # Read the list input from file.
    file_name = 'IntegerArray.txt'
    status, a = read_list(file_name)
    
    # Sort the list.
    if verbose: print('Initial list: {0}'.format(a))   # for test purposes
    tic = time.perf_counter()
    value = dselect(a, istat, verbose=verbose)
    toc = time.perf_counter()
    print('The value of the {0}th statistic is {1}'.format(istat, value))
    print('Number of calls of partitioning function: {0}'.format(gc))
    print('Number of partitionings on parent list:   {0}'.format(gca))
    print('Execution time: {0} ms'.format((toc - tic) * 1000))
    