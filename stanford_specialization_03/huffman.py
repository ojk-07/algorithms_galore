# -*- coding: utf-8 -*-
"""
Huffman's algorithm for computing an optimal prefix-free encoding for a given
alphabet Σ with weigths for each letter of the alphabet.
Running time: O(n log n) for and alphabet Σ with n letters.

A program for Stanford Algorithms Specialization 3 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #3 in the Course
https://www.coursera.org/learn/algorithms-greedy/home/module/3
"""

import code_elements as el
import heaptools     as ht
import time
import sys

def huffman(codes):
    """
    Calculate an optimal prefix-free encoding for a given alphabet Σ with
    weigths for each letter of the alphabet by leveraging Huffman's algorithm.
    
    The code nodes for the letters will be changed in-place.
    
    Arguments:
        codes (list):
            List of codes for the letters, matching every code to the node
            element of class elem.
            elem.key: code id
            elem.val: weitht of the encoded letter
            elem.idx: index of node within heap structure, -1 if not in heap
            elem.parent: reference to the parent node, otherwise 'None'
            elem.left:   reference to the left child node, otherwise 'None'
            elem.right:  reference to the right child node, otherwise 'None'
            elem.encoding: encoding string for the element
            elem.size, elem.height, elem.balance: statistical tree properties,
            which are not used nor updated in this application
    
    Returns:
        min_length (int):
            Minimum encoding length.
        max_length (int):
            Maximum encoding length.
        T (elem):
            Reference to the root node of the Huffman Codes tree.
    """

    # Initialize data structures.
    T = None                  # root node of the Huffman Codes tree
    queue_1 = []              # queue of the codes for original letters
    queue_2 = []              # queue of the codes for merged letters
    min_length = len(codes)   # minimum encoding length < n
    max_length = 0            # maximum encoding length > 0
    # Initialize heap to sort the codes by the weight of letters.
    h = ht.heap(codes.copy(), update_idx=True)

    # Get sorted list of elements from heap.
    for i in range(len(h.e)):
        e = h.deletem(update_idx=True)
        queue_1.append(e)

    # Calculate Huffman Codes tree.
    T = huffman_tree(queue_1, queue_2)

    # Calculate the minimum and maximum encoding lengths.
    for c in codes:
        length = len(c.encoding)
        if length < min_length:
            min_length = length
        if length > max_length:
            max_length = length

    return min_length, max_length, T

def huffman_tree(queue_1, queue_2):
    """
    Calculate an optimal prefix-free encoding for a given alphabet Σ with
    weigths for each letter of the alphabet by leveraging Huffman's algorithm.
    
    The code nodes for the letters will be changed in-place.
    
    This version works iteratively and avoids deep recursion.
    
    Arguments:
        queue_1 (list):
            Queue of the codes for original letters.
        queue_2 (list):
            Queue of the codes for merged letters.

    Returns:
        T (elem):
            Reference to the root node of the Huffman Codes tree.
    """

    # Continue until only one element remains.
    while len(queue_1) + len(queue_2) > 1:
        # Select the two elements with smallest weights.
        if len(queue_2) == 0:
            x = queue_1.pop(0)
            y = queue_1.pop(0)
        elif len(queue_1) == 0:
            x = queue_2.pop(0)
            y = queue_2.pop(0)
        elif len(queue_1) == 1:
            if queue_1[0] <= queue_2[0]:
                x = queue_1.pop(0)
                y = queue_2.pop(0)
            else:
                x = queue_2.pop(0)
                y = queue_2.pop(0)
        else:
            # At least two elements in queue_1 and one element in queue_2.
            if queue_1[0] <= queue_2[0]:
                x = queue_1.pop(0)
                if queue_1[0] <= queue_2[0]:
                    y = queue_1.pop(0)
                else:
                    y = queue_2.pop(0)
            else:
                x = queue_2.pop(0)
                if len(queue_2) == 0 or queue_1[0] <= queue_2[0]:
                    y = queue_1.pop(0)
                else:
                    y = queue_2.pop(0)

        # Create merged element with id 0.
        z = el.elem(0, x.val+y.val, -1, left=x, right=y)
        x.parent = z
        y.parent = z

        # Append merged element to queue_2.
        queue_2.append(z)

    # The last remaining element is the root.
    if len(queue_1) == 1:
        T = queue_1[0]
    else:
        T = queue_2[0]

    # Assign encodings.
    T.encoding = ''
    stack = [(T, T.encoding)]
    while stack:
        node, encoding = stack.pop()
        if node.left is not None:
            node.left.encoding = encoding + '0'
            stack.append((node.left, encoding + '0'))
        if node.right is not None:
            node.right.encoding = encoding + '1'
            stack.append((node.right, encoding + '1'))

    return T

def read_list(file_name):
    """
    Read source data of weights for letters of alphabet Σ.
    Every row contains the weigth of a letter.
    
    Arguments:
        file_name (str):
            File name to be read.
    
    Returns:
        status (int):
            '0' indicates successful processing, '1' that an error ocurred.
        n_letters (int):
            Number of letters.
            We assume that there are the letters 1 ... n.
        codes (list):
            List of codes for the letters, matching every code to the node
            element of class elem.
            The attribute key represents the code id, val the given weights
            and parent, left and right are the respective nodes in the huffman
            tree. The attribute encoding is the binary code assigned to the
            code id.
            For each node element, attribute idx is initialized with -1.
    """

    # Initialize structures.
    codes = []
    n_letters = 0
    # Read list data from file.
    # Each row represents 1 item of the list.
    try:
        with open(file_name, 'r') as f:
            # Read data from file.
            raw_data = f.readlines()
            n = len(raw_data)
            n_letters = n - 1
            # Evaluate all lines.
            for i in range(1, n):   # line number
                # Evaluate current line.
                row = raw_data[i].split()
                weight = int(row[0])
                # Create a node element for the code.
                e = el.elem(i, weight, -1)
                # Append the weight to the list of weights.
                codes.append(e)
        return 0, n_letters, codes
    except:
        return 1, n_letters, codes

# Main program.
def runMe():
    file_name = 'huffman.txt'

    tic = time.perf_counter()
    sys.stdout.write('\nReading input data for Huffman Codes.\n')
    sys.stdout.flush()
    status, n_letters, codes = read_list(file_name)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of letters: ' + str(n_letters) + '\n')
    sys.stdout.flush()
    sys.stdout.write('\nCalculate Huffman Codes.\n')
    sys.stdout.flush()
    min_length, max_length, T = huffman(codes)
    # Minimum and maximum encoding lengths according to assignment.
    sys.stdout.write('\nMinimum encoding length = ' + str(min_length) +
                     ', maximum length = ' + str(max_length) + '\n')
    sys.stdout.flush()
    #sys.stdout.write('Huffman Codes:\n')
    #sys.stdout.write(str(codes) + '\n')
    #sys.stdout.flush()
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
