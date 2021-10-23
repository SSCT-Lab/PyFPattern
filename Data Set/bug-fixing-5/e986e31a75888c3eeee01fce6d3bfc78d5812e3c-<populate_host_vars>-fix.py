def populate_host_vars(self, hosts, variables, group=None, port=None):
    for host in hosts:
        self.inventory.add_host(host, group=group, port=port)
        for k in variables:
            self.inventory.set_variable(host, k, variables[k])