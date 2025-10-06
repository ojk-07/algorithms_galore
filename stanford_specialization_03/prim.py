# -*- coding: utf-8 -*-
"""
Prim's greedy algorithm for calculating a minimal spanning tree in an
undirected graph with weigthed edges (weights can also be negative).

Runtime: O(m log n) for a Graph with m edges and n vertices.

A program for Stanford Algorithms Specialization 3 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #1 in the Course
https://www.coursera.org/learn/algorithms-greedy/home/module/1
"""

import time
import sys
import elements  as el
import heaptools as ht

global INF   # global variable to represent "infinite"
INF = 1000000 

def prim_MST(nodes, adj_dict, s):
    """
    Calculate minimum spanning tree for undirected graph with edge weights
    (can also be negative) from node start to all reachable nodes.

    Arguments:
        nodes (dict):
            Dictionary of nodes, matching every node key to the node element
            of class elem.
            elem.key: key of node
            elem.val: distance to nodes set X, initialized with INF
            elem.idx: index of node within heap structure, -1 if not in heap
            elem.ref: key of closest node in X
        adj_dict (dict):
            Dictionary of nodes, matching every node to its adjacency list,
            including the weights of edges.
        s (elem):
            Start node.

    Returns:
        nodes (dict):
            Changed dictionary of nodes with updated val attributes
            (not relevant, all reachable notes will have val = 0).
        cost (int or float):
            Cost of minimum spanning tree.
        T (list):
            List of edges as node tuples (v, w) of minimum spanning tree.
    """

    # Initialize data structures:
    T = []          # edges of minimum spanning tree
    cost = 0        # cost of minimum spanning tree
    X = []          # nodes processed so far
    s.val = 0       # distance from start to start node s to X is 0
    s.ref = s.key   # s is the closest node to s in X
    X.append(s)
    # Adjust distances to X for the neighbors of s.
    adj_list = adj_dict[s.key]
    for i in adj_list:
        nodes[i[0]].val = i[1]
        nodes[i[0]].ref = s.key
    # Initialize heap, representing V - X.
    nodes_list = []
    for i in nodes.values():
        if not i.key == s.key:
            nodes_list.append(i)
    h = ht.heap(nodes_list, update_idx=True)
    while True:
        # Identify new node.
        try:
            w = h.deletem(update_idx=True)
            # Update cost of minimum spanning tree.
            cost += w.val
            # Add edge to minimum spanning tree T.
            T.append((w.ref, w.key))
        except:
            # No more reachable nodes.
            return cost, T
        # Update distances of nodes in V - X to X.
        w.val = 0   # node w becomes part of X
        adj_list = adj_dict[w.key]
        for e in adj_list:   # edges of node w
            u = nodes[e[0]]  # other node incident to edge e
            if u.idx > -1:   # only if u is still in heap, i.e. in V - X
                d2 = e[1]    # distance of u to X via w
                if d2 < u.val:
                    u.val = d2
                    u.ref = w.key
                # Position of u may now be incorrect, delete u from heap.
                h.delete(u.idx, update_idx=True)
                # Insert u back into heap at right position.
                h.insert(u, update_idx=True)
        # Add w to X.
        X.append(w.key)
    return cost, T

def read_list(file_name):
    """
    Read source data of undirected edges.
    Every row starts with a node, followed by a node and a weight.

    It is assumed that every undirected edge is only reported once,
    but the adjacency lists of both incident nodes must be updated.

    Arguments:
        file_name (str):
            File name to be read.

    Returns:
        status (int):
            '0' indicates successful processing, '1' that an error ocurred.
        nodes (dict):
            Dictionary of nodes, matching every node key to the node element
            of class elem.
            For each node element, attribute val is initialized with INF,
            idx with -1.
        adj_dict (dict):
            Dictionary of nodes, matching every node key to its adjacency list,
            including the weights of edges.
    """

    # Initialize structures.
    global INF
    nodes = {}
    adj_dict = {}
    # Read list data from file.
    # Each row represents 1 item of the list.
    try:
        with open(file_name, 'r') as f:
            # Read data from file.
            raw_data = f.readlines()
            n = len(raw_data)
            # Evaluate all lines.
            for i in range(1, n):   # line number
                # Evaluate current line.
                row = raw_data[i].split()
                anch = int(row[0])
                node = int(row[1])
                weight = int(row[2])
                # Check if anch is already in adj_dict.
                if not anch in adj_dict:
                    # Create an empty entry for anch.
                    e = el.elem(anch, INF, -1)
                    nodes[anch] = e
                    adj_dict[anch] = []
                # Check if node is already in adj_dict.
                if not node in adj_dict:
                    # Create an empty entry for node.
                    e = el.elem(node, INF, -1)
                    nodes[node] = e
                    adj_dict[node] = []
                # Insert edge into adj_dict for anch.
                adj_list = adj_dict[anch]
                adj_list.append([node, weight])
                # Insert edge into adj_dict for node.
                adj_list = adj_dict[node]
                adj_list.append([anch, weight])
        return 0, nodes, adj_dict
    except:
        return 1, nodes, adj_dict

# Main programm
def runMe():
    file_name = 'edges.txt'

    tic = time.perf_counter()
    sys.stdout.write('\nReading input data for Prim.\n')
    sys.stdout.flush()
    status, nodes, adj_dict = read_list(file_name)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of nodes: ' + str(len(nodes)) + '\n')
    sys.stdout.flush()
    sys.stdout.write('\nCalculate minimum spanning tree.\n')
    sys.stdout.flush()
    start = nodes[1]   # start with node '1'
    cost, T = prim_MST(nodes, adj_dict, start)
    # Minimum spanning tree according to assignement.
    sys.stdout.write('\nCost of minimum spanning tree: ' + str(cost) + '\n')
    sys.stdout.flush()
    #sys.stdout.write('Edges of minimum spanning tree:\n')
    #sys.stdout.write(str(T) + '\n')
    #sys.stdout.flush()
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
