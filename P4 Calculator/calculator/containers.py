"""
TDT4113 - Computer Science, Programming Project (Spring 2021)
Project 4 Calculator
made with ❤ by mathiom

Superclass Container and subclasses Queue and Stack
"""


class Container:
    """Generic class for holding items"""

    def __init__(self):
        self._items = []

    def size(self):
        """Return number of elements"""
        return len(self._items)

    def is_empty(self):
        """Check if container is empty"""
        return self.size() == 0

    def push(self, item):
        """Add item to container"""
        self._items.append(item)

    def pop(self):
        """Pop element from container and return it"""
        raise NotImplementedError

    def peek(self):
        """Return top element without removing it"""
        raise NotImplementedError


class Queue(Container):
    """Holds items in a first-in, first-out fashion"""

    def pop(self):
        assert not self.is_empty()
        return self._items.pop(0)

    def peek(self):
        assert not self.is_empty()
        return self._items[0]


class Stack(Container):
    """Holds items in a first-in, last-out fashion"""

    def pop(self):
        assert not self.is_empty()
        return self._items.pop()

    def peek(self):
        assert not self.is_empty()
        return self._items[-1]
