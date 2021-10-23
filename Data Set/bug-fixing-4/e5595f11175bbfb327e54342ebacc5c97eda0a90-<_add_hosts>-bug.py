def _add_hosts(self, items, config_data, format_items=True, project_disks=None):
    '\n            :param items: A list of hosts\n            :param config_data: configuration data\n            :param format_items: format items or not\n        '
    if (not items):
        return
    if format_items:
        items = self._format_items(items, project_disks)
    for host in items:
        self._populate_host(host)
        hostname = self._get_hostname(host)
        self._set_composite_vars(self.get_option('compose'), host, hostname)
        self._add_host_to_composed_groups(self.get_option('groups'), host, hostname)
        self._add_host_to_keyed_groups(self.get_option('keyed_groups'), host, hostname)