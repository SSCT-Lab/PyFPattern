

def _set_variables(self, hostvars):
    for host in hostvars:
        query = self.get_option('query')
        if (query and isinstance(query, MutableMapping)):
            for varname in query:
                hostvars[host][varname] = self._query_vbox_data(host, query[varname])
        strict = self._options.get('strict', False)
        self._set_composite_vars(self.get_option('compose'), hostvars[host], host, strict=strict)
        for key in hostvars[host]:
            self.inventory.set_variable(host, key, hostvars[host][key])
        self._add_host_to_composed_groups(self.get_option('groups'), hostvars[host], host, strict=strict)
        self._add_host_to_keyed_groups(self.get_option('keyed_groups'), hostvars[host], host, strict=strict)
