# -*- coding: utf-8 -*-
"""
Hashing based algorithm to solve the 2sum problem for a set of numbers
in linear time.

A program for Stanford Algorithms Specialization 2 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #4 in the Course
https://www.coursera.org/learn/algorithms-graphs-data-structures/home/module/4
"""

import time
import sys

# Prime numbers for hashing.
# Suitable prime numbers can be found via the Miller-Rabin test.
global p0, p1
p0   = 1999993   # prime number within a constant factor of #data records
p1   = 1999979   # prime number <= p0 - 2
test = 10000     # boundary of the test intervall for t

def h0(x):
    """
    Primary hash function h0.

    Arguments:
        x (int):
            Number to be hashed.

    Returns:
        y (int):
            Hash value.
    """

    global p0
    return x%p0

def h1(x):
    """
    Secondary hash function h1.
    
    Creates return values which are not dividing p0, if p1 <= p0 - 2.

    Arguments:
        x (int):
            Number to be hashed.

    Returns:
        y (int):
            Hash value.
    """

    global p1
    return 2 + x%p1

def h(i, x):
    """
    Hash function h (double hashing).

    Arguments:
        x (int):
            Number to be hashed.

    Returns:
        y (int):
            Hash value.
    """

    global p0
    return (h0(x) + i*i*h1(x))%p0

def read_list(file_name):
    """
    Read source data of numbers to calculate the the 2sum problem with.
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
    global p0, test
    file_name = 'algo1-programming_prob-2sum.txt'

    tic = time.perf_counter()
    sys.stdout.write('\nReading input data for 2Sum Problem.\n')
    sys.stdout.flush()
    status, numbers = read_list(file_name)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of numbers: ' + str(len(numbers)) + '\n')
    sys.stdout.flush()
    sys.stdout.write('\n2Sum matches.\n')
    sys.stdout.flush()
    # Initialize hash table.
    hashes = []
    for i in range(p0):
        hashes.append(None)
    # Insert numbers into hash table.
    absmin = abs(numbers[0])
    for m in numbers:
        # The minimum of the absolute numbers is helpful to check if there
        # is the possibility thata value t could be the sum of 2 identical
        # numbers.
        if abs(m) < absmin:
            absmin = abs(m)
        inserted = False
        i = 0
        while not inserted:
            k = h(i, m)
            if hashes[k] == None:
                # Insert number m into hash table.
                hashes[k] = m
                inserted = True
            else:
                i += 1
    sys.stdout.write('Minimum absolute value: ' + str(absmin) + '\n')
    sys.stdout.flush()
    # Initialize results.
    count = 0
    results = []
    # Loop over t.
    for t in range(-test, test + 1):
        #print('Testing t =', t)
        # Loop over numbers.
        resolved = False
        for m in numbers:
            n = t - m
            # Check if n is in the hash table.
            stop = False
            i = 0
            while not stop:
                k = h(i, n)
                if hashes[k] == n:
                    # Number n found, check that m and n are distinct.
                    if m == n:
                        # Check if n is in the hash table a second time.
                        checked = False
                        i += 1
                        while not checked:
                            k = h(i, n)
                            if hashes[k] == n:
                                # Number n in hash table a second time.
                                checked, stop, resolved = True, True, True
                            elif hashes[k] == None:
                                # Number n not in hash table a second time.
                                checked, stop = True, True
                            else:
                                i += 1
                    else:
                        stop, resolved = True, True
                    if resolved:
                        # Update result counter.
                        count += 1
                        print('Resolved:', t, m, n)
                        # Add results to results table.
                        results.append([t, n])
                elif hashes[k] == None:
                    # Number n not in hash table, stop the search.
                    stop = True
                else:
                    i += 1
            if resolved:
                # Leave loop over numbers for this t.
                break
    sys.stdout.write('\nResults: ' + str(count) + '\n')
    sys.stdout.write(str(results) + '\n')
    sys.stdout.flush()
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
