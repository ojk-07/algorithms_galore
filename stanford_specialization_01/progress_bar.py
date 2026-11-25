# -*- coding: utf-8 -*-
"""
Progress Bar
"""

from time import sleep
import sys

# Main program.
def runMe():
    for i in range(21):
        sys.stdout.write('\r')
        # the exact output you're looking for:
        sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
        sys.stdout.flush()
        sleep(0.25)
    return

if __name__ == '__main__':
    runMe()
