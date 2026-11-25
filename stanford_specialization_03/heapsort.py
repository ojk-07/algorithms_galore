# -*- coding: utf-8 -*-
"""
Heapsort method to be used as an imported module.

A method collection for Stanford Algorithms Specialization 3 written
by Oliver Kroneisen, oliver@kroneisen.net
"""

import elements  as el
import heaptools as ht

def heapsort(values, ascending=True, unique=False):
    """
    Heapsort for a list of key values, using the heap class.
    
    Arguments:
        values (list):
            List of values to be sorted.
        ascending (bool):
            Optional flag defining whether the sorting shall be in
            ascending order.
        unique (bool):
            Optional flag defining whether the sorted list shall contain
            all values or only unique values.
    
    Returns:
        values_sorted (list):
            Sorted list of values.
    """

    # Initialize data structures.
    values_sorted = []

    # Create list of elements for class heap.
    elements = []
    for i in range(len(values)):
        # Create a node element for the value.
        e = el.elem(i, values[i])
        elements.append(e)

    # Initialize heap to sort the elements.
    if not ascending:
        h = ht.heap(elements, mintype=False, update_idx=False)
    else:
        h = ht.heap(elements, mintype=True, update_idx=False)

    # Get sorted list of elements from heap.
    e = h.deletem(update_idx=False)
    values_sorted.append(e.val)
    last_val = e.val
    for i in range(len(h.e)):
        e = h.deletem(update_idx=False)
        if unique:
            if e.val != last_val:
                values_sorted.append(e.val)
            last_val = e.val
        else:
            values_sorted.append(e.val)

    return values_sorted

# Main program.
def runMe():
    # Placeholder.
    return

if __name__ == '__main__':
    runMe()
