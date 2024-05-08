#!/usr/bin/env python3
"""Least Frequently Used caching module.
"""
from collections import OrderedDict

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """Represents an object that allows storing and
    retrieving items from a dictionary with a LFU
    removal mechanism when the limit is reached.
    """
    def __init__(self):
        """Initializes the cache.
        """
        super().__init__()
        self.cache_data = OrderedDict()
        self.keys_freq = OrderedDict()

    def put(self, key, item):
        """Adds an item in the cache.
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            # Increment the frequency
            self.keys_freq[key] += 1
            self.cache_data[key] = item
        else:
            if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                # Find and remove the least frequently used item
                lfu_key = min(self.keys_freq, key=lambda k: self.keys_freq[k])
                self.cache_data.pop(lfu_key)
                self.keys_freq.pop(lfu_key)
                print("DISCARD:", lfu_key)
            self.cache_data[key] = item
            self.keys_freq[key] = 1
        # Move the added or accessed item to the end to handle the tie by LRU
        self.cache_data.move_to_end(key)
        self.keys_freq.move_to_end(key)

    def get(self, key):
        """Retrieves an item by key.
        """
        if key is not None and key in self.cache_data:
            # Increment the frequency
            self.keys_freq[key] += 1
            # Move the accessed item to the end to handle the tie by LRU
            self.cache_data.move_to_end(key)
            self.keys_freq.move_to_end(key)
            return self.cache_data[key]
        return None
