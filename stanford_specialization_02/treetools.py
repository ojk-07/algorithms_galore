# -*- coding: utf-8 -*-
"""
Tree class to be used as an imported module.

A method collection for Stanford Algorithms Specialization 2 written
by Oliver Kroneisen, oliver@kroneisen.net
"""

class btree:
    """
    Class for binary tree, using nodes of class bnode.

    In case of non-unique keys, nodes with keys equal to the key of a pivote
    node are inserted into the left subtree.
 
    Arguments:
        tree_type (str):
            Optional type of tree, e.g. 'std', 'avl'.
        root (bnode):
            Optional reference to the root node, with value 'None'
            in case no root exists.
    """

    def __init__(self, tree_type='std', root=None):
        """
        Initialize btree.

        Arguments:
            tree_type (str):
                Type of tree, e.g. 'std', 'avl'.
            root (bnode):
                Optional reference to the root node, with value 'None'
                in case no root exists.
        """

        self.type = tree_type
        self.root = root
        return

    def __str__(self):
        """
        Convert btree content to string.

        Returns:
            text (str):
                Content of btree converted to a string.
        """
        text = 'Tree of type: ' + str(self.type) + ', root: '
        if self.root != None:
            text += str(self.root.key)
        else:
            text += 'None'
        return text

    def __repr__(self):
        """
        Represent btree as a string.

        Returns:
            text (str):
                Representation of btree.
        """

        return str(self)

    def inorder(self, start=None):
        """
        Traverse subtree in-order, beginning at start, and create its string
        representation.

        It is assumed that start is truly part of btree self, otherwise
        the returned string will represent the subtree of start in the btree
        that start is included in.

        Arguments:
            start (bnode):
                Optional node defining in which subtree to start the traversal.
                In case of 'None', the traversal starts at the root of btree.

        Returns:
            text (str):
                String representation of btree in-order.
        """

        # Initialize data.
        text = ''
        if start == None:
            start = self.root   # root as default value
        if start == None:
            return text   # empty tree, no root assigned

        # Recursive in-order traversal.
        if start.left != None:
            text += self.inorder(start.left)
        text += str(start) + ' '
        if start.right != None:
            text += self.inorder(start.right)
        return text

    def search(self, key, start=None):
        """
        Search for node with key in btree.

        It is assumed that start is truly part of btree self, otherwise
        in case of a successful search, node will be from the btree
        that start is included in.

        Arguments:
            key (int):
                Key of node to be returned.
            start (bnode):
                Optional node defining in which subtree to start the search.
                In case of 'None', the search starts at the root of btree.

        Returns:
            found (bool):
                Flag whether key was found.
            node (bnode):
                For a successful search, node found in btree.
                Otherwise the node where the unsuccesful search ended,
                or 'None' in case of an empty tree.
        """

        # Initialize data.
        if start == None:
            start = self.root   # root as default value
        if start == None:
            return False, None   # empty tree, no root assigned

        # Recursive search.
        if key == start.key:
            return True, start
        elif key <= start.key:
            if start.left == None:
                return False, start
            else:
                return self.search(key, start=start.left)
        else:
            if start.right == None:
                return False, start
            else:
                return self.search(key, start=start.right)

    def findmin(self, start=None):
        """
        Search for a minimum node in btree.

        It is assumed that start is truly part of btree self, otherwise
        in case of a successful search, the minimum node will be from the btree
        that start is included in.

        Arguments:
            start (bnode):
                Optional node defining in which subtree to start the search.
                In case of 'None', the search starts at the root of btree.

        Returns:
            node (bnode):
                For a successful search, a minimum node in btree.
                'None' in case of an empty tree.
        """

        # Initialize data.
        if start == None:
            start = self.root   # root as default value
        if start == None:
            return None   # empty tree, no root assigned

        # Recursive search.
        if start.left == None:
            return start
        else:
            return self.findmin(start=start.left)

    def findmax(self, start=None):
        """
        Search for a maximum node in btree.

        It is assumed that start is truly part of btree self, otherwise
        in case of a successful search, the maximum node will be from the btree
        that start is included in.

        Arguments:
            start (bnode):
                Optional node defining in which subtree to start the search.
                In case of 'None', the search starts at the root of btree.

        Returns:
            node (bnode):
                For a successful search, a maximum node in btree.
                'None' in case of an empty tree.
        """

        # Initialize data.
        if start == None:
            start = self.root   # root as default value
        if start == None:
            return None   # empty tree, no root assigned

        # Recursive search.
        if start.right == None:
            return start
        else:
            return self.findmax(start=start.right)

    def pred(self, node):
        """
        Search for the predecessor of node in btree.

        It is assumed that node is truly part of btree self, otherwise
        in case of a successful search, the predecessor will be from the btree
        that node is included in.

        Arguments:
            node (bnode):
                Node for which a predecessor is to be found.

        Returns:
            predecessor (bnode):
                For a successful search, the predecessor of node in btree,
                otherwise 'None'.
        """

        # Check left subtree of node.
        if node.left != None:
            q = node.left
            # Search rightmost node in left subtree.
            while q.right != None:
                q = q.right
            return q

        # Check parents of node.
        q = node
        while q >= node and q.parent != None:
            q = q.parent
        if q < node:
            return q
        else:
            return None   # no predecessor found

    def succ(self, node):
        """
        Search for the successor of node in btree.

        It is assumed that node is truly part of btree self, otherwise
        in case of a successful search, the sucessor will be from the btree
        that node is included in.

        Arguments:
            node (bnode):
                Node for which a successor is to be found.

        Returns:
            successor (bnode):
                For a successful search, the successor of node in btree,
                otherwise 'None'.
        """

        # Check right subtree of node.
        if node.right != None:
            q = node.right
            # Search leftmost node in right subtree.
            while q.left != None:
                q = q.left
            return q

        # Check parents of node.
        q = node
        while q <= node and q.parent != None:
            q = q.parent
        if q > node:
            return q
        else:
            return None   # no predecessor found

    def rotate(self, node, right=True):
        """
        Rotate btree right or left at node.

        Arguments:
            node (bnode):
                Node where to perform the rotation of btree.
            right (bool):
                Optional flag indicating whether to rotate right or left.

        Returns:
            rotated (bool):
                Flag whether the rotation could be executed.
        """

        # Store information about the parent of node.
        parent = node.parent
        # Perform rotation.
        if right:   # rotate right
            l = node.left
            if l == None:   # rotation not possible
                return False
            # Set reference variables.
            lr = l.right
            # Update references.
            l.parent = parent
            l.right = node
            node.parent = l
            node.left = lr
            if lr != None:
                lr.parent = node
            if parent == None:
                self.root = l
            elif parent.left == node:
                parent.left = l
            else:
                parent.right = l
            # Update stats of node and l.
            node.calc_stats()
            l.calc_stats()
        else:   # rotate left
            r = node.right
            if r == None:   # rotation not possible
                return False
            # Set reference variables.
            rl = r.left
            # Update references.
            r.parent = parent
            r.left = node
            node.parent = r
            node.right = rl
            if rl != None:
                rl.parent = node
            if parent == None:
                self.root = r
            elif parent.left == node:
                parent.left = r
            else:
                parent.right = r
            # Update stats for node and r.
            node.calc_stats()
            r.calc_stats()
        return True

    def balance_avl(self, node):
        """
        Balance btree at node according to avl rules.

        Arguments:
            node (bnode):
                Node where to balance btree.

        Returns:
            balanced (bool):
                Flag whether the balancing could be executed.
        """

        # Initialize variables.
        balanced = False
        if self.type == 'avl' and abs(node.balance) >= 2:
            # Node out of balance.
            if node.balance >= 2:   # case a
                if node.right.balance >= 0:   # case a.1
                    # Rotate left in node.
                    rotated = self.rotate(node, right=False)
                    if rotated:
                        balanced = True
                else:   # case a.2
                    # Double rotation needed.
                    # Rotate right in node.right.
                    rotated = self.rotate(node.right, right=True)
                    # Rotate left in node.
                    if rotated:
                        rotated = self.rotate(node, right=False)
                        if rotated:
                            balanced = True
            else:   # case b
                if node.left.balance <= 0:   # case b.1
                    # Rotate right in node.
                    rotated = self.rotate(node, right=True)
                    if rotated:
                        balanced = True
                else:   # case b.2
                    # Double rotation needed.
                    # Rotate left in node.left.
                    rotated = self.rotate(node.left, right=False)
                    # Rotate right in node.
                    if rotated:
                        rotated = self.rotate(node, right=True)
                        if rotated:
                            balanced = True
        return balanced

    def insert(self, node, unique=True):
        """
        Insert node into btree.
        
        In case of non-unique keys, in this implementation, the new node
        will still be added as a leaf.
        Once AVL balancing is activated, duplicate keys are likely to get
        spread around the tree anyway.

        Arguments:
            node (bnode):
                Node to be inserted into btree.
            unique (bool):
                Optional flag indicating whether only unique keys may
                be inserted.

        Returns:
            inserted (bool):
                Flag whether the node could be inserted.
        """

        # Handle special case of empty tree.
        if self.root == None:
            self.root = node
            node.parent = None
            return True

        # Search for key of node to be inserted.
        found, anchor = self.search(node.key)
        if found:
            if unique:
                # Return since it is not allowed to insert this node.
                return False
            else:
                # Keep searching until the node can be inserted as a leaf
                # as a left child of anchor.
                while anchor.left != None:
                    found, anchor = self.search(node.key, start=anchor.left)

        # Insert node as child of anchor.
        if node <= anchor:
            # Insert node as left child of anchor.
            anchor.left = node
        else:
            # Insert node as right child of anchor.
            anchor.right = node

        # Store anchor as parent for node.
        node.parent = anchor
        # Update stats and rebalance tree if necessary.
        q = node
        while q != None:
            q.calc_stats()
            # Rebalance tree if necessary.
            if self.type == 'avl' and abs(q.balance) >= 2:
                # Node q out of balance.
                self.balance_avl(q)
            q = q.parent
        return True

    def delete(self, node):
        """
        Delete node from btree.

        It is assumed that node is truly part of btree self, otherwise
        in case of a successful deletion, it will be deleted from the btree
        that node was included in.

        Arguments:
            node (bnode):
                Node to be deleted from btree.

        Returns:
            deleted (bool):
                Flag whether the node could be deleted.
        """

        # Distinguish the different cases.
        if node.left == None and node.right == None:
            # Case 1. Directly delete node from btree.
            anchor = node.parent
            if node.parent != None:
                # Remove node as child of its parent.
                if node.parent.left == node:
                    node.parent.left = None
                else:
                    node.parent.right = None
            else:
                # Remove the root node of btree (in case btree points to node).
                if self.root == node:
                    self.root = None
                else:
                    return False
        elif node.left == None:
            # Case 2a. Replace node by right child.
            anchor = node.parent
            if node.parent != None:
                # Replace node as child of its parent.
                if node.parent.left == node:
                    node.parent.left = node.right
                else:
                    node.parent.right = node.right
            else:
                # Replace the root node.
                self.root = node.right
            node.right.parent = node.parent
        elif node.right == None:
            # Case 2b. Replace node by left child.
            anchor = node.parent
            if node.parent != None:
                # Replace node as child of its parent.
                if node.parent.left == node:
                    node.parent.left = node.left
                else:
                    node.parent.right = node.left
            else:
                # Replace the root node.
                self.root = node.left
            node.left.parent = node.parent
        else:
            # Case 3. Most complex case for nodes with 2 children.
            # Find predecessor of node.
            # Since node has a left child, the predecessor must exist and
            # is located in the left subtree of node.
            # The predecessor therefore also has a parent.
            # Like any predecessor, it can only have a left child.
            pred = self.pred(node)
            if pred.parent == node:
                # Case 3a. This configuration needs a special treatment.
                anchor = pred
                # Replace node by pred.
                if node.parent != None:
                    # Replace node as child of its parent.
                    if node.parent.left == node:
                        node.parent.left = pred
                    else:
                        node.parent.right = pred
                else:
                    # Replace the root node.
                    self.root = pred
                # Update pred.
                pred.parent = node.parent
                pred.right = node.right
                # Update the other child of node.
                node.right.parent = pred
            else:
                # Case 3b. The parent node of pred is not affected by changes.
                anchor = pred.parent
                # Replace pred by the left child of pred.
                # Consider also the case that there is no left child of pred.
                if pred.parent.left == pred:
                    pred.parent.left = pred.left
                else:
                    pred.parent.right = pred.left
                if pred.left != None:
                    pred.left.parent = pred.parent
                # Replace node by pred.
                if node.parent != None:
                    # Replace node as child of its parent.
                    if node.parent.left == node:
                        node.parent.left = pred
                    else:
                        node.parent.right = pred
                else:
                    # Replace the root node.
                    self.root = pred
                # Update pred.
                pred.parent = node.parent
                pred.left, pred.right = node.left, node.right
                # Update the children of node.
                node.left.parent, node.right.parent = pred, pred

        # Common adjustments in case of successful deletion.
        # Update stats for anchor and its parents.
        q = anchor
        while q != None:
            q.calc_stats()
            # Rebalance tree if necessary.
            if self.type == 'avl' and abs(q.balance) >= 2:
                # Node q out of balance.
                self.balance_avl(q)
            q = q.parent
        return True

    def rank(self, node):
        """
        Provide the rank of node in btree, i.e. which i-th order statistic
        node represents.

        It is assumed that node is truly part of btree self, otherwise
        the result will be from the btree that node is included in.

        Arguments:
            node (bnode):
                Node for which the rank shall be returned.

        Returns:
            i (int):
                Rank of node.
        """

        # Calculate elements to the left from left child.
        if node.left != None:
            size_left = node.left.size
        else:
            size_left = 0

        # Calculate elements to the left from left parent.
        if node.parent != None and node.parent.right == node:
            size_left += node.parent.size - node.size
        return size_left + 1

    def select(self, i, start=None):
        """
        Search for i-th order statistic in btree.

        It is assumed that start is truly part of btree self, otherwise
        in case of a successful search, node will be from the btree
        that start is included in.

        Arguments:
            i (int):
                Number i of i-th order statistic to be returned.
            start (bnode):
                Optional node defining in which subtree to start the search.
                In case of 'None', the search starts at the root of btree.

        Returns:
            found (bool):
                Flag whether the i-th order statistic was found.
            node (bnode):
                For a successful search, node of i-th order statistic in btree,
                otherwise 'None'.
        """

        # Initialize data.
        if start == None:
            start = self.root   # root as default value
        if start == None:
            return False, None   # empty tree, no root assigned

        # Check validity of parameter i.
        if i < 1:
            return False, None   # i must be a positive integer
        if i > start.size:
            return False, None   # there is no i-th order statistic in subtree

        # Recursive search.
        if start.left != None:
            size_left = start.left.size
        else:
            size_left = 0
        if i == size_left + 1:
            return True, start
        elif i <= size_left:
            return self.select(i, start=start.left)
        else:
            return self.select(i - size_left - 1, start=start.right)

# Main program.
def runMe():
    # Placeholder.
    return

if __name__ == '__main__':
    runMe()
