# -*- coding: utf-8 -*-
"""
Create input for selection and sorting algorithms.

A program for Stanford Algorithms Specialization written by Oliver Kroneisen,
oliver@kroneisen.net
"""

import random as rd

def write_list(file_name, nmin, nmax, mode=0):
    """
    Write list data to file, as input for selection and sorting algorithms.
    Each row represents 1 item of the list.
        
    Arguments:
        file_name (str):
            File name for the data to be written.
        nmin (int):
            Start value for test data.
        nmax (int):
            Stop value for test data.
        mode (int):
            1:    sorted numbers will be written.
            2:    identical numbers will be written.
            else: nmax - nmin + 1 randomly generated numbers with
                  nmin <= i <= nmax will be written.
    
    Returns:
        err (int):
            Indicator 0 for success and 1 for errors.
    """
    
    try:
        with open(file_name, 'w') as f:
            for i in range(nmax - nmin + 1):
                if mode == 1:
                    f.write('{0}\n'.format(nmin + i))
                elif mode == 2:
                    f.write('{0}\n'.format(nmin))
                else:
                    n = nmin + int(rd.random()*(nmax - nmin + 1))
                    f.write('{0}\n'.format(n))
        return 0
    except:
        return 1

if __name__ == '__main__':
    
    # Write test data to file.
    file_name = 'Test.txt'
    status = write_list(file_name, 1, 1000, mode=0)
    if status:
        print('Error when writing to the file.')
    else:
        print('Data successfully written to file.')
