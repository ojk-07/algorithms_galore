# -*- coding: utf-8 -*-
"""
Test for Tree and BNode classes to be used as an imported module.

A program for Stanford Algorithms Specialization 2 written by Oliver Kroneisen,
oliver@kroneisen.net
"""

import bnodes as bn
import treetools as tt

def add_node(tree, key):
    node = bn.bnode(key)
    status = tree.insert(node)
    print('Insert', key, '->', status, node)
    return status, node

def del_node(tree, node):
    status = tree.delete(node)
    print('Delete', node, '->', status)
    return status

# Main programm
def runMe():
    # Test 01: Insert.
    # Prepare the initial tree structure.
    t1 = tt.btree(tree_type='avl')
    add_node(t1, 20)
    add_node(t1, 10)
    add_node(t1, 35)
    add_node(t1, 15)
    add_node(t1, 30)
    add_node(t1, 45)
    add_node(t1, 25)
    add_node(t1, 40)
    print(t1.inorder())
    print()

    # Insert 27.
    add_node(t1, 27)
    print(t1.inorder())
    print()
    
    # Insert 26.
    add_node(t1, 26)
    print(t1.inorder())
    print()

    # Insert 43.
    add_node(t1, 43)
    print(t1.inorder())
    print()

    # Insert 41.
    add_node(t1, 41)
    print(t1.inorder())
    print()

    # Test 02: Delete.
    # Prepare the initial tree structure.
    t2 = tt.btree(tree_type='avl')
    _, n90 = add_node(t2, 90)
    add_node(t2, 40)
    _, n130 = add_node(t2, 130)
    add_node(t2, 30)
    add_node(t2, 70)
    _, n120 = add_node(t2, 120)
    _, n150 = add_node(t2, 150)
    add_node(t2, 10)
    add_node(t2, 50)
    _, n80 = add_node(t2, 80)
    add_node(t2, 110)
    add_node(t2, 60)
    print(t2.inorder())
    print()

    # Delete 150.
    del_node(t2, n150)
    print(t2.inorder())
    print()

    # Delete 80.
    del_node(t2, n80)
    print(t2.inorder())
    print()

    # Delete 130.
    del_node(t2, n130)
    print(t2.inorder())
    print()

    # Delete 90.
    del_node(t2, n90)
    print(t2.inorder())
    print()

    # Delete 120.
    del_node(t2, n120)
    print(t2.inorder())
    print()
    return

if __name__ == '__main__':
    runMe()
