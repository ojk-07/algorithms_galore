# -*- coding: utf-8 -*-
"""
Test for Tree and BNode classes to be used as an imported module.

A program for Stanford Algorithms Specialization 2 written by Oliver Kroneisen,
oliver@kroneisen.net
"""

import bnodes as bn
import treetools as tt

def add_node(tree, key, mark='', unique=True):
    node = bn.bnode(key, mark=mark)
    status = tree.insert(node, unique=unique)
    print('Insert', key, '->', status, node)
    return status, node

def del_node(tree, node):
    status = tree.delete(node)
    print('Delete', node, '->', status)
    return status

# Main programm
def runMe():
    # Test 01: Insert (including non-unique keys).
    # Prepare the initial tree structure.
    t1 = tt.btree(tree_type='avl')
    _, n1 = add_node(t1, 20, mark='n1(1)')
    _, n2 = add_node(t1, 10, mark='n2')
    _, n3 = add_node(t1, 35, mark='n3')
    _, n4 = add_node(t1, 15, mark='n4')
    _, n5 = add_node(t1, 30, mark='n5')
    _, n6 = add_node(t1, 45, mark='n6')
    _, n7 = add_node(t1, 25, mark='n7')
    _, n8 = add_node(t1, 40, mark='n8')
    print(t1.inorder())
    print()

    # Insert 20.
    _, n9 = add_node(t1, 20, mark='n9(2)')
    status = t1.insert(n9, unique=False)
    print('Insert', n9.key, '->', status, n9)
    print(t1.inorder())
    print()
    
    # Insert 20.
    _, n10 = add_node(t1, 20, mark='n10(3)', unique=False)
    print(t1.inorder())
    print()

    # Insert 20.
    _, n11 = add_node(t1, 20, mark='n11(4)', unique=False)
    print(t1.inorder())
    print()

    # Test 02: Delete (including non-unique keys).
    # Delete 150.
    del_node(t1, n1)
    print(t1.inorder())
    print()
    return

if __name__ == '__main__':
    runMe()
