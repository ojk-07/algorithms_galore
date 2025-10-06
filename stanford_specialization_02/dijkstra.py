# -*- coding: utf-8 -*-
"""
Dijkstra's algorithm for calculating shortest paths in a directed graph
with only none-negative edge weights.

A program for Stanford Algorithms Specialization 2 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #2 in the Course
https://www.coursera.org/learn/algorithms-graphs-data-structures/home/module/2
"""

import elements as el
import heaptools as ht
import time
import sys

global INF   # global variable to represent "infinite"
INF = 1000000 

def dijkstra_paths(nodes, adj_dict, s):
    """
    Calculate shortest paths for directed graph with non-negative edge
    weights from node start to all reachable nodes.

    Arguments:
        nodes (dict):
            Dictionary of nodes, matching every node key to the node element
            of class elem.
            elem.key: key of node
            elem.val: shortest path distance to start, initialized with INF
            elem.idx: index of node within heap structure, -1 if not in heap
            elem.ref: key of predecessor node on shortest path to start
        adj_dict (dict):
            Dictionary of nodes, matching every node to its adjacency list,
            including the weights of edges.
        s (elem):
            Start node.

    Returns:
        nodes (dict):
            Changed dictionary of nodes with updated val and ref attributes.
        X (list):
            List of all reachable nodes from start as elements of class elem.
    """

    # Initialize data structures:
    X = []   # nodes processed so far
    s.val = 0   # distance from start to start node s is 0
    s.ref = s.key   # predecessor of start node s is s itself
    # Initialize heap.
    nodes_list = []
    for i in nodes.values():
        nodes_list.append(i)
    h = ht.heap(nodes_list, update_idx=True)
    while True:
        # Identify new node.
        try:
            w = h.deletem(update_idx=True)
        except:
            # No more reachable nodes.
            return X
        # Update shortest path information.
        dw = w.val
        adj_list = adj_dict[w.key]
        for e in adj_list:   # edges of node w
            u = nodes[e[0]]  # head of edge e
            if u.idx > -1:   # only if u is still in heap
                d2 = dw + e[1]   # distance of u to s via w
                if d2 < u.val:
                    u.val = d2
                    u.ref = w.key
                    # Position of u may now be incorrect, delete u from heap.
                    h.delete(u.idx, update_idx=True)
                    # Insert u back into heap at right position.
                    h.insert(u, update_idx=True)
        # Add w to X.
        X.append(w.key)
    return X

def read_list(file_name):
    """
    Read source data of directed edges (arcs).
    Every row starts with the tail node of an arc, followed by 1 or several
    tuples of [tail nodes, weights] for arcs.

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
            for i in range(n):   # line number
                row_list = []
                # Evaluate current line.
                for j in enumerate(raw_data[i].split()):
                    if j[0] == 0:
                        node = int(j[1])
                        head = node
                    else:
                        node = int(j[1].split(',')[0])
                        weight = int(j[1].split(',')[1])
                    # Check if node is already in adj_dict.
                    if not node in adj_dict:
                        # Create an empty entry for now.
                        e = el.elem(node, INF, -1)
                        nodes[node] = e
                        adj_dict[node] = []
                    if j[0] > 0:
                        row_list.append([node, weight])
                # Insert row_list into adj_dict entry for head.
                adj_list = adj_dict[head]
                adj_list += row_list
        return 0, nodes, adj_dict
    except:
        return 1, nodes, adj_dict

# Main programm
def runMe():
    file_name = 'dijkstraData.txt'

    tic = time.perf_counter()
    sys.stdout.write('\nReading input data for Dijsktra.\n')
    sys.stdout.flush()
    status, nodes, adj_dict = read_list(file_name)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of nodes: ' + str(len(nodes)) + '\n')
    sys.stdout.flush()
    sys.stdout.write('\nCalculate shortest paths.\n')
    sys.stdout.flush()
    start = nodes[1]   # start with node '1'
    dijkstra_paths(nodes, adj_dict, start)
    # Shortest paths according to assignement.
    sys.stdout.write('\nResults for assignment:\n')
    sys.stdout.flush()
    list = [7, 37, 59, 82, 99, 115, 133, 165, 188, 197]
    for i in list:
        sys.stdout.write(str(nodes[i].val) + ',')
    sys.stdout.write('\n')
    sys.stdout.flush()
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
