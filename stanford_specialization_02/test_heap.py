# -*- coding: utf-8 -*-
"""
Test for Heap and Element classes to be used as an imported module.

A program for Stanford Algorithms Specialization 2 written by Oliver Kroneisen,
oliver@kroneisen.net
"""

import elements as el
import heaptools as ht

global INF   # global variable to represent "infinite"
INF = 1000000 

# Main programm
def runMe():
    # Test 01.
    print('Testsatz 1')
    h = ht.heap([18, 7, 11, 5, 20, 25])
    print(h)
    m = h.deletem()
    print('deletem ->', m)
    print(h)
    k = 3
    h.insert(k)
    print('insert ->', k)
    print(h)
    k = 2
    h.insert(k)
    print('insert ->', k)
    print(h)
    k = 1
    h.insert(k)
    print('insert ->', k)
    print(h)
    # Test 02.
    print('Testsatz 2')
    h = ht.heap([2, 13, 3, 21, 25, 4, 5])
    print(h)
    idx = 4
    d = h.e[idx]
    h.delete(idx)
    print('delete element at index', idx, '->', d)
    print(h)
    idx = 5
    d = h.e[idx]
    h.delete(idx)
    print('delete element at index', idx, '->', d)
    print(h)
    idx = 0
    d = h.e[idx]
    h.delete(idx)
    print('delete element at index', idx, '->', d)
    print(h)
    m = h.deletem()
    print('deletem ->', m)
    print(h)
    # Test 03.
    print('Testsatz 3')
    e1 = el.elem(2, 2, -1)
    e2 = el.elem(13, 13, -1)
    e3 = el.elem(3, 3, -1)
    e4 = el.elem(21, 21, -1)
    e5 = el.elem(25, 25, -1)
    e6 = el.elem(4, 4, -1)
    e7 = el.elem(5, 5, -1)
    e8 = el.elem(7, 7, -1)
    e9 = el.elem(1, 1, -1)
    e10 = el.elem(42, 42, -1)
    h = ht.heap([e1, e2, e3, e4, e5, e6, e7], update_idx=True)
    print(h)
    idx = 4
    d = h.e[idx]
    h.delete(idx, update_idx=True)
    print('delete element at index', idx, '->', d)
    print(h)
    idx = 5
    d = h.e[idx]
    h.delete(idx, update_idx=True)
    print('delete element at index', idx, '->', d)
    print(h)
    idx = 0
    d = h.e[idx]
    h.delete(idx, update_idx=True)
    print('delete element at index', idx, '->', d)
    print(h)
    m = h.deletem(update_idx=True)
    print('deletem:', m)
    print(h)
    h.insert(e8, update_idx=True)
    print('insert ->', e8.val)
    print(h)
    h.insert(e9, update_idx=True)
    print('insert ->', e9.val)
    print(h)
    h.insert(e10, update_idx=True)
    print('insert ->', e10.val)
    print(h)
    return

if __name__ == '__main__':
    runMe()
