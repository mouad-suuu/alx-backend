#!/usr/bin/env python3
"""Last-In First-Out caching module.
"""
from base_caching import BaseCaching


class LIFOCache(BaseCaching):
    """Represents an object that allows storing and
    retrieving items from a dictionary with a LIFO
    removal mechanism when the limit is reached.
    """

    def __init__(self):
        """Initializes the cache.
        """
        super().__init__()
        self.last_key = None

    def put(self, key, item):
        """Adds an item in the cache.
        If the cache exceeds MAX_ITEMS, the last item
        added will be removed (LIFO order).
        """
        if key is None or item is None:
            return
        self.cache_data[key] = item
        if self.last_key is not None and len(self.cache_data) > BaseCaching.MAX_ITEMS:
            discarded = self.last_key
            del self.cache_data[discarded]
            print("DISCARD:", discarded)
        self.last_key = key

    def get(self, key):
        """Retrieves an item by key.
        Returns None if the key is not found or if key is None.
        """
        return self.cache_data.get(key, None)
