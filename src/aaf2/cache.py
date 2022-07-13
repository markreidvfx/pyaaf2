from __future__ import (
    unicode_literals,
    absolute_import,
    print_function,
    division,
    )

class LRUNode(object):
    def __init__(self):
        self.next = None
        self.prev = None
        self.value = None

        self.empty = True
        self.key = None

sentinel = object()

class LRUCacheDict(object):

    def __init__(self, size=512):
        self.data = {}

        # create circlular double link list
        self.head = LRUNode()
        self.head.next = self.head
        self.head.prev = self.head

        for i in range(size):
            node = LRUNode()
            node.next = self.head
            node.prev = self.head.prev

            self.head.prev.next = node
            self.head.prev = node

    def make_first(self, node):
        # remove
        node.prev.next = node.next
        node.next.prev = node.prev

        # hook up new prev and next
        node.prev = self.head.prev
        node.next = self.head.prev.next

        # update neighbors to point to new node
        node.next.prev = node
        node.prev.next = node

    def __contains__(self, key):
        return key in self.data

    def __setitem__(self, key, value):

        if key in self.data:
            node = self.data[key]
            node.value = value
            self.make_first(node)
            self.head = node
            return

        # pick the last node
        node = self.head.prev

        if not node.empty:
            del self.data[node.key]

        node.empty = False
        node.key = key
        node.value = value

        self.head = node
        self.data[key] = node

    def __getitem__(self, key):
        value = self.get(key, sentinel)
        if value is sentinel:
            raise KeyError()
        return value

    def get(self, key, default=None):
        node = self.data.get(key, sentinel)
        if node is sentinel:
            return default

        self.make_first(node)
        self.head = node

        return node.value

    def __delitem__(self, key):

        node = self.data.pop(key)
        node.empty = True

        node.key = None
        node.value = None

        self.make_first(node)
        self.head = node.next
