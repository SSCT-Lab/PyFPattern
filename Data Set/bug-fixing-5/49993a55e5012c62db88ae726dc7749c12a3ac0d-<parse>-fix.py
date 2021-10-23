def parse(self, inventory, loader, path, cache=True):
    '\n        Parses the inventory file\n        '
    if (not HAS_REQUESTS):
        raise AnsibleParserError('Please install "requests" Python module as this is required for VMware Guest dynamic inventory plugin.')
    elif (not HAS_PYVMOMI):
        raise AnsibleParserError('Please install "PyVmomi" Python module as this is required for VMware Guest dynamic inventory plugin.')
    if HAS_REQUESTS:
        required_version = (2, 3)
        requests_version = requests.__version__.split('.')[:2]
        try:
            requests_major_minor = tuple(map(int, requests_version))
        except ValueError:
            raise AnsibleParserError("Failed to parse 'requests' library version.")
        if (requests_major_minor < required_version):
            raise AnsibleParserError(("'requests' library version should be >= %s, found: %s." % ('.'.join([str(w) for w in required_version]), requests.__version__)))
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