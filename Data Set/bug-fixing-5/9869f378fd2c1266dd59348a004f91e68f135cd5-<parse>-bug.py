def parse(self, inventory, loader, path, cache=True):
    super(InventoryModule, self).parse(inventory, loader, path)
    self._read_config_data(path=path)
    api_account = (self.get_option('api_account') or 'default')
    conf = _load_conf(self.get_option('api_config'), api_account)
    try:
        api_key = (self.get_option('api_key') or conf.get('key'))
    except Exception as e:
        raise AnsibleError('Could not find an API key. Check the configuration files.')
    hostname_preference = (self.get_option('hostname') or 'v4_main_ip')
    for server in _retrieve_servers(api_key):
        server = Vultr.normalize_result(server, SCHEMA)
        for group in ['region', 'os']:
            self.inventory.add_group(group=server[group])
            self.inventory.add_host(group=server[group], host=server['name'])
        for (attribute, value) in server.items():
            self.inventory.set_variable(server['name'], attribute, value)
        self.inventory.set_variable(server['name'], 'ansible_host', server[hostname_preference])