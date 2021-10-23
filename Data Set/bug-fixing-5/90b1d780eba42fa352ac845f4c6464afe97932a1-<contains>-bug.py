def contains(self, key):
    self._expire_keys()
    return (self._cache.zrank(self._keys_set, key) >= 0)