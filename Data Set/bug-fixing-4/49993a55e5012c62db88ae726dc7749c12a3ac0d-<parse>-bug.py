def parse(self, inventory, loader, path, cache=True):
    '\n        Parses the inventory file\n        '
    super(InventoryModule, self).parse(inventory, loader, path, cache=cache)
    cache_key = self.get_cache_key(path)
    config_data = self._read_config_data(path)
    source_data = None
    if cache:
        cache = self.get_option('cache')
    update_cache = False
    if cache:
        try:
            source_data = self.cache.get(cache_key)
        except KeyError:
            update_cache = True
    self._consume_options(config_data)
    self._set_credentials()
    self.content = self._login()
    if self.with_tags:
        self.rest_content = self._login_vapi()
    using_current_cache = (cache and (not update_cache))
    cacheable_results = self._populate_from_source(source_data, using_current_cache)
    if update_cache:
        self.cache.set(cache_key, cacheable_results)