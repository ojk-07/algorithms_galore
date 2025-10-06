# -*- coding: utf-8 -*-
"""
BNodes class to be used as an imported module.

A method collection for Stanford Algorithms Specialization 2 written
by Oliver Kroneisen, oliver@kroneisen.net
"""

class bnode:
    """
    Class for nodes to be used in binary search trees.
    
    The attributes of this class are not protected to make handling the
    elements easier, i.e. no setter / getter methods are needed.

    The nodes have the internal attribute size which reflects the size
    of the subtree for this node, when part of a binary tree.
    This attribute is calculated automatically when the configuration
    the node is in has changed.

    Arguments:
        key (int):
            Key of node, i.e. its identifier and criterion for searching.
        mark (bool, int or float):
            A mark on the node for different purposes.
        parent (bnode):
            Optional reference to the parent node, with value 'None'
            in case no parent exists.
        left (bnode):
            Optional reference to the left child node, with value 'None'
            in case no left child exists.
        right (bnode):
            Optional reference to the right child node, with value 'None'
            in case no right child exists.
    """

    def __init__(self, key, mark=None, parent=None, left=None, right=None):
        """
        Initialize bnode.

        Arguments:
            key (int):
                Key of node, i.e. its identifier and criterion for searching.
            mark (bool, int or float):
                Optional mark on the node for different purposes.
            parent (bnode):
                Optional reference to the parent node, with value 'None'
                in case no parent exists.
            left (bnode):
                Optional reference to the left child node, with value 'None'
                in case no left child exists.
            right (bnode):
                Optional reference to the right child node, with value 'None'
                in case no right child exists.
        """

        self.key    = key
        self.mark   = mark
        self.parent = parent
        self.left   = left
        self.right  = right
        self.size   = 1
        if self.left != None:
            self.size += self.left.size
        if self.right != None:
            self.size += self.right.size
        return

    def __str__(self):
        """
        Convert bnode content to string.

        Returns:
            text (str):
                Content of bnode converted to a string.
        """

        #text = str(self.key)
        #text = str(self.key) + ':' + str(self.mark)
        #text = str(self.key) + ':' + str(self.size)
        text = str(self.key)
        if self.parent != None:
            text += ':' + str(self.parent.key)
        else:
            text += ':None'
        if self.left != None:
            text += ':' + str(self.left.key)
        else:
            text += ':None'
        if self.right != None:
            text += ':' + str(self.right.key)
        else:
            text += ':None'
        return text

    def __repr__(self):
        """
        Represent bnode as a string.

        Returns:
            text (str):
                Representation of bnode.
        """

        return str(self)

    def __lt__(self, other):
        """
        Overload lt relation for bnodes.

        Returns:
            condition (bool):
                Condition of lt operation.
        """

        return (self.key < other.key)

    def __le__(self, other):
        """
        Overload le relation for bnodes.

        Returns:
            condition (bool):
                Condition of le operation.
        """

        return(self.key <= other.key)

    def __gt__(self, other):
        """
        Overload gt relation for bnodes.

        Returns:
            condition (bool):
                Condition of gt operation.
        """

        return(self.key > other.key)

    def __ge__(self, other):
        """
        Overload ge relation for bnodes.

        Returns:
            condition (bool):
                Condition of ge operation.
        """

        return(self.key >= other.key)

# Main program.
def runMe():
    # Placeholder.
    return

if __name__ == '__main__':
    runMe()
