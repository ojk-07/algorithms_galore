# -*- coding: utf-8 -*-
"""
Test for Tree and BNode classes to be used as an imported module.

A program for Stanford Algorithms Specialization 2 written by Oliver Kroneisen,
oliver@kroneisen.net
"""

import bnodes as bn
import treetools as tt

# Main programm
def runMe():
    # Test 01.
    key = 3
    n1 = bn.bnode(key)
    print(n1, '-> size:', n1.size)

    key = 5
    n2 = bn.bnode(key, left=n1)
    n1.parent = n2
    print(n2, '-> size:', n2.size)
    print(n1, '-> size:', n1.size)

    t1 = tt.btree(root=n2)
    print(t1)
    print()

    key = 3
    status, n = t1.search(key)
    print('Search', key, '->', status, n)

    key = 7
    status, n = t1.search(key)
    print('Search', key, '->', status, n)

    key = 1
    status, n = t1.search(key)
    print('Search', key, '->', status, n)
    print()

    key = 2
    n3 = bn.bnode(key)
    status = t1.insert(n3)
    print('Insert', key, '->', status, n1)

    key = 3
    n4 = bn.bnode(key)
    status = t1.insert(n4)
    print('Insert', key, '->', status, n3)

    status = t1.insert(n4, unique=False)
    print('Insert', key, '->', status, n3, n1)
    print('Size of tree:', t1.root.size)
    print(t1.inorder())

    key = 7
    n5 = bn.bnode(key)
    status = t1.insert(n5)
    print('Insert', key, '->', status)
    print('Size of tree:', t1.root.size)
    print(t1.inorder())
    print()

    min_node = t1.findmin()
    print('A minimum node:', min_node)

    max_node = t1.findmax()
    print('A maximum node:', max_node)
    print()

    p = t1.pred(n1)
    print('Predecessor of', n1, '->', p)

    p = t1.pred(n5)
    print('Predecessor of', n5, '->', p)

    p = t1.pred(n3)
    print('Predecessor of', n3, '->', p)

    p = t1.succ(n3)
    print('Successor of', n3, '->', p)

    p = t1.succ(n4)
    print('Successor of', n4, '->', p)

    p = t1.succ(n2)
    print('Successor of', n2, '->', p)

    p = t1.succ(n5)
    print('Successor of', n5, '->', p)
    print()

    print('Before deletion:')
    print('Size of tree:', t1.root.size)
    print(t1.inorder())

    status = t1.delete(n5)
    print('Delete', n5, '->', status)
    print('Size of tree:', t1.root.size)
    print(t1.inorder())
    
    status = t1.delete(n4)
    print('Delete', n4, '->', status)
    print('Size of tree:', t1.root.size)
    print(t1.inorder())
    print()

    key = 11
    n6 = bn.bnode(key)
    status = t1.insert(n6)
    print('Insert', key, '->', status)
    print('Size of tree:', t1.root.size)
    print(t1.inorder())
    print(n3, n3.size)
    print(n1, n1.size)
    print(n2, n2.size)
    print(n6, n6.size)
    print()

    status = t1.delete(n2)
    print('Delete', n2, '->', status)
    print('Size of tree:', t1.root.size)
    print(t1.inorder())
    print('Root', t1.root)
    print()

    i = 2
    status, n = t1.select(i)
    print(i, 'th order statistic:', status, '->', n)

    i = 3
    status, n = t1.select(i)
    print(i, 'th order statistic:', status, '->', n)
    print()

    # Test 02.
    t2 = tt.btree()
    v1 = bn.bnode(1)
    v2 = bn.bnode(2)
    v3 = bn.bnode(4)
    v4 = bn.bnode(5)
    v5 = bn.bnode(11)
    t2.insert(v4)
    t2.insert(v1)
    t2.insert(v3)
    t2.insert(v2)
    t2.insert(v5)
    print('Before deletion:')
    print('Size of tree:', t2.root.size)
    print(t2.inorder())

    status = t2.delete(v4)
    print('Delete', v4, '->', status)
    print('Size of tree:', t2.root.size)
    print(t2.inorder())
    print('Root', t2.root)
    print()

    i = 1
    status, n = t2.select(i)
    print(i, 'th order statistic:', status, '->', n)
    print('Rank:', n, '->', t2.rank(n))

    i = 2
    status, n = t2.select(i)
    print(i, 'th order statistic:', status, '->', n)
    print('Rank:', n, '->', t2.rank(n))

    i = 3
    status, n = t2.select(i)
    print(i, 'th order statistic:', status, '->', n)
    print('Rank:', n, '->', t2.rank(n))

    i = 4
    status, n = t2.select(i)
    print(i, 'th order statistic:', status, '->', n)
    print('Rank:', n, '->', t2.rank(n))

    i = 5
    status, n = t2.select(i)
    print(i, 'th order statistic:', status, '->', n)

    i = 0
    status, n = t2.select(i)
    print(i, 'th order statistic:', status, '->', n)
    return

if __name__ == '__main__':
    runMe()
