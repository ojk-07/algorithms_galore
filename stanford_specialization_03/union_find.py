# -*- coding: utf-8 -*-
"""
Union-find class to be used as an imported module.

A method collection for Stanford Algorithms Specialization 3 written
by Oliver Kroneisen, oliver@kroneisen.net
"""

class union_find:
    """
    Class for union-find data structure including lazy unions, unions-by-rank
    and path compression, which provides a runtime complexity of O(m⋅α(n)).
    
    The elements are identified by their position in the list: element i is
    stored at position i-1. It is assumed that the elements are numbered from
    1 to n.
    The union-find data structure is array-like implemented using the lists
    parents and ranks.
    In order to test the data structure, it can be initialized by providing
    the optional lists parents and ranks, instead of inserting single elements.
    
    Arguments:
        parents (list):
            List of the parents of each element.
        ranks (list):
            List of the ranks of each element.
    """

    def __init__(self, parents=[], ranks=[]):
        """
        Initialize union-find data structure.
        
        Arguments:
            parents (list):
                List of the parents of each element.
            ranks (list):
                List of the ranks of each element.
        """

        assert len(parents) == len(ranks)
        self.parents = parents
        self.ranks   = ranks
        return

    def __str__(self):
        """
        Convert union-find data structure to string.
        
        Returns:
            text (str):
                Content of union-find data structure converted to a string.
        """

        text = 'Union-Find data structure'
        text += '\n  Parents: ' + str(self.parents)
        text += '\n  Ranks:   ' + str(self.ranks)
        return text

    def __repr__(self):
        """
        Represent union-find data structure as a string.
        
        Returns:
            text (str):
                Representation of union-find data structure.
        """

        return str(self)

    def make_set(self, parent=-1, rank=0):
        """
        Insert element into the union-find data structure.
        
        Arguments:
            parent (int):
                Parent of the element to be inserted.
                When the default value -1 is provided, the element will be
                its own parent, which denotes a root element.
            rank (int):
                Rank of the element to be inserted.
                Per default the rank is set to 0, which denotes a leaf element.
        """

        n = len(self.parents)   # number of elements in the data structure
        # Identify new element with id n+1.
        if parent == -1:
            self.parents.append(n+1)   # make new element its own parent
        else:
            self.parents.append(parent)
        self.ranks.append(rank)
        return

    def find(self, element):
        """
        Find the set the element belongs to.
        
        Arguments:
            element (int):
                Element whose set representative is to be found.
        """

        # Determine the set representative.
        s = element
        while self.parents[s-1] != s:
            s = self.parents[s-1]
        # Update the parents along the chain of the find operation with
        # this set representative (path compression).
        e = element
        while self.parents[e-1] != e:
            n = self.parents[e-1]
            self.parents[e-1] = s   # set shortcut to set representative
            e = n
        return s

    def union(self, i, j):
        """
        Unite the sets the elements i and j belong to.
        
        Arguments:
            i (int):
                First element whose set is to be united.
            j (int):
                Second element whose set is to be united.
        """

        # Determine the set representatives of i and j.
        si, sj = self.find(i), self.find(j)
        # Determine the ranks of the set representatives.
        ri, rj = self.ranks[si-1], self.ranks[sj-1]
        # Unite sets with lazy union and follow union-by-rank methodology.
        if ri > rj:
            # Merge set sj into si.
            self.parents[sj-1] = si
        elif ri == rj:
            # Merge set si into sj and update rank of sj.
            self.parents[si-1] = sj
            self.ranks[sj-1]  += 1
        else:
            # Merge set si into sj.
            self.parents[si-1] = sj
        return

# Main program.
def runMe():
    # Placeholder.
    return

if __name__ == '__main__':
    runMe()
