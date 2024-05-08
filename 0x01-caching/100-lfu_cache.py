#!/usr/bin/env python3
"""Least Frequently Used (LFU) caching module with LRU tie-breaker.
"""
from collections import defaultdict, OrderedDict
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """Represents an object that stores and retrieves items
    using an LFU removal mechanism with LRU tie-breaker
    when the cache limit is reached.
    """

    def __init__(self):
        """Initializes the cache.
        """
        super().__init__()
        self.cache_data = {}
        self.frequency = defaultdict(OrderedDict)
        self.min_freq = 0

    def put(self, key, item):
        """Adds an item to the cache.
        Removes the LFU item with LRU consideration if limit is exceeded.
        """
        if key is None or item is None:
            return
        if key in self.cache_data:
            # Increment the frequency of the key
            _, freq = self.cache_data[key]
            self.cache_data[key] = (item, freq + 1)
            del self.frequency[freq][key]
            self.frequency[freq + 1][key] = item
            if not self.frequency[freq]:
                if freq == self.min_freq:
                    self.min_freq += 1
            freq += 1
        else:
            self.cache_data[key] = (item, 1)
            self.frequency[1][key] = item
            self.min_freq = 1

        if len(self.cache_data) > BaseCaching.MAX_ITEMS:
            oldest_key, _ = next(iter(self.frequency[self.min_freq].items()))
            del self.frequency[self.min_freq][oldest_key]
            del self.cache_data[oldest_key]
            print("DISCARD:", oldest_key)
            if not self.frequency[self.min_freq]:
                self.min_freq += 1

    def get(self, key):
        """Retrieves an item by key.
        Updates the item's frequency and recency of use.
        Returns None if the key is not found or if key is None.
        """
        if key is None or key not in self.cache_data:
            return None
        item, freq = self.cache_data[key]
        # Update the item's frequency
        del self.frequency[freq][key]
        self.frequency[freq + 1][key] = item
        self.cache_data[key] = (item, freq + 1)
        if not self.frequency[freq]:
            if freq == self.min_freq:
                self.min_freq += 1
        return item
