#!/usr/bin/env python3
"""Most Recently Used (MRU) caching module.
"""
from collections import OrderedDict
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """Represents an object that stores and retrieves items
    using an MRU removal mechanism when the cache limit is reached.
    """

    def __init__(self):
        """Initializes the cache.
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Adds an item to the cache.
        Removes the most recently used item if the limit is exceeded.
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item
        self.cache_data.move_to_end(key)
        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discarded = next(reversed(self.cache_data))
            del self.cache_data[discarded]
            print("DISCARD:", discarded)

    def get(self, key):
        """Retrieves an item by key.
        Moves the item to the end to mark it as recently used.
        Returns None if the key is not found or if key is None.
        """
        if key is None or key not in self.cache_data:
            return None
        self.cache_data.move_to_end(key)
        return self.cache_data[key]
