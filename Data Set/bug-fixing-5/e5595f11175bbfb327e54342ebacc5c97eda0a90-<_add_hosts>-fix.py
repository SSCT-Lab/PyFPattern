def _add_hosts(self, items, config_data, format_items=True, project_disks=None):
    '\n            :param items: A list of hosts\n            :param config_data: configuration data\n            :param format_items: format items or not\n        '
    if (not items):
        return
    hostname_ordering = ['public_ip', 'private_ip', 'name']
    if self.get_option('hostnames'):
        hostname_ordering = self.get_option('hostnames')
    for host_json in items:
        host = GcpInstance(host_json, hostname_ordering, project_disks, format_items)
        self._populate_host(host)
        hostname = host.hostname()
        self._set_composite_vars(self.get_option('compose'), host.to_json(), hostname)
        self._add_host_to_composed_groups(self.get_option('groups'), host.to_json(), hostname)
        self._add_host_to_keyed_groups(self.get_option('keyed_groups'), host.to_json(), hostname)