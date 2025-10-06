# -*- coding: utf-8 -*-
"""
Miller-Rabin-Test with exact results for numbers < 3*10^24 bzw. 2**78.

This program is related to the programming assignment #4 in the Course
https://www.coursera.org/learn/algorithms-graphs-data-structures/home/module/4
"""

import math, time

def _try_composite(a, d, n, s):
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n-1:
            return False
    return True # n  is definitely composite
 
def is_prime(n, _precision_for_huge_n=24):
    if n in (0, 1):
        return False
    if n in _known_primes:
        return True
    if any((n%p) == 0 for p in _known_primes):
        return False
    d, s = n - 1, 0
    while not d&1: # e d&1 is equivalent to d%2
        d, s = d >> 1, s + 1
    # Returns exact according to
    # https://de.wikipedia.org/wiki/Miller-Rabin-Test
    if n < 1373653: 
        return not any(_try_composite(a, d, n, s)
            for a in (2, 3))
    elif n < 9080191: 
        return not any(_try_composite(a, d, n, s)
            for a in (31, 73))
    elif n < 4759123141: 
        return not any(_try_composite(a, d, n, s)
            for a in (2, 7, 61))
    elif n < 2152302898747: 
        return not any(_try_composite(a, d, n, s)
            for a in (2, 3, 5, 7, 11))
    elif n < 3474749660383: 
        return not any(_try_composite(a, d, n, s)
            for a in (2, 3, 5, 7, 11, 13))
    elif n < 341550071728321: 
        return not any(_try_composite(a, d, n, s)
            for a in (2, 3, 5, 7, 11, 13, 17))
    elif n < 3825123056546413051: 
        return not any(_try_composite(a, d, n, s)
            for a in (2, 3, 5, 7, 11, 13, 17, 19, 23))
    elif n < 318665857834031151167461: 
        return not any(_try_composite(a, d, n, s)
            for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37))
    else:
        # otherwise
        return not any(_try_composite(a, d, n, s) 
            for a in _known_primes[:_precision_for_huge_n])

_def_up_limit = 100
#_def_up_limit = 37
_known_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
_known_primes += [x for x in range(37, _def_up_limit, 2) if is_prime(x)]

# Main programm
def runMe():
    start_time = time.perf_counter()
    print("Miller-Rabin-Test für Primzahlen")
    size = 1000000
    start = max(2, 2*size - size//1000)
    end   = 2*size
    for i in range(start, end + 1):
        if is_prime(i):
            print(i, "ist eine Primzahl.")
    end_time = time.perf_counter()
    t = math.floor(0.5+(end_time-start_time)*1000000)/1000
    print("Berechnungszeit = {0} ms".format(t))
    return

if __name__ == '__main__':
    runMe()
