# -*- coding: utf-8 -*-
"""
Strongly Connected Components algorithm (Kosaraju's Two Pass algorithm).
Running time O(n+m).

A program for Stanford Algorithms Specialization 2 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #1 in the Course
https://www.coursera.org/learn/algorithms-graphs-data-structures/home/module/1
"""

import time
import sys

t = 0   # global variable for finishing times (needed in pass 1)
s = 0   # global variable for current source node (needed in pass 2)

def dfs_loop(vertices, vertex_status, adj_dict):
    """
    Outer loop for recursive Depth-First Search (DFS) algorithm.
    
    The dictionary vertex_status is changed in-place.
    
    Arguments:
        vertices (list):
            List of all available vertices.
        vertex_status (dict):
            Dictionary of vertices, providing a status list [ip, m, c]
            per vertex with the following information:
            ip: 0 not processed, 1 processed,
            m: 'magical number' = finishing time,
            c: leading vertex where DFS started so that vertex i was found.
        adj_dict (dict):
            Dictionary of vertices, matching every vertex to its
            adjacency list.
    
    Returns:
        vertices_as_finished (list):
            List of all vertices, sorted in descending order by finishing time.
    """

    # Initialize global variables.
    global t, s
    t, s = 0, 0
    # Initialize vertices_as_finished.
    vertices_as_finished = []

    # Ensure to explore all vertices with outer loop.
    for root in vertices:
        if vertex_status[root][0] == 0:   # vertex root not yet explored
            # Update leading vertex number.
            s = root
            dfs(vertices, vertices_as_finished, vertex_status, adj_dict, s)

    return vertices_as_finished[::-1]   # return in inverted order

def dfs(vertices, vertices_as_finished, vertex_status, adj_dict, i):
    """
    Recursive Depth-First Search (DFS) algorithm.
    
    The dictionary vertex_status is changed in-place.
    
    Arguments:
        vertices (list):
            List of all available vertices.
        vertices_as_finished (list):
            List of all vertices, sorted in ascending order by finishing time.
        vertex_status (dict):
            Dictionary of vertices, providing a status list [ip, m, c]
            per vertex with the following information:
            ip: 0 not processed, 1 processed,
            m: 'magical number' = finishing time,
            c: leading vertex where DFS started so that vertex i was found.
        adj_dict (dict):
            Dictionary of vertices, matching every vertex to its
            adjacency list.
        i (int):
            Node number to start the DFS search from.
    
    Returns:
        vertices_as_finished (list):
            List of all vertices, sorted in ascending order by finishing time.
    """

    global t, s

    # Mark vertex i as explored in current pass.
    vertex_status[i][0] += 1
    # Set leading vertex.
    vertex_status[i][2] = s
    # Process successors of vertex i from adjacency list.
    adj_list = adj_dict[i]
    for j in adj_list:   # inner loop
        if vertex_status[j][0] == 0:   # vertex j not yet processed
            dfs(vertices, vertices_as_finished, vertex_status, adj_dict, j)
    # Increment and set finishing time for vertex i.
    t += 1
    vertex_status[i][1] = t
    # Insert vertex i into vertices_as_finished in ascending order
    # by finishing time.
    vertices_as_finished.append(i)

    return vertices_as_finished

def dfs_iter(vertices, vertex_status, adj_dict):
    """
    Iterative Depth-First Search (DFS) algorithm.
    
    The dictionary vertex_status is changed in-place.
    
    Arguments:
        vertices (list):
            List of all available vertices.
        vertex_status (dict):
            Dictionary of vertices, providing a status list [ip, m, c]
            per vertex with the following information:
            ip: 0 not processed, 1 processed,
            m: 'magical number' = finishing time,
            c: leading vertex where DFS started so that vertex i was found.
        adj_dict (dict):
            Dictionary of vertices, matching every vertex to its
            adjacency list.
    
    Returns:
        vertices_as_finished (list):
            List of all vertices, sorted in descending order by finishing time.
    """

    # Initialize global variables.
    global t, s
    t, s = 0, 0
    # Initialize vertices_as_finished.
    vertices_as_finished = []

    # Ensure to explore all vertices with outer loop.
    for root in vertices:
        if vertex_status[root][0] != 0:
            continue
        # Set value for current leading vertex s.
        s = root
        # Mark root vertex as explored in current pass.
        vertex_status[root][0] = 1
        # The current root is its own leading vertex.
        vertex_status[root][2] = s
        # Put root and its successors on stack.
        stack = [(root, iter(adj_dict.get(root, [])))]

        # Process stack.
        while stack:
            v, successors = stack[-1]
            # Try to explore the successors of current vertex v.
            try:
                w = next(successors)
                if vertex_status[w][0] == 0:   # w not yet explored
                    # Mark w as explored.
                    vertex_status[w][0] = 1
                    # Set current root as leading vertex for w.
                    vertex_status[w][2] = s
                    # Put w and its successors on stack.
                    stack.append((w, iter(adj_dict.get(w, []))))
            except StopIteration:
                stack.pop()   # the stack item is fully processed
                # Increment global finishing time.
                t += 1
                # Update the finishing time of vertex v.
                vertex_status[v][1] = t
                # Add vertex v to vertices_as_finished.
                # The list is in increasing order of finsihing times.
                vertices_as_finished.append(v)

    return vertices_as_finished[::-1]   # return in inverted order

def extract_scc(vertex_status):
    """
    Extract strongly connected components (SCCs) from vertex_status.
    
    Arguments:
        vertex_status (dict):
            Dictionary of vertices, providing a status list [ip, m, c]
            per vertex with the following information:
            ip: 0 not processed, 1 processed,
            m: 'magical number' = finishing time,
            c: leading vertex where DFS started so that vertex i was found.

    Returns:
        components (dict):
            Dictionary of leading vertices and the number of vertices in their
            strongly connected component (SCC).
        sizes (list):
            List of sizes of SCCs.
    """

    # Initialize statistics of components.
    components = {}
    sizes = []

    # Evaluate all vertices with respect to their leading vertices.
    for i in vertex_status:
        leading_vertex = vertex_status[i][2]
        if leading_vertex in components:
            components[leading_vertex] += 1
        else:
            components[leading_vertex] = 1
    # Extract the sizes of components into a list.
    # Remark: the following steps destroy the linear execution time
    # of Kosaraju's algorithm.
    # Using the DSelect algorithm, we could nonetheless determine
    # the 10 largest SCCs still in linear time.
    # However, we assume that the number of SCCs is much smaller than
    # the number of vertices, so we can afford to create a list with
    # unique sizes and sort the list.
    for i in components:
        s = components[i]
        if not s in sizes:
            sizes.append(s)
    sizes.sort(reverse=True)   # descending by size

    return components, sizes

def read_list(file_name, reverse=False):
    """
    Read source data of directed edges (arcs).
    Every row starts with the tail vertex of an arc, followed by 1 or several
    head vertices for arcs.
    
    Arguments:
        file_name (str):
            File name to be read.
        reverse (bool):
            Flag defining whether the meaning of tails and heads in the
            input file shall be reversed.
    
    Returns:
        status (int):
            0 indicates successful processing, 1 that an error ocurred.
        vertices (list):
            List of all available vertices.
        vertex_status (dict):
            Dictionary of vertices, providing a status list [ip, m, c]
            per vertex with the following information:
            ip: 0 not processed, 1 processed,
            m: 'magical number' = finishing time,
            c: leading vertex where DFS started so that vertex i was found.
            Will be initialized in this method by [0, -1, -1].
        adj_dict (dict):
            Dictionary of vertices, matching every vertex to its
            adjacency list.
    """

    # Initialize data structures.
    vertices = []
    vertex_status = {}
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
                # Evaluate current line.
                for j in enumerate(raw_data[i].split()):
                    vertex = int(j[1])
                    # Check if node is already in adj_dict.
                    if not vertex in adj_dict:
                        # Create an empty entry for now.
                        vertices.append(vertex)
                        vertex_status[vertex] = [0, -1, -1]
                        adj_dict[vertex] = []
                    if j[0] == 0:
                        vertex_1 = vertex
                    else:
                        vertex_2 = vertex
                        if reverse:
                            # vertex_2 is tail, vertex_1 is head of arc.
                            # Insert vertex_1 into adj_dict entry for vertex_2.
                            adj_list = adj_dict[vertex_2]
                            adj_list.append(vertex_1)
                        else:
                            # vertex_1 is head, vertex_2 is tail of arc.
                            # Insert vertex_2 into adj_dict entry for vertex_1.
                            adj_list = adj_dict[vertex_1]
                            adj_list.append(vertex_2)
        return 0, vertices, vertex_status, adj_dict
    except:
        return 1, vertices, vertex_status, adj_dict

# Main programm
def runMe():
    file_name = 'scc.txt'   # 35 s

    tic = time.perf_counter()
    # Pass 1 of Kosaraju's algorithm.
    sys.stdout.write('\nReading input data for pass 1.\n')
    sys.stdout.flush()
    # Read the graph input from file for reversed graph.
    status, vertices_1, vertex_status, adj_dict = (
        read_list(file_name, reverse=True)
    )
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of vertices: ' + str(len(vertices_1)) + '\n')
    sys.stdout.flush()
    sys.stdout.write('\nCalculating pass 1.\n')
    sys.stdout.flush()
    # Execute DFS on reversed graph.
    #vertices_2 = dfs_loop(vertices_1, vertex_status, adj_dict)
    vertices_2 = dfs_iter(vertices_1, vertex_status, adj_dict)
    # Since the data is read from file again, the processing status and 
    # leading vertex in vertex_status is automatically reset to prepare
    # for second DFS run.
    # Pass 2 of Kosaraju's algorithm.
    sys.stdout.write('\nReading input data for pass 2.\n')
    sys.stdout.flush()
    # Read the graph input from file for original graph.
    status, vertices_1, vertex_status, adj_dict = (
        read_list(file_name, reverse=False)
    )
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('\nCalculating pass 2.\n')
    sys.stdout.flush()
    # Execute DFS on original graph with vertices in descending order
    # by finishing time.
    #dfs_loop(vertices_2, vertex_status, adj_dict)
    dfs_iter(vertices_2, vertex_status, adj_dict)
    # Extract strongly connected components (SCCs) from vertex_status.
    sys.stdout.write('\nExtracting SCC sizes.\n')
    sys.stdout.flush()
    components, sizes = extract_scc(vertex_status)
    sys.stdout.write('No. of SCCs: ' + str(len(components)) + '\n')
    sys.stdout.write('Sizes: ' + str(sizes) + '\n')
    sys.stdout.flush()
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
