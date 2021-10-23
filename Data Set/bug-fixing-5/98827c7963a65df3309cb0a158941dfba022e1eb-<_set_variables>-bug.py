def _set_variables(self, hostvars, groups):
    for host in hostvars:
        self._set_composite_vars(self._config_data.get('compose'), hostvars[host], host)
        for key in hostvars[host]:
            self.inventory.set_variable(host, key, hostvars[host][key])
        self._add_host_to_composed_groups(self._config_data.get('groups'), hostvars[host], host)
        self._add_host_to_keyed_groups(self._config_data.get('keyed_groups'), hostvars[host], host)
    for (group_name, group_hosts) in groups.items():
        self.inventory.add_group(group_name)
        for host in group_hosts:
            self.inventory.add_child(group_name, host)