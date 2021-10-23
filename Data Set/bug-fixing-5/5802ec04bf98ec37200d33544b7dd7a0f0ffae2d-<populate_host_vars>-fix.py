def populate_host_vars(self, hosts, variables, group=None, port=None):
    if (not isinstance(variables, MutableMapping)):
        raise AnsibleParserError(('Invalid data from file, expected dictionary and got:\n\n%s' % to_native(variables)))
    for host in hosts:
        self.inventory.add_host(host, group=group, port=port)
        for k in variables:
            self.inventory.set_variable(host, k, variables[k])