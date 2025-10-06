# -*- coding: utf-8 -*-
"""
Element class to be used as an imported module.

A method collection for Stanford Algorithms Specialization 2 written
by Oliver Kroneisen, oliver@kroneisen.net
"""

class elem:
    """
    Class for element to be used in a heap or other sorting algorithms.
    
    The attributes of this class are not protected to make handling the
    elements easier, i.e. no setter / getter methods are needed.

    Arguments:
        key (int):
            Key of element, i.e. its identifier.
        val (int or float):
            The value of the element, which will be used for comparisions.
        idx (int):
            Index of element in an enclosing list.
            A value of -1 indicates that the element is not part of
            an enclosing list.
        ref (int):
            Reference to the key of another element (optional).
    """

    def __init__(self, key, val, idx, ref=-1):
        """
        Initialize element.

        Arguments:
            key (int):
                Key of element, i.e. its identifier.
            val (int or float):
                The value of the element, which will be used for comparisions.
            idx (int):
                Index of element in an enclosing list.
                A value of -1 indicates that the element is not part of
                an enclosing list.
            ref (int):
                Reference to the key of another element (optional).
        """

        self.key = key
        self.val = val
        self.idx = idx
        self.ref = ref
        return

    def __str__(self):
        """
        Convert element content to string.

        Returns:
            text (str):
                Content of element converted to a string.
        """

        #text = str(self.key)
        #text = str(self.key) + ':' + str(self.idx)
        #text = str(self.key) + ':' + str(self.val) + ':' + str(self.idx)
        text = str(self.key) + ':' + str(self.val) + ':' + str(self.ref)
        return text

    def __repr__(self):
        """
        Represent element as a string.

        Returns:
            text (str):
                Representation of element.
        """

        return str(self)

    def __lt__(self, other):
        """
        Overload lt relation for elements.

        Returns:
            condition (bool):
                Condition of lt operation.
        """

        return (self.val < other.val)

    def __le__(self, other):
        """
        Overload le relation for elements.

        Returns:
            condition (bool):
                Condition of le operation.
        """

        return(self.val <= other.val)

    def __gt__(self, other):
        """
        Overload gt relation for elements.

        Returns:
            condition (bool):
                Condition of gt operation.
        """

        return(self.val > other.val)

    def __ge__(self, other):
        """
        Overload ge relation for elements.

        Returns:
            condition (bool):
                Condition of ge operation.
        """

        return(self.val >= other.val)

# Main program.
def runMe():
    # Placeholder.
    return

if __name__ == '__main__':
    runMe()
