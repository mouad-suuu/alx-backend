#!/usr/bin/env python3
"""Most Recently Used caching module.
"""
from collections import OrderedDict
from base_caching import BaseCaching


class MRUCache(BaseCaching):
    """Represents an object that allows storing and
    retrieving items from a dictionary with an MRU
    removal mechanism when the limit is reached.
    """

    def __init__(self):
        """Initializes the cache.
        """
        super().__init__()
        self.cache_data = OrderedDict()

    def put(self, key, item):
        """Adds an item in the cache.
        If the cache is at capacity before adding a new item,
        the most recently used item gets discarded.
        """
        if key is None or item is None:
            return
        # If the item exists, update the order without discarding
        if key in self.cache_data:
            del self.cache_data[key]
        # Check capacity and discard the most recently used item if necessary
        elif len(self.cache_data) >= BaseCaching.MAX_ITEMS:
            mru_key, _ = self.cache_data.popitem(last=True)
            print("DISCARD:", mru_key)
        self.cache_data[key] = item
        self.cache_data.move_to_end(key, last=True)

    def get(self, key):
        """Retrieves an item by key.
        Moves the item to the end to mark it as recently used.
        """
        if key is None or key not in self.cache_data:
            return None
        self.cache_data.move_to_end(key, last=True)
        return self.cache_data[key]
