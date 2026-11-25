# -*- coding: utf-8 -*-
"""
Element class to be used as an imported module.

A method collection for Stanford Algorithms Specialization 3 written
by Oliver Kroneisen, oliver@kroneisen.net
"""

class elem:
    """
    Class for element to be used in a heap or other sorting algorithms.
    
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
            Key of element, i.e. its identifier.
        val (int or float):
            The value of the element, which will be used for comparisions.
        idx (int):
            Index of element in an enclosing list.
            A value of -1 indicates that the element is not part of
            an enclosing list.
        parent (elem):
            Optional reference to the parent node, with value 'None'
            in case no parent exists.
        left (elem):
            Optional reference to the left child node, with value 'None'
            in case no left child exists.
        right (elem):
            Optional reference to the right child node, with value 'None'
            in case no right child exists.
        encoding (str):
            Encoding string for the element (optional).
    """

    def __init__(self, key, val, idx=-1, parent=None, left=None, right=None,
                 encoding=''):
        """
        Initialize element.

        Arguments:
            key (int):
                Key of element, i.e. its identifier.
            val (int or float):
                The value of the element, which will be used for comparisions.
            idx (int):
                Index of element in an enclosing list (optional).
                A value of -1 indicates that the element is not part of
                an enclosing list.
            parent (elem):
                Optional reference to the parent node, with value 'None'
                in case no parent exists.
            left (elem):
                Optional reference to the left child node, with value 'None'
                in case no left child exists.
            right (elem):
                Optional reference to the right child node, with value 'None'
                in case no right child exists.
            encoding (str):
                Encoding string for the element (optional).
        """

        self.key = key
        self.val = val
        self.idx = idx
        self.parent = parent
        self.left   = left
        self.right  = right
        self.encoding = encoding
        self.calc_stats()
        return

    def __str__(self):
        """
        Convert element content to string.

        Returns:
            text (str):
                Content of element converted to a string.
        """

        # Set text elements.
        t_key = str(self.key)
        t_val = str(self.val)
        t_idx = str(self.idx)
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
        variant = 3
        if variant == 1:
            text = t_key + ':' + t_idx
        elif variant == 2:
            text = t_key
            text += ':' + t_val
            text += ':' + t_idx
        elif variant == 3:
            text = t_key
            text += ':' + t_val
            text += ':' + self.encoding
        elif variant == 4:   # tree structure
            text = t_key
            text += ':' + t_val
            text += ':' + t_parent
            text += ':' + t_left
            text += ':' + t_right
            text += ':' + t_size
            text += ':' + t_height
            text += ':' + t_balance
        else:
        	text = t_key
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
