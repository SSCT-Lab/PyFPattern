def _set_variables(self, hostvars):
    for host in hostvars:
        query = self.get_option('query')
        if (query and isinstance(query, MutableMapping)):
            for varname in query:
                hostvars[host][varname] = self._query_vbox_data(host, query[varname])
        self._set_composite_vars(self.get_option('compose'), hostvars, host)
        for key in hostvars[host]:
            self.inventory.set_variable(host, key, hostvars[host][key])
        self._add_host_to_composed_groups(self.get_option('groups'), hostvars, host)