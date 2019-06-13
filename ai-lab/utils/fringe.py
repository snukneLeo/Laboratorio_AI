"""
Data structures representing the fringe for search methods
"""

import heapq
from collections import deque
from abc import ABC, abstractmethod


class FringeNode:
    """
    Fringe state representation
    """
    def __init__(self, state, parent=None, pathcost=0, value=0):
        """
        Creates a representation of a node in the fringe

        Args:
            state: the state embedded in the node
            parent: parent node (optional)
            pathcost: path cost from the root node to this one (optional)
            value: value of a node (optional)
        """
        self.state = state
        self.pathcost = pathcost
        self.value = value
        self.parent = parent
        self.removed = False

    def __lt__(self, other):
        """
        Compare function between nodes - 'lower than'

        Args:
            other: object to compare to

        Returns:
            True if lower, False otherwise
        """
        return self.value < other.value

    def __hash__(self):
        """
        Hash value of a node: the unique integer identifier of its state

        Returns:
             unique integer identifier of the embedded state
        """
        return self.state


class Fringe(ABC):
    """
    General fringe abstract class
    """
    def __init__(self, fringe=None):
        """
        Initializes the fringe

        Args:
            fringe: initial fringe
        """
        self.fringe = fringe
        self.frdict = {}  # For quick access to fringe content
        self.frlen = 0

    def is_empty(self):
        """
        Checks if the fringe is empty

        Returns:
            True if empty, False otherwise
        """
        return self.frlen == 0

    @abstractmethod
    def add(self, n):
        """
        Adds a new state to the fringe

        Args:
            n: node to be added to the fringe
        """
        raise NotImplementedError

    def replace(self, n):
        """
        Replaces the node with state ``n.state`` with the new node ``n``

        Args:
            n: node with the state to replace
        """
        self.frdict[n.state].removed = True
        self.frdict[n.state] = n
        self.frlen -= 1
        self.add(n)

    @abstractmethod
    def remove(self):
        """
        Returns (and removes) the first node of the fringe (depending on how the fringe stores the nodes)

        Returns:
            removed node
        """
        raise NotImplementedError

    def __len__(self):
        """
        Returns the current length of the fringe

        Returns:
            current length of the fringe
        """
        return self.frlen

    def __contains__(self, item):
        """
        Checks if the fringe contais the state item

        Args:
            item: state item to search within the fringe

        Returns:
            True if contained, False otherwise
        """
        return item in self.frdict

    def __getitem__(self, i):
        """
        Indexing function: returns the node embedding a specified state (if in the fringe)

        Args:
            i: index (state)

        Returns:
            node
        """
        return self.frdict[i]


class QueueFringe(Fringe):
    """
    Queue implementation of the fringe (FIFO)
    """
    def __init__(self):
        super().__init__(deque())

    def add(self, n):
        self.frdict[n.state] = n
        self.fringe.append(n)
        self.frlen += 1

    def remove(self):
        while True:
            n = self.fringe.popleft()
            if not n.removed:
                if n.state in self.frdict:
                    del self.frdict[n.state]
                self.frlen -= 1
                return n


class StackFringe(Fringe):
    """
    Stack implementation of the fringe (LIFO)
    """
    def __init__(self):
        super().__init__([])

    def add(self, n):
        self.frdict[n.state] = n
        self.fringe.append(n)
        self.frlen += 1

    def remove(self):
        while True:
            n = self.fringe.pop()
            if not n.removed:
                if n.state in self.frdict:
                    del self.frdict[n.state]
                self.frlen -= 1
                return n


class PriorityFringe(Fringe):
    """
    Ordered implementation of the fringe
    """
    def __init__(self):
        super().__init__([])

    def add(self, n):
        heapq.heappush(self.fringe, n)
        self.frdict[n.state] = n
        self.frlen += 1

    def remove(self):
        while True:
            n = heapq.heappop(self.fringe)
            if not n.removed:
                if n.state in self.frdict:
                    del self.frdict[n.state]
                self.frlen -= 1
                return n
