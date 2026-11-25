# -*- coding: utf-8 -*-
"""
Algorithms for calculating All-Pairs Shortest Paths (APSP) for a directed graph
with eventually negative edge weights and negative-weight cycles.

This includes:
* Dijkstra's algorithm for calculating shortest paths in a directed graph
with only none-negative edge weights.
Running time of this binary heap based version:
O(m log n) instead of O(m + n log n)
* Bellman-Ford's algorithm for calculting shortest paths in a directed graph
with eventually negative edge weights and negative-weight cycles.
Running time: O(mn)
* Floyd-Warshall's algorithm for calculating all pairs of shortest paths in a
directed graph with eventually negative edge weights and
negative-weight cycles.
Running time: O(n³)
* Johnson's algorithm to reduce the calculation of all pairs of shortest paths
in a directed graph with eventually negative edge weights and
negative-weight cycles to a combination of Bellman-Ford and Dijkstra.
Running time of this version: O(mn log n) instead of O(mn + n² log n)

A program for Stanford Algorithms Specialization 4 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #1 in the Course
https://www.coursera.org/learn/algorithms-npcomplete/home/module/1
"""

import elements  as el
import heaptools as ht
import time
import sys
import copy
from math import inf as INF

def dijkstra_paths(vertices, adj_dict, s):
    """
    Calculate shortest paths for directed graph with non-negative edge
    weights from vertex start to all reachable vertices using
    Dijkstra's algorithm.
    
    The vertices dictionary will be changed in-place to contain updated val
    and ref attributes.
    
    Arguments:
        vertices (dict):
            Dictionary of vertices, matching every vertex key to a node element
            of class elem.
            elem.key: key of vertex
            elem.val: shortest path distance to start, initialized with INF
            elem.idx: index of node within heap structure, -1 if not in heap
            elem.ref: key of predecessor vertex on shortest path to start
        adj_dict (dict):
            Dictionary of vertices, matching every vertex to its
            adjacency list, including the weights of edges.
        s (elem):
            Start vertex.
    
    Returns:
        min_length (int):
            Length of shortest among the shortest paths, excluding the trivial
            path from start vertex s to s with length 0.
        dist (dict):
            Dictionary of distances from start vertex s to vertex j.
    """

    # Initialize data structures.
    min_length = INF   # length of shortest among the shortest paths
    dist = {}          # distances from start vertex s to vertex j
    X    = []          # vertices processed so far
    # Initialize vertices and heap.
    vertices_list = []
    for v in vertices.values():
        # Set default values.
        v.val = INF   # vertex not reachable from s
        v.idx = -1    # vertex not in heap
        v.ref = -1    # vertex has no predecessor on path from s
        vertices_list.append(v)
    # Special initialization for start vertex s.
    s.val = 0       # distance from start vertex s to vertex s is 0
    s.ref = s.key   # predecessor of start vertex s is s itself    
    h = ht.heap(vertices_list, update_idx=True)
    # Loop over all vertices.
    while True:
        # Identify new node.
        try:
            w = h.deletem(update_idx=True)
        except:
            # No more reachable vertices.
            break
        # Update shortest path information.
        dw = w.val
        adj_list = adj_dict[w.key]
        for e in adj_list:   # edges of vertex w
            u = vertices[e[0]]  # head of edge e
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
    # Update dictionary of distances.
    for v in vertices.values():
        dist[v.key] = v.val
        # Update minimum min_length, if necessary.
        if v != s and v.val < min_length:
            min_length = v.val
    return min_length, dist

def bellman_ford_paths(vertices, adj_dict, s):
    """
    Calculate shortest paths for directed graph with eventually negative
    edge weights and negative-weight cycles for all pairs of vertices
    using Floyd-Warshall's algorithm.
    
    The vertices dictionary will be changed in-place to contain updated val
    and ref attributes.
    
    Arguments:
        vertices (dict):
            Dictionary of vertices, matching every vertex key to a node element
            of class elem.
            elem.key: key of vertex
            elem.val: shortest path distance to start, initialized with INF
            elem.idx: index of node within heap structure, -1 if not in heap
            elem.ref: key of predecessor vertex on shortest path to start
        adj_dict (dict):
            Dictionary of vertices, matching every vertex to its
            adjacency list, including the weights of edges.
        s (elem):
            Start vertex.
    
    Returns:
        has_nwc (bool):
            Flag to indicate whether the graph contains negative-weight cycles.
            In this case, min_length and dist are empty.
        min_length (int):
            Length of shortest among the shortest paths, excluding the trivial
            path from start vertex s to s with length 0.
        dist (dict):
            Dictionary of distances from start vertex s to vertex j.
    """

    # Initialize data structures.
    n = len(vertices)    # number of vertices
    has_nwc    = False   # flag for negative-weight cycles
    min_length = INF     # length of shortest among the shortest paths
    dist       = {}      # distances from start vertex s to vertex j
    # Initialize vertices. We use the vertices objects instead of A[i, v]
    for v in vertices.values():
        # Set default values.
        v.val = INF   # vertex not reachable from s
        v.idx = -1    # vertex not in heap
        v.ref = -1    # vertex has no predecessor on path from s
    # Special initialization for start vertex s.
    s.val = 0       # distance from start vertex s to vertex s is 0
    s.ref = s.key   # predecessor of start vertex s is s itself
    # Iterate n times (at most).
    for i in range(n):
        has_changed = False
        # Store current distances of vertices in dictionary dist,
        # instead of A[i-1, v].
        for v in vertices.values():
            dist[v.key] = v.val
        # Loop over all vertices.
        for w in vertices.values():
            if dist[w.key] == INF:   # skip unreachable vertices
                continue
            # Loop over all neighbours of w.
            for neighbour in adj_dict[w.key]:
                v      = vertices[neighbour[0]]
                weight = neighbour[1]
                # Examine which case we are in.
                d = dist[w.key] + weight
                if d < v.val:
                    # Case 2.
                    has_changed = True
                    v.val = d
                    v.ref = w.key
                # Nothing to do in Case 1.
        # Terminate iterations if nothing has changed.
        if not has_changed:
            break
    # Check the n-th iteration for a change.
    if i+1 == n and has_changed:
        # The graph contains negative-weight cycles.
        has_nwc = True
        dist    = {}
        return has_nwc, min_length, dist
    # Update dictionary of distances.
    for v in vertices.values():
        dist[v.key] = v.val
        # Update minimum min_length, if necessary.
        if v != s and v.val < min_length:
            min_length = v.val
    return has_nwc, min_length, dist

def floyd_warshall_paths(n_vertices, edges):
    """
    Calculate shortest paths for directed graph with eventually negative
    edge weights and negative-weight cycles from vertex start to all
    reachable vertices using Bellman-Ford's algorithm.
    
    The vertices dictionary will not be changed in-place with respect to the
    val and ref attributes.
    
    Arguments:
        n_vertices (int):
            Number of vertices.
            We assume that there are the vertices 1 ... n.
        edges (list):
            List of edges in form of tuples (tail, head, weight).
    
    Returns:
        has_nwc (bool):
            Flag to indicate whether the graph contains negative-weight cycles.
            In this case, min_length and dist are empty.
        min_length (int):
            Length of shortest among all shortest paths, excluding the trivial
            paths from a vertex to itself with length 0.
        dist2D (list):
            2-D array of distances from vertex i to vertex j.
            Array indices are zero-based.
        intv2D (list):
            2-D array of keys of the intermediary vertex between vertex i and j
            that was used to create the final shortest path between i and j.
            Array indices are zero-based.
            Can be used to reconstruct the shortest paths.
    """

    # Initialize data structures.
    n = n_vertices       # number of vertices
    has_nwc    = False   # flag for negative-weight cycles
    min_length = INF     # length of shortest among the shortest paths
    # 2-D array of distances from vertex i to vertex j.
    dist2D     = [[INF for j in range(n)] for i in range(n)]
    # Update distances with base case information.
    for i in range(n):
        # Diagonal elements have length 0.
        dist2D[i][i] = 0
    for e in edges:
        # Update distances with edge weights for connected vertices.
        i, j, weight = e[0] - 1, e[1] - 1, e[2]
        dist2D[i][j] = min(dist2D[i][j], weight)   # new edges reduce weights
    # 2-D array for distances from previous iteration.
    dist2D_old = copy.deepcopy(dist2D)
    # 2-D array of intermediary vertices between vertex i and vertex j.
    # Initially, we assume that j would be reached directly from i, if at all.
    intv2D     = [[None for j in range(n)] for i in range(n)]
    # Iterate on allowed intermediary vertices.
    for k in range(n):
        has_changed = False
        print('Iteration', k+1)
        # Iterate on start vertices.
        for i in range(n):
            # Iterate on target vertices.
            for j in range(n):
                # Skip unreachable vertices.
                if dist2D_old[i][k] == INF or dist2D_old[k][j] == INF:
                    continue
                # Examine which case we are in.
                d = dist2D_old[i][k] + dist2D_old[k][j]
                if d < dist2D_old[i][j]:
                    # Case 2.
                    has_changed = True
                    dist2D[i][j] = d
                    intv2D[i][j] = k+1
                # Nothing to do in Case 1.
            # Check for negative-weight cycles.
            if dist2D[i][i] < 0:
                has_nwc = True
                dist2D  = []
                intv2D  = []
                return has_nwc, min_length, dist2D, intv2D
        # Copy array dist2D to dist2D_old.
        if has_changed:
            dist2D_old = copy.deepcopy(dist2D)
    # Calculate length of shortest among all shortest paths.
    for i in range(n):
        for j in range(n):
            if i != j:
                d = dist2D[i][j]
                # Update minimum min_length, if necessary.
                if d < min_length:
                    min_length = d
    return has_nwc, min_length, dist2D, intv2D

def johnson_paths(vertices, adj_dict):
    """
    Calculate shortest paths for directed graph with eventually negative
    edge weights and negative-weight cycles for all pairs of vertices
    using Johnson's algorithm.
    
    The vertices and adj_dict dictionary will not be changed.
    
    Arguments:
        vertices (dict):
            Dictionary of vertices, matching every vertex key to a node element
            of class elem.
            elem.key: key of vertex
            elem.val: shortest path distance to start, initialized with INF
            elem.idx: index of node within heap structure, -1 if not in heap
            elem.ref: key of predecessor vertex on shortest path to start
        adj_dict (dict):
            Dictionary of vertices, matching every vertex to its
            adjacency list, including the weights of edges.
    
    Returns:
        has_nwc (bool):
            Flag to indicate whether the graph contains negative-weight cycles.
            In this case, min_length and dist are empty.
        min_length (int):
            Length of shortest among all shortest paths, excluding the trivial
            paths from a vertex to itself with length 0.
        dist2D (list):
            2-D array of distances from vertex i to vertex j.
            Array indices are zero-based.
        pred2D (list):
            2-D array of keys of the predecessor vertex of vertex j
            on the final shortest path between i and j.
            Array indices are zero-based.
            Can be used to reconstruct the shortest paths.
    """

    # Initialize data structures.
    n = len(vertices)    # number of vertices
    has_nwc    = False   # flag for negative-weight cycles
    min_length = INF     # length of shortest among the shortest paths
    # 2-D array of distances from vertex i to vertex j.
    dist2D     = [[INF for j in range(n)] for i in range(n)]
    # 2-D array of predecessors on shortest path from vertex i to vertex j.
    pred2D     = [[-1 for j in range(n)] for i in range(n)]
    # Create deepcopies of the original dictionaries.
    vertices_copy = copy.deepcopy(vertices)
    adj_dict_copy = copy.deepcopy(adj_dict)
    # Create artifical vertex s, connected with all vertices with weight 0.
    s_key = 0   # artifical source vertex s named as 0
    s = el.elem(s_key, INF)
    adj_list = []
    for v in vertices_copy.values():   # loop over all original vertices
        adj_list.append([v.key, 0])
    vertices_copy[s_key] = s
    adj_dict_copy[s_key] = adj_list
    # Calculate values of potential p with Bellman-Ford's algorithm.
    print('Calculating potential p.')
    has_nwc, _, p = bellman_ford_paths(vertices_copy, adj_dict_copy, s)
    if has_nwc:
        return has_nwc, min_length, dist2D, pred2D
    # Adjust weights in adj_dict dictionary.
    print('Adjusting edge weights.')
    for w in vertices_copy.values():   # loop over all vertices
        if w == s:   # skip artificial vertex s
            continue
        adj_list = adj_dict_copy[w.key]
        for neighbour in adj_list:   # loop over all neighbours of vertex w
            # Adjust edge weight.
            v_key        = neighbour[0]
            weight       = neighbour[1]
            neighbour[1] = weight + p[w.key] - p[v_key]
    # Calculate distances with Dijkstra's algorithm.
    iter = 0
    for w in vertices_copy.values():   # loop over all vertices
        if w == s:   # skip artificial vertex s
            continue
        print('Iteration', iter+1)
        _, dist = dijkstra_paths(vertices_copy, adj_dict_copy, w)
        # Correct distances according to potential p.
        min_length_w = INF
        for v in vertices_copy.values():   # loop over all vertices
            if w == s:      # skip artificial vertex s
                continue
            if dist[v.key] == INF:   # skip unreachable vertices
                continue
            d = dist[v.key] - p[w.key] + p[v.key]
            dist[v.key] = d
            if w != v and d < min_length_w:
                min_length_w = d
        # Update result arrays dist2D and pred2D.
        i = w.key-1
        for j in range(n):
            dist2D[i][j] = dist[j+1]
            pred2D[i][j] = vertices_copy[j+1].ref
        # Update minimum min_length, if necessary.
        if min_length_w < min_length:
            min_length = min_length_w
        iter += 1
    return has_nwc, min_length, dist2D, pred2D

def calc_path_from_pred(i, j, pred2D):
    """
    Calculate shortest paths from predecessor matrix for source vertex with
    zero-based index i and target vertex with zero-based index j.
    
    Arguments:
        i (int):
            Zero-based index of source vertex.
        j (int):
            Zero-based index of target vertex.
        pred2D (list):
            2-D array of keys of the predecessor vertex of vertex j
            on the final shortest path between i and j.
            Array indices are zero-based.
    
    Returns:
        path (list):
            Vertices on shortest path with vertices named 1 ... n.
            Returns an empty list if the target vertex is not reachable from
            the source vertex.
    """

    # Initialize data structures.
    path = []   # shortest path from source vertex to target vertex
    # Base case: target vertex is identical to source vertex.
    if i == j:
        return [i+1]
    # Reconstruct shortest path.
    pred = pred2D[i][j]
    if pred == -1:   # target vertex not reachable from source vertex
        return []
    else:
        path.insert(0, j+1)
    while pred != i+1:
        path.insert(0, pred)
        pred = pred2D[i][pred-1]
    path.insert(0, i+1)
    return path

def calc_path_from_intv(i, j, dist2D, intv2D):
    """
    Calculate shortest paths from intermediary vertex matrix for source vertex
    with zero-based index i and target vertex with zero-based index j.
    
    Arguments:
        i (int):
            Zero-based index of source vertex.
        j (int):
            Zero-based index of target vertex.
        dist2D (list):
            2-D array of distances from vertex i to vertex j.
            Array indices are zero-based.
        intv2D (list):
            2-D array of keys of the intermediary vertex between vertex i and j
            that was used to create the final shortest path between i and j.
            Array indices are zero-based.
    
    Returns:
        path (list):
            Vertices on shortest path with vertices named 1 ... n.
            Returns an empty list if the target vertex is not reachable from
            the source vertex.
    """

    # Check if target vertex is reachable from source vertex.
    if dist2D[i][j] == INF:
        return []
    # Base case 1: target vertex is identical to source vertex.
    if i == j:
        return [i+1]
    # Determine intermediate vertex.
    k = intv2D[i][j]
    # Base case 2: no intermediary vertex between source and target vertex.
    if k == None:
        return [i+1, j+1]
    # Recurse to reconstruct both parts of the shortest path.
    path_1 = calc_path_from_intv(i, k-1, dist2D, intv2D)
    path_2 = calc_path_from_intv(k-1, j, dist2D, intv2D)
    return path_1[:-1] + path_2

def calc_path_length(path, edges):
    """
    Calculate the total weight of a path.
    
    Arguments:
        path (list):
            Vertices on shortest path with vertices named 1 ... n.
        edges (list):
            List of edges in form of tuples (tail, head, weight).
    
    Returns:
        length (int or float):
            Length of the input path.
    """

    # Initialize data structures.
    length = 0
    # Handle path with only one vertex, which is understood as zero length.
    if len(path) == 1:
        return 0
    # Determine weights along the path.
    for u, v in zip(path[:-1], path[1:]):
        weights = [w for tail, head, w in edges
                   if tail == u and head == v]
        # Handle case that there are no edges for the path.
        if not weights:
            return INF
        # Update path length.
        length += min(weights)
    return length

def read_edges_list(file_name):
    """
    Read source data of directed edges (arcs) in edges list format.
    Every row starts with the tail vertex of an arc, followed by the head
    vertex and the weight for the arc.
    
    Arguments:
        file_name (str):
            File name to be read.
    
    Returns:
        status (int):
            '0' indicates successful processing, '1' that an error ocurred.
        n_vertices (int):
            Number of vertices.
            We assume that there are the vertices 1 ... n.
        n_edges (int):
            Number of edges.
            We assume that there are the edges 1 ... m.
        has_nwe (bool):
            Flag to indicate whether the graph contains any negative-weight
            edges.
        edges (list):
            List of edges in form of tuples (tail, head, weight).
        vertices (dict):
            Dictionary of vertices, matching every vertex key to a node element
            of class elem.
            For each node element, attribute val is initialized with INF,
            (and by default idx and ref with -1).
        adj_dict (dict):
            Dictionary of vertices, matching every vertex key to its adjacency
            list, including the weights of edges.
    """

    # Initialize data structures.
    has_nwe    = False   # flag for negative-weight edges
    n_vertices = 0
    n_edges    = 0
    edges      = []
    vertices   = {}
    adj_dict   = {}
    # Read list data from file.
    # Each row represents 1 item of the list.
    try:
        with open(file_name, 'r') as f:
            # Read data from file.
            raw_data = f.readlines()
            n = len(raw_data)
            # Evaluate first line.
            row = raw_data[0].split()
            n_vertices_input = int(row[0])
            n_edges_input    = int(row[1])
            # Evaluate all other lines.
            for i in range(1, n):   # line number
                # Evaluate current line.
                row = raw_data[i].split()
                tail   = int(row[0])
                head   = int(row[1])
                weight = int(row[2])
                if weight < 0:
                    has_nwe = True
                # Add edge to list of edges.
                edges.append((tail, head, weight))
                # Check if tail already is in adj_dict.
                if not tail in adj_dict:
                    # Create an empty entry for now.
                    e = el.elem(tail, INF)
                    vertices[tail] = e
                    adj_dict[tail] = []
                # Check if head already is in adj_dict.
                if not head in adj_dict:
                    # Create an empty entry for now.
                    e = el.elem(head, INF)
                    vertices[head] = e
                    adj_dict[head] = []
                # Add edge to adjacency list in adj_dict entry for tail.
                adj_list = adj_dict[tail]
                adj_list.append([head, weight])
        n_vertices = len(vertices)
        n_edges    = len(edges)
        assert n_vertices == n_vertices_input
        assert n_edges    == n_edges_input
        return 0, n_vertices, n_edges, has_nwe, edges, vertices, adj_dict
    except:
        return 1, n_vertices, n_edges, has_nwe, edges, vertices, adj_dict

def read_adjacency_list(file_name):
    """
    Read source data of directed edges (arcs) in adjacency list format.
    Every row starts with the tail vertex of an arc, followed by 1 or several
    tuples of [head vertex, weight] for arcs.
    
    Arguments:
        file_name (str):
            File name to be read.
    
    Returns:
        status (int):
            '0' indicates successful processing, '1' that an error ocurred.
        n_vertices (int):
            Number of vertices.
            We assume that there are the vertices 1 ... n.
        n_edges (int):
            Number of edges.
            We assume that there are the edges 1 ... m.
        has_nwe (bool):
            Flag to indicate whether the graph contains any negative-weight
            edges.
        edges (list):
            List of edges in form of tuples (tail, head, weight).
        vertices (dict):
            Dictionary of vertices, matching every vertex key to a node element
            of class elem.
            For each node element, attribute val is initialized with INF,
            (and by default idx and ref with -1).
        adj_dict (dict):
            Dictionary of vertices, matching every vertex key to its adjacency
            list, including the weights of edges.
    """

    # Initialize data structures.
    has_nwe    = False   # flag for negative-weight edges
    n_vertices = 0
    n_edges    = 0
    edges      = []
    vertices   = {}
    adj_dict   = {}
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
                        vertex = int(j[1])
                        tail = vertex
                    else:
                        vertex = int(j[1].split(',')[0])
                        weight = int(j[1].split(',')[1])
                        if weight < 0:
                            has_nwe = True
                    # Check if vertex already is in adj_dict.
                    if not vertex in adj_dict:
                        # Create an empty entry for now.
                        e = el.elem(vertex, INF)
                        vertices[vertex] = e
                        adj_dict[vertex] = []
                    if j[0] > 0:
                        row_list.append([vertex, weight])
                        # Add edge to list of edges.
                        edges.append((tail, vertex, weight))
                # Insert row_list into adj_dict entry for tail.
                adj_list = adj_dict[tail]
                adj_list += row_list
        n_vertices = len(vertices)
        n_edges    = len(edges)
        return 0, n_vertices, n_edges, has_nwe, edges, vertices, adj_dict
    except:
        return 1, n_vertices, n_edges, has_nwe, edges, vertices, adj_dict

# Main programm
def runMe():
    #file_name = 'dijkstra.txt'
    #file_name = 'g1.txt'
    #file_name = 'g2.txt'
    #file_name = 'g3.txt'
    file_name = 'large.txt'

    tic = time.perf_counter()
    sys.stdout.write('\nReading input data for All-Pairs Shortest Paths.\n')
    sys.stdout.flush()
    #status, n, m, has_nwe, edges, vertices, adj_dict\
    #    = read_adjacency_list(file_name)
    status, n, m, has_nwe, edges, vertices, adj_dict\
        = read_edges_list(file_name)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of vertices: ' + str(n) +
                     ', no. of edges: ' + str(m) + '\n')
    sys.stdout.flush()
    if has_nwe:
        msg = 'The graph contains edges with negative weights.\n'
    else:
        msg = 'The graph does not contain edges with negative weights.\n'
    sys.stdout.write(msg)
    sys.stdout.flush()
    sys.stdout.write('\nCalculating shortest paths.\n')
    sys.stdout.flush()
    has_nwc = False   # assume no negative-weight cycles

    # Simple case for fixed start vertex.
    #start = vertices[1]   # start with vertex '1'
    #min_length, dist = dijkstra_paths(vertices, adj_dict, start)
    #if has_nwe:
    #    sys.stdout.write('Warning! Dijkstra's result may be incorrect.\n')
    #sys.stdout.write('Shortest length among shortest paths from vertex ' +
    #                 str(start.key) + ': ' + str(min_length) + '\n')
    #sys.stdout.flush()
    #has_nwc, min_length, dist = bellman_ford_paths(vertices, adj_dict, start)
    #sys.stdout.write('\nResults for simple case with fixed start vertex:\n')
    #sys.stdout.flush()
    #if has_nwc:
    #    sys.stdout.write('The graph contains negative-weight cyclces.\n')
    #else:
    #    sys.stdout.write('Shortest length among shortest paths from vertex ' +
    #                     str(start.key) + ': ' + str(min_length) + '\n')
    #sys.stdout.flush()

    # Calculation of all pairs.
    #has_nwc, min_value, dist2D, intv2D = floyd_warshall_paths(n, edges)
    #path = calc_path_from_intv(0, 999, dist2D, intv2D)
    #length = calc_path_length(path, edges)
    #assert dist2D[0][999] == length
    has_nwc, min_value, dist2D, pred2D = johnson_paths(vertices, adj_dict)
    #path = calc_path_from_pred(0, 999, pred2D)
    #length = calc_path_length(path, edges)
    #assert dist2D[0][999] == length
    # Shortest paths according to assignment.
    sys.stdout.write('\nResults for assignment:\n')
    sys.stdout.flush()
    if has_nwc:
        sys.stdout.write('The graph contains negative-weight cyclces.\n')
    else:
        sys.stdout.write('Shortest length among all shortest paths: ' +
                         str(min_value) + '\n')
    sys.stdout.flush()

    # Primitive approach: run Bellman-Ford for all start vertices.
    #min_value = INF
    #iter = 0
    #for s in vertices.values():
    #    print('Iteration', iter+1)
    #    has_nwc, min_length, dist = bellman_ford_paths(vertices, adj_dict, s)
    #    if has_nwc:
    #        break
    #    if min_length < min_value:
    #        min_value = min_length
    #    iter += 1
    #sys.stdout.write('\nResults for assignment:\n')
    #sys.stdout.flush()
    #if has_nwc:
    #    sys.stdout.write('The graph contains negative-weight cyclces.\n')
    #else:
    #    sys.stdout.write('Shortest length among all shortest paths: ' +
    #                     str(min_value) + '\n')
    #sys.stdout.flush()

    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
