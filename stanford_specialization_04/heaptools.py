# -*- coding: utf-8 -*-
"""
Heap class to be used as an imported module.

A method collection for Stanford Algorithms Specialization 2 written
by Oliver Kroneisen, oliver@kroneisen.net
"""

class heap:
    """
    Class for minimum / maximum heap.
    
    The heap elements have to provide a lt / gt relation.
    In case of flag update_idx = True, the elements also must have
    an accessible idx attribute.
    
    Arguments:
        elements (list):
            List of elements to initialize the heap.
        mintype (bool):
            Optional flag defining whether the heap shall be a minimum heap
            (= default) or a maximum heap.
        update_idx (bool):
            Optional flag defining whether the idx attribute shall be updated
            during heap operations to always reflect the position of that
            element in the heap.
    """

    def __init__(self, elements, mintype=True, update_idx=False):
        """
        Initialize heap.

        Arguments:
            elements (list):
                List of elements to initialize the heap.
            mintype (bool):
                Optional flag defining whether the heap shall be a
                minimum heap (= default) or a maximum heap.
            update_idx (bool):
                Optional flag defining whether the idx attribute shall be
                updated during heap operations to always reflect the position
                of that element in the heap.
        """

        self.e = elements
        self.mintype = mintype
        n = len(self.e)
        # Update idx attribute to match the position in the heap, if requested.
        if update_idx:
            for i in range(n):
                self.e[i].idx = i
        # Build-up heap.
        if n > 1:   # nothing to do in case of less than 2 elements
            i = n//2 - 1
            while i >= 0:
                self.reheap(i, n - 1, update_idx=update_idx)
                i -= 1
        return

    def __str__(self):
        """
        Convert heap content to string.

        Returns:
            text (str):
                Content of heap converted to a string.
        """

        return 'Heap: ' + str(self.e)

    def __repr__(self):
        """
        Represent heap as a string.

        Returns:
            text (str):
                Representation of heap.
        """

        return str(self)

    def reheap(self, i, k, update_idx=False):
        """
        Re-establish minimum / maximum heap condition for element list
        [i, ..., k] using the bottom-up logic.
        The element at position i might violate the heap condition.

        Arguments:
            i (int):
                Start index (inclusive) for applying reheap.
            k (int):
                Stop index (inclusive) for applying reheap.
            update_idx (bool):
                Optional flag defining whether the idx attribute shall be
                updated during heap operations to always reflect the position
                of that element in the heap.
        """

        # Check parameters i, k.
        if i > k:
            # Swap parameters.
            i, k = k, i
        if i < 0 or k >= len(self.e):
            msg = 'Error in reheap: Start/stop indices out of bound.'
            raise ValueError(msg)

        # Step 1.
        j = i + 1   # the virtual heap index j starts with 1
        if self.mintype:
            while 2*j < k + 1:
                if self.e[2*j - 1] < self.e[2*j]:
                    j = 2*j   # comparison
                else:
                    j = 2*j + 1
        else:
            while 2*j < k + 1:
                if self.e[2*j - 1] > self.e[2*j]:
                    j = 2*j   # comparison
                else:
                    j = 2*j + 1
        if 2*j == k + 1:
            j = k + 1   # j is associated to leaf b

        # Step 2. Sink in e[i] if necessary.
        if self.mintype:
            while self.e[i] < self.e[j - 1]:
                j //= 2   # comparison
        else:
            while self.e[i] > self.e[j - 1]:
                j //= 2   # comparison
        # j is associated to q.

        # Step 3.
        # Swap e[i] and q (denoted by r now).
        r, self.e[j - 1] = self.e[j - 1], self.e[i]
        if update_idx:
            self.e[j - 1].idx = j - 1
        j //= 2
        while j > i:   # move nodes (q and path to q) one step up
        # Swap e[j - 1] and r.
            r, self.e[j - 1] = self.e[j - 1], r
            if update_idx:
                self.e[j - 1].idx = j - 1
            j //= 2
        return

    def insert(self, element, update_idx=False):
        """
        Insert element into minimum / maximum heap.

        Arguments:
            element (elem):
                Element to be inserted.
            update_idx (bool):
                Optional flag defining whether the idx attribute shall be
                updated during heap operations to always reflect the position
                of that element in the heap.
        """

        # Set idx of inserted element, if necessary.
        n = len(self.e)
        if update_idx:
            element.idx = n
        # Add element at end of heap.
        self.e.append(element)
        k = n + 1   # virtual heap index k is associated with q
        # Identify parent p of q.
        j = k // 2   # virtual heap index j is associated with p
        if self.mintype:
            while 0 < j and self.e[k - 1] < self.e[j - 1]:
                # Swap q and p.
                self.e[j - 1], self.e[k - 1] = self.e[k - 1], self.e[j - 1]
                if update_idx:
                    self.e[j - 1].idx, self.e[k - 1].idx = j - 1, k - 1
                # Update q and p.
                k = j
                j = k // 2
        else:
            while 0 < j and self.e[k - 1] > self.e[j - 1]:
                # Swap q and p.
                self.e[j - 1], self.e[k - 1] = self.e[k - 1], self.e[j - 1]
                if update_idx:
                    self.e[j - 1].idx, self.e[k - 1].idx = j - 1, k - 1
                # Update q and p.
                k = j
                j = k // 2
        return

    def deletem(self, update_idx=False):
        """
        Return and delete minimum / maximum element from minimum /
        maximum heap.

        Arguments:
            update_idx (bool):
                Optional flag defining whether the idx attribute shall be
                updated during heap operations to always reflect the position
                of that element in the heap.

        Returns:
            element (elem):
                Element deleted from heap.
                In case the update flag is 'True', the idx attribute will be
                reset to -1 to reflect that the element is not in the heap.
        """

        # Check heap.
        n = len(self.e)
        if n == 0:   # heap is empty
            msg = 'Error in deletem: Heap is empty.'
            raise ValueError(msg)
        # Identify minimum / maximum at top of heap.
        element = self.e[0]
        # Swap element at top and last element.
        self.e[0], self.e[n - 1] = self.e[n - 1], self.e[0]
        if update_idx:
            self.e[0].idx, self.e[n - 1].idx = 0, n - 1
        # Drop last element.
        self.e.pop()
        # Reset idx of deleted element min, if necessary.
        if update_idx:
            element.idx = -1
        # Re-establish heap condition.
        if n > 2:   # nothing to do in case of less than 2 elements left
            self.reheap(0, n - 2, update_idx=update_idx)
        return element

    def delete(self, idx, update_idx=False):
        """
        Return and delete element at idx from minimum / maximum heap.

        Arguments:
            idx (int):
                Index of element to be returned and deleted.
            update_idx (bool):
                Optional flag defining whether the idx attribute shall be
                updated during heap operations to always reflect the position
                of that element in the heap.

        Returns:
            element (elem):
                Element deleted from heap.
                In case the update flag is 'True', the idx attribute will be
                reset to -1 to reflect that the element is not in the heap.
        """

        # Check parameter index.
        n = len(self.e)
        if idx < 0 or idx >= n:   # no such element in heap
            msg = 'Error in delete: No such element in heap.'
            raise ValueError(msg)
        # Identify element at idx.
        element = self.e[idx]
        # Swap element at idx and last element.
        self.e[idx], self.e[n - 1] = self.e[n - 1], self.e[idx]
        if update_idx:
            self.e[idx].idx, self.e[n - 1].idx = idx, n - 1
        # Drop last element.
        self.e.pop()
        # Reset idx of deleted element, if necessary.
        if update_idx:
            element.idx = -1
        # Raise element at idx in heap, if necessary.
        if idx < n - 1:   # nothing to do in case of deletion of last element
            j = idx + 1   # the virtual heap index j starts with 1
            if self.mintype:
                while j > 1 and self.e[j - 1] < self.e[j//2 - 1]:
                    # Swap elements.
                    i = j//2
                    self.e[j - 1], self.e[i - 1] = self.e[i - 1], self.e[j - 1]
                    if update_idx:
                        self.e[j - 1].idx, self.e[i - 1].idx = j - 1, i - 1
                    j = i
            else:
                while j > 1 and self.e[j - 1] > self.e[j//2 - 1]:
                    # Swap elements.
                    i = j//2
                    self.e[j - 1], self.e[i - 1] = self.e[i - 1], self.e[j - 1]
                    if update_idx:
                        self.e[j - 1].idx, self.e[i - 1].idx = j - 1, i - 1
                    j = i
            # Re-establish heap condition.
            if n - j > 1:   # nothing to do in case of less than 2 elements
                self.reheap(j - 1, n - 2, update_idx=update_idx)
        return element

# Main program.
def runMe():
    # Placeholder.
    return

if __name__ == '__main__':
    runMe()
