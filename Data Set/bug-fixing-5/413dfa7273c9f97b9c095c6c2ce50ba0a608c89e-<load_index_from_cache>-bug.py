def load_index_from_cache(self):
    ' Reads the index from the cache file sets self.index '
    cache = open(self.cache_path_index, 'r')
    json_index = cache.read()
    self.index = json.loads(json_index)