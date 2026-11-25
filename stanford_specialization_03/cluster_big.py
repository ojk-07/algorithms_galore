# -*- coding: utf-8 -*-
"""
Single-Link Clustering algorithm based on Kruskal's MST algorithm.

Kruskal's greedy algorithm calculates a minimal spanning tree in an
undirected graph with weigthed edges (weights can also be negative).
Running time: O(m log m) for a Graph with m edges and n vertices.

In the Single-Link Clustering application, edges represent dissimilarities
between the vertices.
For this excercise, the dissimilarities are provided implicitly by the
hamming distance associated to the bit codes of the vertices.
The MST is represented by a union-find data structure.

A program for Stanford Algorithms Specialization 3 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #2 in the Course
https://www.coursera.org/learn/algorithms-greedy/home/module/2
"""

import union_find as uf
import time
import sys

def slc_hamming(min_dist, vertices):
    """
    Calculate Single-Link Clustering for graph with hamming distances for
    dissimiliarities between vertices denoted by byte codes.
    
    Arguments:
        min_dist (int or float):
            Targeted minimum distance of Single-Link Clustering.
        vertices (list):
            List of vertices, where every vertex is given in terms of a
            bytes object.
    
    Returns:
        n_clusters:
            Number of clusters that has been reached.
        T (list):
            List of edges as node tuples (v, w) that have been utilized for
            cluster merge.
    """

    # Initialize data structures.
    T = []   # edges utilized for cluster merge
    # Initialize union-find structure, representing the clusters.
    n_vertices = len(vertices)
    parents    = list(range(1, n_vertices + 1))   # each vertex in own cluster
    ranks      = [0] * n_vertices                 # each vertex is a leaf
    n_clusters = n_vertices                       # number of clusters
    u = uf.union_find(parents, ranks)
    
    # Loop over all starting vertices to identify edges with a weight
    # not larger than min_dist.
    i = 0
    while i < len(vertices) - 1:
        print(f'i = {i}, #clusters = {n_clusters}')
        # Loop over all possible ending vertices.
        j = i + 1
        while j < len(vertices):
            # Calculate distance between vertices i and j.
            c = bytes(x ^ y for x, y in zip(vertices[i], vertices[j]))
            d = sum(x.bit_count() for x in c)
            if d < min_dist:
                # Merge the clusters that the vertices i and j belong to.
                si = u.find(i)
                sj = u.find(j)
                if si != sj:
                    # Unite clusters si and sj.
                    u.union(si, sj)
                    # Add edge to list of utilized edges.
                    T.append((i, j))
                    # Decrease number of clusters.
                    n_clusters -= 1
            # Increase ending vertex.
            j += 1
        # Increase starting vertex.
        i += 1
    # Targeted min_dist has been reached.
    return n_clusters, T

def read_list(file_name):
    """
    Read source data of vertices with bit code.
    Every contains a bit code denoting the characteristic of this vertex.
    
    It is assumed that every distinct vertex is only reported once.
    
    Arguments:
        file_name (str):
            File name to be read.
    
    Returns:
        status (int):
            '0' indicates successful processing, '1' that an error ocurred.
        vertices (list):
            List of vertices, where every vertex is given in terms of a
            bytes object.
    """

    # Initialize structures.
    vertices = []
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
                s = raw_data[i].replace(' ', '')
                b = int(s, 2).to_bytes((len(s) + 7) // 8, byteorder='big')
                # Append the bytes object to the list of vertices.
                vertices.append(b)
        return 0, vertices
    except:
        return 1, vertices

# Main program.
def runMe():
    file_name = 'clustering_big.txt'
    min_dist = 3   # targeted minimum distance of clustering

    tic = time.perf_counter()
    sys.stdout.write('\nReading input data for Single-Link Clustering.\n')
    sys.stdout.flush()
    status, vertices = read_list(file_name)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of vertices: ' + str(len(vertices)) + '\n')
    sys.stdout.flush()
    sys.stdout.write('\nCalculate clustering.\n')
    sys.stdout.flush()
    n_clusters, T = slc_hamming(min_dist, vertices)
    # Number of clusters according to assignment.
    sys.stdout.write('\nNumber of clusters for minimum distance = ' +
                     str(min_dist) + ': ' + str(n_clusters) + '\n')
    sys.stdout.flush()
    #sys.stdout.write('Utilized edges for cluster merge:\n')
    #sys.stdout.write(str(T) + '\n')
    #sys.stdout.flush()
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
