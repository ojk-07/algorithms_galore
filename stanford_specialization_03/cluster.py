# -*- coding: utf-8 -*-
"""
Single-Link Clustering algorithm based on Kruskal's MST algorithm.

Kruskal's greedy algorithm calculates a minimal spanning tree in an
undirected graph with weigthed edges (weights can also be negative).
Running time: O(m log m) for a Graph with m edges and n vertices.

In the Single-Link Clustering application, edges represent dissimilarities
between the vertices.
For this excercise, the complete undirected graph of dissimilarities is
provided in a file.
The MST is represented by a union-find data structure.
The edges are sorted in ascending order with respect to edge cost by Heapsort.

A program for Stanford Algorithms Specialization 3 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #2 in the Course
https://www.coursera.org/learn/algorithms-greedy/home/module/2
"""

import elements   as el
import heaptools  as ht
import union_find as uf
import time
import sys

def slc(k, n_vertices, edges):
    """
    Calculate Single-Link Clustering for graph with edge weights denoting
    the dissimilarity (can also be negative) beween vertices.
    
    Arguments:
        k (int):
            Number of clusters to be calculated.
        n_vertices (int):
            Number of vertices.
            We assume that there are the vertices 1 ... n.
        edges (list):
            List of edges, matching every edge to the node element
            of class elem.
            elem.key: first vertex of the edge
            elem.val: distance between vertices
            elem.idx: index of node within heap structure, -1 if not in heap
            elem.ref: second vertex of the edge
    
    Returns:
        n_clusters:
            Number of clusters that has been reached.
        min_dist (int or float):
            Minimum distance of Single-Link Clustering.
        T (list):
            List of edges as node tuples (v, w) that have been utilized for
            cluster merge.
    """

    # Initialize data structures.
    T = []         # edges utilized for cluster merge
    X = []         # edges processed so far
    min_dist = 0   # minimum distance of Single-Link Clustering
    # Initialize union-find structure, representing the clusters.
    parents    = list(range(1, n_vertices + 1))   # each vertex in own cluster
    ranks      = [0] * n_vertices                 # each vertex is a leaf
    n_clusters = n_vertices                       # number of clusters
    u = uf.union_find(parents, ranks)
    # Initialize heap, representing E - X.
    h = ht.heap(edges, update_idx=True)
    while n_clusters > max(k, 1):
        # Identify new edge.
        try:
            e = h.deletem(update_idx=True)
            # Check that this edge is not within the same cluster.
            s1 = u.find(e.key)
            s2 = u.find(e.ref)
            if s1 != s2:
                # Unite clusters s1 and s2.
                u.union(s1, s2)
                # Add edge to list of utilized edges.
                T.append((min(e.key, e.ref), max(e.key, e.ref)))
                # Decrease number of clusters.
                n_clusters -= 1
        except:
            # No more edges available, but cannot happen for a complete graph.
            # In this case, we only have 1 cluster left, and we report
            # mind_dist as the default value 0.
            return n_clusters, min_dist, T
        # Add e to X.
        X.append(e)
    # Targeted number of clusters has been reached,
    # calculate the minimum distance of Single-Link Clustering.
    if n_clusters > 1:
        # For only 1 cluster, we report mind_dist as the default value 0.
        # Therefore, nothing to do in that case.
        try:
            # The next heavier edge acros the remaining clusters determines
            # the minimum distance.
            found = False
            while not found:
                e = h.deletem(update_idx=True)
                # Check that this edge is not within the same cluster.
                s1 = u.find(e.key)
                s2 = u.find(e.ref)
                if s1 != s2:
                    # Edge across the remaining clusters found.
                    found = True
            min_dist = e.val
        except:
            # No more edges available, but cannot happen for a complete graph.
            # In this case, we report mind_dist as the default value 0.
            pass
    return n_clusters, min_dist, T

def read_list(file_name):
    """
    Read source data of undirected edges.
    Every row starts with a vertex, followed by a vertex and a weight.
    
    It is assumed that every undirected edge is only reported once.
    
    Arguments:
        file_name (str):
            File name to be read.
    
    Returns:
        status (int):
            '0' indicates successful processing, '1' that an error ocurred.
        n_vertices (int):
            Number of vertices.
            We assume that there are the vertices 1 ... n.
        edges (list):
            List of edges, matching every edge to the node element
            of class elem.
            The attribute key represents the first vertex of the edge,
            ref the second vertex and val the given weithts.
            For each node element, attribute idx is initialized with -1.
    """

    # Initialize structures.
    edges = []
    n_vertices = 0
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
                vertex1 = int(row[0])
                vertex2 = int(row[1])
                weight = int(row[2])
                n_vertices = max(n_vertices, vertex1, vertex2)
                # Create an entry for the edge.
                e = el.elem(vertex1, weight, -1, vertex2)
                # Append the edge to the list of edges.
                edges.append(e)
        return 0, n_vertices, edges
    except:
        return 1, n_vertices, edges

# Main programm
def runMe():
    file_name = 'clustering.txt'
    k = 4   # number of target clusters

    tic = time.perf_counter()
    sys.stdout.write('\nReading input data for Single-Link Clustering.\n')
    sys.stdout.flush()
    status, n_vertices, edges = read_list(file_name)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of vertices: ' + str(n_vertices) +
                     ', edges: ' + str(len(edges)) + '\n')
    sys.stdout.flush()
    sys.stdout.write('\nCalculate clustering.\n')
    sys.stdout.flush()
    n_clusters, min_dist, T = slc(k, n_vertices, edges)
    # Minimum spanning tree according to assignement.
    sys.stdout.write('\nMinimum cluster distance for k = ' +
                     str(n_clusters) + ': ' + str(min_dist) + '\n')
    sys.stdout.flush()
    #sys.stdout.write('Utilized edges for cluster merge:\n')
    #sys.stdout.write(str(T) + '\n')
    #sys.stdout.flush()
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
