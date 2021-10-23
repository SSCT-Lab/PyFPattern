def parse(self, inventory, loader, path, cache=True):
    super(InventoryModule, self).parse(inventory, loader, path)
    config_data = self._read_config_data(path)
    self._set_credentials()
    (regions, filters, hostnames, strict_permissions) = self._get_query_options(config_data)
    if cache:
        cache = self._options.get('cache')
        cache_key = self.get_cache_key(path)
    else:
        cache_key = None
    formatted_inventory = {
        
    }
    cache_needs_update = False
    if cache:
        try:
            results = self.cache.get(cache_key)
        except KeyError:
            cache_needs_update = True
        else:
            self._populate_from_source(results)
    if ((not cache) or cache_needs_update):
        results = self._query(regions, filters, strict_permissions)
        self._populate(results, hostnames)
        formatted_inventory = self._format_inventory(results, hostnames)
    if cache_needs_update:
        self.cache.set(cache_key, formatted_inventory)