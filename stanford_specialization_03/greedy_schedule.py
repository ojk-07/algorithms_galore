# -*- coding: utf-8 -*-
"""
Greedy schedule algorithm for calculating optimal scheduling of jobs with given
weights and lengths, such that the weighted sum of lengths becomes minimal.

Runtime: O(n log n) for n jobs.

A program for Stanford Algorithms Specialization 3 written by Oliver Kroneisen,
oliver@kroneisen.net

This program is related to the programming assignment #1 in the Course
https://www.coursera.org/learn/algorithms-greedy/home/module/1
"""

import time
import sys
import elements_adjusted as el
import heaptools         as ht

def read_list(file_name):
    """
    Read source data of job weights and lengths.
    The file starts with the total number of jobs.
    Then, every contains the job weight and length.

    Arguments:
        file_name (str):
            File name to be read.

    Returns:
        status (int):
            '0' indicates successful processing, '1' that an error ocurred.
        jobs (list):
            List of all jobs, containing elements with weight, length, and val
            attribute, where val will be used for scheduling.
    """

    # Initialize structures.
    jobs = []
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
                values = raw_data[i].split()
                w = int(values[0])
                l = int(values[1])
                #val = w - l   # heuristic val (wrong!)
                val = w/l     # heuristic val (correct!)
                e = el.elem(i-1, w, l, val, -1)
                # Add element to jobs list.
                jobs.append(e)
        return 0, jobs
    except:
        return 1, jobs

# Main programm
def runMe():
    file_name = 'jobs.txt'

    tic = time.perf_counter()
    sys.stdout.write('\nReading job input data.\n')
    sys.stdout.flush()
    status, jobs = read_list(file_name)
    if status:   # error in reading the input file
        sys.stdout.write('Error reading input data, stop.\n')
        sys.stdout.flush()        
        return
    sys.stdout.write('No. of jobs: ' + str(len(jobs)) + '\n')
    sys.stdout.flush()
    # Create heap for jobs.
    h = ht.heap(jobs, mintype=False, update_idx=True)   # maximum heap
    # Schedule jobs and update weighted sum.
    sys.stdout.write('\nCalculate schedule.\n')
    sys.stdout.flush()
    wsum = 0
    tfin = 0
    stop = False
    while not stop:
        # Identify next job.
        try:
            job = h.deletem(update_idx=True)
            #print('Schedule', job.key, job.weight, job.length, '->', job.val)
            # Update wsum.
            tfin += job.length
            wsum += job.weight*tfin
        except:
            # No more jobs to schedule.
            stop = True
    # Weighted sum accoridng to assignement.
    sys.stdout.write('\nWeighted sum: ' + str(wsum) + '\n')
    sys.stdout.flush()
    toc = time.perf_counter()
    print('\nExecution time: {0} ms'.format((toc - tic) * 1000))
    return

if __name__ == '__main__':
    runMe()
