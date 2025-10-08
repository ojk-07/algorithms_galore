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
    
    Attention: if the attribute parent is set, then the new node will
    also have self.parent = parent. However, the parent node will not be
    changed and therefore will not yet reflect that self is its child.

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
        self.calc_stats()
        return

    def __str__(self):
        """
        Convert bnode content to string.

        Returns:
            text (str):
                Content of bnode converted to a string.
        """

        # Set text elements.
        t_key = str(self.key)
        t_mark = str(self.mark)
        if self.parent != None:
            t_parent = str(self.parent.key)
        else:
            t_parent = 'None'
        if self.left != None:
            t_left = str(self.left.key)
        else:
            t_left = 'None'
        if self.right != None:
            t_right = str(self.right.key)
        else:
            t_right = 'None'
        t_size = str(self.size)
        t_height = str(self.height)
        t_balance = str(self.balance)
        
        # Compose output text.
        variant = 5
        if variant == 1:
            text = t_key + ':' + t_mark
        elif variant == 2:
            text = t_key
            text += ':' + t_parent
            text += ':' + t_left
            text += ':' + t_right            
        elif variant == 3:   # for statistics
            text = t_key
            text += ':' + t_parent
            text += ':' + t_left
            text += ':' + t_right
            text += ':' + t_size            
        elif variant == 4:   # for avl trees
            text = t_key
            text += ':' + t_parent
            text += ':' + t_left
            text += ':' + t_right
            text += ':' + t_height
            text += ':' + t_balance
        elif variant == 5:   # for avl trees, e.g. including non-unique keys
            text = t_key
            text += ':' + t_mark
            text += ':' + t_parent
            text += ':' + t_left
            text += ':' + t_right
            text += ':' + t_height
            text += ':' + t_balance
        else:
        	text = t_key
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

    def calc_stats(self):
        """
        Calculate statistical properties of bnodes,
        including size, height and balance.
        """

        self.size = 1
        left_height, right_height = 0, 0
        if self.left != None:
            self.size += self.left.size
            left_height = self.left.height + 1
        if self.right != None:
            self.size += self.right.size
            right_height = self.right.height + 1
        self.height = max(left_height, right_height)
        self.balance = right_height - left_height
        return

# Main program.
def runMe():
    # Placeholder.
    return

if __name__ == '__main__':
    runMe()
