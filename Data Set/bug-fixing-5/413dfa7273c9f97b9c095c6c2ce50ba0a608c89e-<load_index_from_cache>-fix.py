def load_index_from_cache(self):
    ' Reads the index from the cache file sets self.index '
    with open(self.cache_path_index, 'r') as f:
        self.index = json.load(f)