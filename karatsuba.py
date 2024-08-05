# -*- coding: utf-8 -*-
"""
Karatsuba's algorithm.

A program for Stanford Algorithms Specialization written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #1 in the Course
https://www.coursera.org/learn/algorithms-divide-conquer/home/module/1
"""

import time

def karatsuba(a, b, verbose=False):
    """
    Recursive calculation of the product of 2 numbers using
    Kartsuba's algorithm for decimal represenation in time n^log_2(3).

    Arguments:
        a (string):
            First factor.
        b (string):
            Second factor.
        verbose (bool):
            More intermediate output is written when True.

    Returns:
        ab (string):
            The product of a times b.
        """

    # Convert int factors a and b to strings.
    na = len(a)
    nb = len(b)

    # Split factors a and b.
    # The general case is considered here, where na can also be odd.

    # Try to make na2 and nb2 even numbers each,
    # when splitting off at least 2 digits in a and b.
    na2, nb2 = (na // 4) * 2, (nb // 4) * 2

    if na2 == 0 or nb2 == 0:
        # Try to split off at least 1 digit in a and b each,
        # then also the sum of na2 and nb2 will still be even.
        if na > 1 and nb > 1:
            # It is possible to splitt off 1 digit in a and be each.
            na2, nb2 = 1, 1
        else:
            # This is the base case, where at least one of the factors
            # is a 1 digit number. Calculate the product directly.
            if verbose:
                print('Base case: {0}*{1}'.format(a, b))
            ab = str(int(a) * int(b))
            return ab
            
    # The first part of the splitted numbers takes the remaining digits.
    na1 = na - na2
    nb1 = nb - nb2

    # Split the large factors into smaller parts.
    a1, a2 = a[:na1], a[na1:]
    b1, b2 = b[:nb1], b[nb1:]
    if verbose:
        print('Split: {0} {1} {2} {3}'.format(a1, a2, b1, b2))

    # Calculate smaller products recursively.
    m1 = int(karatsuba(a1, b1, verbose=verbose))
    m2 = int(karatsuba(a2, b2, verbose=verbose))
    c1 = str(int(a1) + int(a2))
    c2 = str(int(b1) + int(b2))
    m3 = int(karatsuba(c1, c2, verbose=verbose)) - m1 - m2
    if verbose:
        print('Interim values: {0} {1} {2}'.format(m1, m2, m3))

    # Calculate the overall product.
    # It has been secured that the sum of na2 and nb2 is even.
    np = (na2 + nb2) // 2   # with no remainder
    ab = str(m1 * 10**(2*np) + m3 * 10**np + m2)
    if verbose:
        print('Interim product: {0}'.format(ab))

    return ab

if __name__ == '__main__':

    # Set parameters for calculation.
    verbose = False
    #a = '3141'
    #b = '2718'
    #a = '31415926'
    #b = '27182818'
    #a = '3141592653589793'
    #b = '2718281828459045'
    a = '3141592653589793238462643383279502884197169399375105820974944592'
    b = '2718281828459045235360287471352662497757247093699959574966967627'

    # Calculate the product.
    tic1 = time.perf_counter()
    c = karatsuba(a, b, verbose=verbose)
    toc1 = time.perf_counter()
    mc = int(c)
    print('The product of a times b: {0}'.format(mc))
    tic2 = time.perf_counter()
    mp = int(a) * int(b)
    toc2 = time.perf_counter()
    print('Crosschecking the result: {0}'.format(mp))
    print('Difference: {0}'.format(mc - mp))
    print('Execution time algorithm: {0} ms'.format((toc1 - tic1) * 1000))
    print('Execution time natively:  {0} ms'.format((toc2 - tic2) * 1000))
