def parse(self, inventory, loader, path, cache=True):
    super(InventoryModule, self).parse(inventory, loader, path)
    self._read_config_data(path=path)
    conf = _load_conf(self.get_option('api_config'), self.get_option('api_account'))
    try:
        api_key = (self.get_option('api_key') or conf.get('key'))
    except Exception:
        raise AnsibleError('Could not find an API key. Check inventory file and Vultr configuration files.')
    hostname_preference = self.get_option('hostname')
    for server in _retrieve_servers(api_key):
        server = Vultr.normalize_result(server, SCHEMA)
        for group in ['region', 'os']:
            self.inventory.add_group(group=server[group])
            self.inventory.add_host(group=server[group], host=server['name'])
        for (attribute, value) in server.items():
            self.inventory.set_variable(server['name'], attribute, value)
        if (hostname_preference != 'name'):
            self.inventory.set_variable(server['name'], 'ansible_host', server[hostname_preference])