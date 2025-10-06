# -*- coding: utf-8 -*-
"""
Strongly Connected Components algorithm (Kosaraju's Two Pass algorithm).

A program for Stanford Algorithms Specialization 2 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #1 in the Course
https://www.coursera.org/learn/algorithms-graphs-data-structures/home/module/1
"""

import time
import sys

global t   # global variable for finishing times (needed in pass 1)
global s   # global variable for current source node (needed in pass 2)

def DFSloop(nodes, nodes_stat, adj_dict):
    """
    Outer loop for recursive Depth-First Search (DFS) algorithm..

    Arguments:
        nodes (list):
            List of all available nodes.
        nodes_stat (dict):
            Dictionary of nodes, providing a status list [ip, m, c] per node
            with the following information:
            ip: '0' not processed, '1' processed,
            m: 'magical number' = finishing time,
            l: leading node where DFS started so that node i was found.
        adj_dict (dict):
            Dictionary of nodes, matching every node to its adjacency list.

    Returns:
        nodes_stat (dict):
            Changed dictionary of nodes.
        nodes_new (list):
            List of all nodes, sorted in descending order by finishing time.
    """

    # Initialize global variables.
    global t
    global s
    t, s = 0, 0
    # Initialize nodes_new.
    nodes_new = []
    # Ensure to process all nodes with outer loop.
    for i in nodes:
        if nodes_stat[i][0] < 1:   # node i not yet processed
            # Update leading node number.
            s = i
            DFS(nodes, nodes_new, nodes_stat, adj_dict, s)
    return nodes_new

def DFS(nodes, nodes_new, nodes_stat, adj_dict, i):
    """
    Recursive Depth-First Search (DFS) algorithm..

    Arguments:
        nodes (list):
            List of all available nodes.
        nodes_new (list):
            List of all nodes, sorted in descending order by finishing time.
        nodes_stat (dict):
            Dictionary of nodes, providing a status list [ip, m, c] per node
            with the following information:
            ip: '0' not processed, '1' processed,
            m: 'magical number' = finishing time,
            l: leading node where DFS started so that node i was found.
        adj_dict (dict):
            Dictionary of nodes, matching every node to its adjacency list.
        i (int):
            Node number to start the DFS search from.

    Returns:
        nodes_new (list):
            Changed list of all nodes, sorted in descending order
            by finishing time.
        nodes_stat (dict):
            Changed dictionary of nodes.
    """

    global t
    global s
    # Mark node i as explored in current pass.
    nodes_stat[i][0] += 1
    # Set leading node.
    nodes_stat[i][2] = s
    # Process successors of i from adjacency list.
    adj_list = adj_dict[i]
    for j in adj_list:   # inner loop
        if nodes_stat[j][0] < 1:   # node j not yet processed
            DFS(nodes, nodes_stat, adj_dict, j)
    # Increment and set finishing time for node i.
    t += 1
    nodes_stat[i][1] = t
    # Insert node i into nodes_new in descending order by finishing time.
    nodes_new.insert(0, i)
    return

def DFSiter(nodes, nodes_stat, adj_dict):
    """
    Iterative Depth-First Search (DFS) algorithm..

    Arguments:
        nodes (list):
            List of all available nodes.
        nodes_stat (dict):
            Dictionary of nodes, providing a status list [ip, m, c] per node
            with the following information:
            ip: '0' not processed, '1' processed,
            m: 'magical number' = finishing time,
            l: leading node where DFS started so that node i was found.
        adj_dict (dict):
            Dictionary of nodes, matching every node to its adjacency list.

    Returns:
        nodes_stat (dict):
            Changed dictionary of nodes.
        nodes_new (list):
            List of all nodes, sorted in descending order by finishing time.
    """

    # Initialize global variables.
    global t
    global s
    t, s = 0, 0
    # Initialize nodes_new.
    nodes_new = []
    # Initialize stack.
    stack = []
    # Ensure to process all nodes with outer loop.
    for i in nodes:
        if nodes_stat[i][0] < 1:   # node i not yet processed
            # Put node i on stack.
            stack.insert(0, i)
            # Update leading node number.
            s = i
            # Mark node i as explored in current pass.
            nodes_stat[i][0] += 1
            # The leading node will however only be set once also all
            # successors have been explored.
            # Process stack in inner loop.
            while stack:   # as long as the stack is not empty
                j = stack[0]   # keep node j on stack for now
                # Check if all successors of node j have been explored,
                # by checking the flag for the leading node.
                if nodes_stat[j][2] > -1:
                    # Processing node j for the second time.
                    # Increment and set finishing time for node j.
                    t += 1
                    nodes_stat[j][1] = t
                    # Insert node j into nodes_new in descending order
                    # by finishing time.
                    nodes_new.insert(0, j)
                    # Remove node j from stack.
                    stack.pop(0)
                else: 
                    # Process successors of j from adjacency list.
                    adj_list = adj_dict[j]
                    tmp_list = []
                    for k in adj_list:   # inner loop
                        if nodes_stat[k][0] < 1:   # node k not explored
                            # Prepare node k to be put on stack.
                            tmp_list.append(k)
                            # Mark node k as explored in current pass.
                            nodes_stat[k][0] += 1
                    if tmp_list:   # unexplored successors have been found
                        # Add successors on top of stack.
                        stack = tmp_list + stack
                    # Set leading node for node j.
                    nodes_stat[j][2] = s
    return nodes_new

def extractSCC(nodes_stat):
    """
    Extract strongly connected components (SCCs) from nodes_stat.

    Arguments:
        nodes_stat (dict):
            Dictionary of nodes, providing a status list [ip, m, c] per node
            with the following information:
            ip: '0' not processed, '1' processed,
            m: 'magical number' = finishing time,
            l: leading node where DFS started so that node i was found.

    Returns:
        components (dict):
            Dictionary of leading nodes and the number of nodes in their
            strongly connected component (SCC).
        sizes (list):
            List of sizes of SCCs.
    """

    # Initialize statistics of components.
    components = {}
    sizes = []
    # Evaluate all nodes with respect to their leading nodes.
    for i in nodes_stat:
        leading_node = nodes_stat[i][2]
        if leading_node in components:
            components[leading_node] += 1
        else:
            components[leading_node] = 1
    # Extract the sizes of components into a list.
    # Remark: the following steps destroy the linear execution time
    # of Kosaraju's algorithm.
    # Using the DSelect algorithm, we could nonetheless determine
    # the 10 largest SCCs still in linear time.
    # However, we assume that the number of SCCs is much smaller than
    # the number of nodes, so we can afford to create a list with unique sizes
    # and sort the list.
    for i in components:
        s = components[i]
        if not s in sizes:
            sizes.append(s)
    sizes.sort(reverse=True)   # descending by size
    return components, sizes

def read_list(file_name, reverse=False):
    """
    Read source data of directed edges (arcs).
    Every row starts with the tail node of an arc, followed by 1 or several
    tail nodes for arcs.

    Arguments:
        file_name (str):
            File name to be read.
        reverse (bool):
            Flag defining whether the meaning of tails and heads in the
            input file shall be reversed.

    Returns:
        status (int):
            '0' indicates successful processing, '1' that an error ocurred.
        nodes (list):
            List of all available nodes.
        nodes_stat (dict):
            Dictionary of nodes, providing a status list [ip, m, c] per node
            with the following information:
            ip: '0' not processed, '1' processed,
            m: 'magical number' = finishing time,
            l: leading node where DFS started so that node i was found.
            Will be initialized in this method by [0, -1, -1].
        adj_dict (dict):
            Dictionary of nodes, matching every node to its adjacency list.
    """

    # Initialize structures.
    nodes = []
    nodes_stat = {}
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
                    node = int(j[1])
                    # Check if node is already in adj_dict.
                    if not node in adj_dict:
                        # Create an empty entry for now.
                        nodes.append(node)
                        nodes_stat[node] = [0, -1, -1]
                        adj_dict[node] = []
                    if j[0] == 0:
                        node_1 = node
                    else:
                        node_2 = node
                        if reverse:
                            # node_1 is tail, node_1 is head of arc.
                            # Insert node_1 into adj_dict entry for node_2.
                            adj_list = adj_dict[node_2]
                            adj_list.append(node_1)
                        else:
                            # node_1 is head, node_2 is tail of arc.
                            row_list.append(node_2)
                            # Insert row_list into adj_dict entry for node_1.
                            adj_list = adj_dict[node_1]
                            adj_list += row_list
        return 0, nodes, nodes_stat, adj_dict
    except:
        return 1, nodes, nodes_stat, adj_dict

# Main programm
def runMe():
    file_name = 'SCC.txt'   # 1355 s = 23 min

    tic = time.perf_counter()
    # Pass 1 of Kosaraju's algorithm.
    sys.stdout.write('\nReading input data for pass 1.\n')
    sys.stdout.flush()
    # Read the graph input from file for reversed graph.
    status, nodes, nodes_stat, adj_dict = read_list(file_name, reverse=True)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of nodes: ' + str(len(nodes)) + '\n')
    sys.stdout.flush()
    sys.stdout.write('\nCalculating pass 1.\n')
    sys.stdout.flush()
    # Execute DFS on reversed graph.
    #nodes_new = DFSloop(nodes, nodes_stat, adj_dict)
    nodes_new = DFSiter(nodes, nodes_stat, adj_dict)
    # Pass 2 of Kosaraju's algorithm.
    sys.stdout.write('\nReading input data for pass 2.\n')
    sys.stdout.flush()
    # Read the graph input from file for original graph.
    status, nodes, nodes_stat, adj_dict = read_list(file_name, reverse=False)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('\nCalculating pass 2.\n')
    sys.stdout.flush()
    # Execute DFS on original graph with nodes in descending order
    # by finishing time.
    #DFSloop(nodes_new, nodes_stat, adj_dict)
    DFSiter(nodes_new, nodes_stat, adj_dict)
    #Extract strongly connected components (SCCs) from nodes_stat.
    sys.stdout.write('\nExtracting SCC sizes.\n')
    sys.stdout.flush()
    components, sizes = extractSCC(nodes_stat)
    sys.stdout.write('No. of SCCs: ' + str(len(components)) + '\n')
    sys.stdout.write('Sizes: ' + str(sizes) + '\n')
    sys.stdout.flush()
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
