def parse(self, inventory, loader, path, cache=True):
    super(InventoryModule, self).parse(inventory, loader, path)
    cache_key = self.get_cache_key(path)
    config_data = self._read_config_data(path)
    self._consume_options(config_data)
    source_data = None
    if cache:
        cache = self.get_option('cache')
    update_cache = False
    if cache:
        try:
            source_data = self.cache.get(cache_key)
        except KeyError:
            update_cache = True
    if (not source_data):
        b_pwfile = to_bytes(self.get_option('settings_password_file'), errors='surrogate_or_strict')
        running = self.get_option('running_only')
        cmd = [self.VBOX, b'list', b'-l']
        if running:
            cmd.append(b'runningvms')
        else:
            cmd.append(b'vms')
        if (b_pwfile and os.path.exists(b_pwfile)):
            cmd.append(b'--settingspwfile')
            cmd.append(b_pwfile)
        try:
            p = Popen(cmd, stdout=PIPE)
        except Exception as e:
            raise AnsibleParserError(to_native(e))
        source_data = p.stdout.read().splitlines()
    using_current_cache = (cache and (not update_cache))
    cacheable_results = self._populate_from_source(source_data, using_current_cache)
    if update_cache:
        self.cache.set(cache_key, cacheable_results)