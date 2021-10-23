def get_inventory_from_cache(self):
    ' Reads the inventory from the cache file and returns it as a JSON\n        object '
    with open(self.cache_path_cache, 'r') as f:
        json_inventory = f.read()
        return json_inventory