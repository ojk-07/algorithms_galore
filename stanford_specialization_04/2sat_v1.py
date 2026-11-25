# -*- coding: utf-8 -*-
"""
2SAT satisfaction problem based on Papadimitriou's randomized algorithm,
running time: O(n² log n),
or Kosaraju's algorithm for strong connected components, where n is the number
of variables and m the number of clauses,
running time: O(n + m).

A program for Stanford Algorithms Specialization 4 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #4 in the Course
https://www.coursera.org/learn/algorithms-npcomplete/home/module/4
"""

import time
import sys
import os
import math
import random as rd

t = 0   # global variable for finishing times (needed in scc pass 1)
s = 0   # global variable for current source vertex (needed in scc pass 2)

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

def build_implication_graph(n_vars, clauses):
    """
    Build implication graph from list of clauses for 2SAT.
    
    In this version, the adjacency lists for the original graph and the
    graph with all directed edges inversed are created.
    
    Arguments:
        n_vars (int):
            Number of variables.
            We assume that there are the variables 1 ... n.
        clauses (list):
            List of clauses, where the variables are defined by a tuple
            (var1, var2).
    
    Returns:
        vertices (list):
            List of the vertices of the implication graph.
            The vertices -n ... -1 and 1 ... n are mapped to the positions
            0 ... n-1 and n ... 2n-1, where the range 0 ... n-1 stands for
            the variable literals ~x_i and the range n ... 2n-1 stands for
            the variable literals x_i. The mapping is as follows:
            pos(x_i) = x_i + n - 1 for x_i > 0,
            pos(x_i) = x_i + n     for x_i < 0.
        vertex_status (dict):
            Dictionary of vertices, providing a status list [ip, m, c]
            per vertex with the following information:
            ip: 0 not processed, 1 processed,
            m: 'magical number' = finishing time,
            c: leading vertex where DFS started so that vertex i was found.
            Will be initialized in this method by [0, -1, 0].
        adj_dict (dict):
            Dictionary of vertices of the original graph, matching every
            vertex to its adjacency list.
            The dictionary contains entries for the literals x_i with positive
            sign and ~x_i with negative sign.
        adj_dict_rev (dict):
            Dictionary of vertices of the graph with reversed directed edges,
            matching every vertex to its adjacency list.
            The dictionary contains entries for the literals x_i with positive
            sign and ~x_i with negative sign.
    """

    # Initialize data structures.
    vertices      = []   # list of vertices
    vertex_status = {}   # status list per vertex
    adj_dict      = {}   # adjacency dictionary of the original graph
    adj_dict_rev  = {}   # adjacency dictionary of the reversed graph

    # Handle edge case.
    if n_vars < 0:
        msg = 'Number of variables must be non-negative.'
        raise ValueError(msg)
    
    if n_vars == 0:
        if clauses:
            msg = 'Clauses cannot contain variables '
            msg += 'when there are zero variables.'
            raise ValueError(msg)
        return vertices, vertex_status, adj_dict, adj_dict_rev

    # Create list of vertices.
    vertices = list(range(-n_vars, 0)) + list(range(1, n_vars+1))
    # Create dictionary vertex_status with initial values.
    for i in range (1, n_vars+1):
        vertex_status[i], vertex_status[-i] = [0, -1, 0], [0, -1, 0]

    # Loop over clauses and build adjacency dictionaries.
    for lit1, lit2 in clauses:
        # Check that literals are in the allowed range.
        if lit1 == 0 or abs(lit1) > n_vars or lit2 == 0 or abs(lit2) > n_vars:
            msg = 'Variable numbering is not in 1 ... #variables.'
            raise ValueError(msg)
        # In the original implication graph, ~lit1 points to lit2 and
        # ~lit2 to lit1.
        adj_list = adj_dict.get(-lit1)
        if adj_list is None:
            adj_dict[-lit1] = [lit2]
        else:
            adj_list.append(lit2)
            adj_dict[-lit1] = adj_list
        adj_list = adj_dict.get(-lit2)
        if adj_list is None:
            adj_dict[-lit2] = [lit1]
        else:
            adj_list.append(lit1)
            adj_dict[-lit2] = adj_list
        # In the reversed implication graph, lit1 points to ~lit2 and
        # lit2 points to ~lit1.
        adj_list = adj_dict_rev.get(lit1)
        if adj_list is None:
            adj_dict_rev[lit1] = [-lit2]
        else:
            adj_list.append(-lit2)
            adj_dict_rev[lit1] = adj_list
        adj_list = adj_dict_rev.get(lit2)
        if adj_list is None:
            adj_dict_rev[lit2] = [-lit1]
        else:
            adj_list.append(-lit1)
            adj_dict_rev[lit2] = adj_list

    return vertices, vertex_status, adj_dict, adj_dict_rev

def calc_2sat_from_scc(n_vars, vertex_status):
    """
    Check for satisfyability of the 2SAT instance and construct a satisfying
    assignment, if possible, by inspecting the vertices' scc stored in
    vertex_stat.
    
    Arguments:
        n_vars (int):
            Number of variables.
            We assume that there are the variables 1 ... n.
        vertex_status (dict):
            Dictionary of vertices, providing a status list [ip, m, c]
            per vertex with the following information:
            ip: 0 not processed, 1 processed,
            m: 'magical number' = finishing time,
            c: leading vertex where DFS started so that vertex i was found.
    
    Returns:
        is_solvable (bool):
            Flag whether the 2SAT instance is satisfiable.
        solution (list):
            Satisfying assignment for the 2SAT instance, if it has been found.
    """

    # Initialize data structures.
    is_solvable = True   # flag whether 2SAT instance is satisfiable
    solution    = []     # satisfying assignment for the 2SAT instance

    # Check wether some literals x_i and ~x_i belong to the same scc.
    for i in range(1, n_vars+1):
        if vertex_status[i][2] == vertex_status[-i][2]:
            is_solvable = False
            return is_solvable, solution

    # Construct satisfying assignment.
    for i in range(1, n_vars+1):
        if vertex_status[i][1] < vertex_status[-i][1]:
            solution.append(True)
        else:
            solution.append(False)

    return is_solvable, solution

def calc_2sat_randomized(n_vars, clauses, seed=None):
    """
    Search a satisfying assignment for the 2SAT instance using
    Papadimitriou's randomized algorithm.
    
    Arguments:
        n_vars (int):
            Number of variables.
            We assume that there are the variables 1 ... n.
        clauses (list):
            List of clauses, where the variables are defined by a tuple
            (var1, var2).
    
    Returns:
        is_solvable (bool):
            Flag whether the 2SAT instance is satisfiable.
        solution (list):
            Satisfying assignment for the 2SAT instance, if it has been found.
    """

    # Initialize data structures.
    tic         = time.perf_counter()
    is_solvable = False   # flag whether 2SAT instance is satisfiable
    solution    = []      # satisfying assignment for the 2SAT instance
    rd.seed(seed)         # initialize the random seed

    # Handle edge case.
    if n_vars < 0:
        msg = 'Number of variables must be non-negative.'
        raise ValueError(msg)
    
    if n_vars == 0:
        if clauses:
            msg = 'Clauses cannot contain variables '
            msg += 'when there are zero variables.'
            raise ValueError(msg)
        is_solvable = True
        return is_solvable, solution

    # Prepare adjacency list for variables to clauses.
    var_2_clauses = [[] for _ in range(n_vars)]
    for clause_idx, (lit1, lit2) in enumerate(clauses):
        # Check that literals are in the allowed range.
        if lit1 == 0 or abs(lit1) > n_vars or lit2 == 0 or abs(lit2) > n_vars:
            msg = 'Variable numbering is not in 1 ... #variables.'
            raise ValueError(msg)
        var_2_clauses[abs(lit1)-1].append(clause_idx)
        if lit2 != lit1:
            var_2_clauses[abs(lit2)-1].append(clause_idx)
    print('Variables to clauses dictionary created.')

    # Outer loop.
    n_outer_iterations = int(math.log2(n_vars)) + 1
    n_inner_iterations = 2*n_vars*n_vars
    mod_messages = n_inner_iterations//100
    for i in range(n_outer_iterations):
        # Print statistics for current iteration.
        toc = time.perf_counter()
        print(f'outer iteration = {i+1}, Δt = {toc-tic:.3f} s')
        # Determine random variable assignment as starting point.
        values_trial = []
        for j in range(n_vars):
            coin_flip = int(rd.random()*2)   # random integer 0 or 1
            values_trial.append(coin_flip == 1)
        # Determine non-satisfied clauses.
        unsatisfied_list = []
        unsatisfied_pos  = {}
        for clause_idx, (lit1, lit2) in enumerate(clauses):
            # Check if clause is non-satisfied under current trial.
            val1 = values_trial[abs(lit1)-1]
            val2 = values_trial[abs(lit2)-1]
            if lit1 < 0:
                val1 = not val1
            if lit2 < 0:
                val2 = not val2
            satisfied = val1 or val2
            if not satisfied:
                unsatisfied_pos[clause_idx] = len(unsatisfied_list)
                unsatisfied_list.append(clause_idx)
        # Check for unsatisfied clauses.
        if len(unsatisfied_list) == 0:
            # Current trial satisfies 2SAT!
            is_solvable = True
            solution    = values_trial
            return is_solvable, solution                                

        # Inner loop: run 2n² local search trials.
        for j in range(n_inner_iterations):
            # Print statistics for current inner iteration.
            if mod_messages > 0 and j%(mod_messages) == 0:
                toc = time.perf_counter()
                print(f'inner iteration = {j+1}, Δt = {toc-tic:.3f} s')
            # Pick an unsatisfied clause.
            #unsatisfied_idx = rd.choice(unsatisfied_list)
            idx = int(rd.random()*len(unsatisfied_list))   # random idx
            unsatisfied_idx = unsatisfied_list[idx]
            lit1, lit2 = clauses[unsatisfied_idx]
            # Switch value of one of the two variables.
            coin_flip = int(rd.random()*2)   # random integer 0 or 1
            if coin_flip:   # interpret 0, 1 values as boolean
                # Switch value of second variable.
                var_idx = abs(lit2) - 1
            else:
                # Switch value of first variable.
                var_idx = abs(lit1) - 1
            values_trial[var_idx] = not values_trial[var_idx]
            # Update all affected clauses.
            for clause_idx in var_2_clauses[var_idx]:
                # Re-evaluate clause.
                lit1, lit2 = clauses[clause_idx]
                val1 = values_trial[abs(lit1)-1]
                val2 = values_trial[abs(lit2)-1]
                if lit1 < 0:
                    val1 = not val1
                if lit2 < 0:
                    val2 = not val2
                satisfied = val1 or val2
                if clause_idx in unsatisfied_pos:
                    if satisfied:
                        # Identify position of clause to remove.
                        pos = unsatisfied_pos.pop(clause_idx)
                        # Identify position of last unsatisfied clause.
                        last_pos = len(unsatisfied_list) - 1
                        # Swap last clause with clause to remove.
                        if pos != last_pos:
                            last_clause = unsatisfied_list[last_pos]
                            unsatisfied_list[pos] = last_clause
                            unsatisfied_pos[last_clause] = pos
                        # Remove clause from unsatisfied clauses in O(1).
                        unsatisfied_list.pop()
                else:
                    if not satisfied:
                        # Add new unsatisfied clause.
                        unsatisfied_pos[clause_idx] = len(unsatisfied_list)
                        unsatisfied_list.append(clause_idx)
            # Check for unsatisfied clauses.
            if len(unsatisfied_list) == 0:
                # Current trial satisfies 2SAT!
                is_solvable = True
                solution    = values_trial
                return is_solvable, solution                                
    # No solution found. We assume that there is no solution.
    # This is correct with probability >= 1 - 1/nvars.

    return is_solvable, solution

def validate_2sat_solution(clauses, solution):
    """
    Validate a 2SAT assignment against the clauses to ensure that it is a
    satisfying assignment.
    
    Arguments:
        clauses (list):
            List of clauses, where the variables are defined by a tuple
            (var1, var2).
        solution (list):
            Assignment for the 2SAT instance.
    
    Returns:
        is_correct (bool):
            Flag whether the assignment satisfies the 2SAT instance.
    """

    # Check against all clauses. 
    for lit1, lit2 in clauses:
        val1 = solution[abs(lit1)-1]
        val2 = solution[abs(lit2)-1]
        if lit1 < 0:
            val1 = not val1
        if lit2 < 0:
            val2 = not val2
        if not (val1 or val2):
            return False

    return True

def read_list(file_name):
    """
    Read source data of a 2SAT instance.
    The first row contains the number of variables.
    Every other row contains the 2 literals in an 'or' clause,
    where -7 would denote 'not x7' and 3 would denote 'x3'.
    
    Arguments:
        file_name (str):
            File name to be read.
    
    Returns:
        status (int):
            0 indicates successful processing, 1 that an error ocurred.
        n_vars (int):
            Number of variables.
            We assume that there are the variables 1 ... n.
        n_clauses (int):
            Number of clauses.
        clauses (list):
            List of clauses, where the variables are defined by a tuple
            (var1, var2).
    """

    # Initialize structures.
    clauses   = []
    n_clauses = 0
    n_vars    = 0

    # Read list data from file.
    # Each row represents 1 item of the list.
    try:
        with open(file_name, 'r') as f:
            # Read data from file.
            raw_data = f.readlines()
            n = len(raw_data)
            n_clauses = n - 1
            # Evaluate first line.
            row = raw_data[0].split()
            n_vars = int(row[0])
            # Evaluate all other lines.
            for i in range(1, n):   # line number
                # Evaluate current line.
                row = raw_data[i].split()
                var1 = int(row[0])
                var2 = int(row[1])
                # Add the variables to the list of clauses.
                clauses.append((var1, var2))
        return 0, n_vars, n_clauses, clauses
    except Exception as e:
        sys.stdout.write(f'read_list failed: {e!r} (cwd: {os.getcwd()})\n')
        n_vars, n_clauses, clauses = 0, 0, []
        return 1, n_vars, n_clauses, clauses

# Main program.
def runMe():
    #file_name = '2sat1.txt'   # satisfiable
    #file_name = '2sat2.txt'   # not satisfiable
    #file_name = '2sat3.txt'   # satisfiable
    #file_name = '2sat4.txt'   # satisfiable
    #file_name = '2sat5.txt'   # not satisfiable
    file_name = '2sat6.txt'   # not satisfiable

    tic = time.perf_counter()
    sys.stdout.write('\nReading input data for 2SAT Problem.\n')
    sys.stdout.flush()
    status, n_vars, n_clauses, clauses = read_list(file_name)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of variables: ' + str(n_vars) +
                     ', no. of clauses: ' + str(n_clauses) + '\n')
    sys.stdout.flush()
    sys.stdout.write('\nCalculate 2SAT assignment.\n')
    sys.stdout.flush()
    method = 2
    if method == 1:
        # Solve by Papadimitriou's randomized algorithm.
        seed = None
        is_solvable, solution = (
            calc_2sat_randomized(n_vars, clauses, seed=seed)
        )
    else:
        # Solve by Kosaraju's algorithm for strong connected components.
        sys.stdout.write('Build implication graph.\n')
        sys.stdout.flush()
        vertices_1, vertex_status, adj_dict, adj_dict_rev = (
            build_implication_graph(n_vars, clauses)
        )
        # Pass 1 of Kosaraju's algorithm:
        # Execute DFS on reversed graph.
        sys.stdout.write('Calculating pass 1.\n')
        sys.stdout.flush()
        vertices_2 = dfs_iter(vertices_1, vertex_status, adj_dict_rev)
        # Reset processing status and leading vertex in vertex_status
        # to prepare for second DFS run.
        for vertex in vertices_1:
            vertex_status[vertex][0], vertex_status[vertex][2] = 0, 0
        # Pass 2 of Kosaraju's algorithm:
        # Execute DFS on original graph with vertices in descending order
        # by finishing time.
        sys.stdout.write('Calculating pass 2.\n')
        sys.stdout.flush()
        dfs_iter(vertices_2, vertex_status, adj_dict)
        # Check satisfyability and extract satisfying assignment.
        sys.stdout.write('Construct 2SAT assignment.\n')
        sys.stdout.flush()
        is_solvable, solution = calc_2sat_from_scc(n_vars, vertex_status)
    # Satisfyability of 2SAT problem according to assignment.
    if is_solvable:
        # Check correctness of the solution.
        is_correct = validate_2sat_solution(clauses, solution)
        if is_correct:
            sys.stdout.write('\nThis 2SAT instance is satisfiable.\n')
            if n_vars <= 100:
                sys.stdout.write('Satisfying assignment of variables:\n')
                sys.stdout.write(str(solution) + '\n')
                sys.stdout.flush()
        else:
            sys.stdout.write('\nCalculated solution is not valid.\n')
    else:
        sys.stdout.write('\nThis 2SAT instance is not satisfiable.\n')
    sys.stdout.flush()
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
