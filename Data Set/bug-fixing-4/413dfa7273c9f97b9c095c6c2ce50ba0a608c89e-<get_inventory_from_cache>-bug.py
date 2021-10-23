def get_inventory_from_cache(self):
    ' Reads the inventory from the cache file and returns it as a JSON\n        object '
    cache = open(self.cache_path_cache, 'r')
    json_inventory = cache.read()
    return json_inventory