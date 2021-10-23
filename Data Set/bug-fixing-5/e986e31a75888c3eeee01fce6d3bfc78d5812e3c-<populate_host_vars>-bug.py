def populate_host_vars(self, hosts, variables, group=None, port=None):
    if hosts:
        for host in hosts:
            self.inventory.add_host(host, group=group, port=port)
            if variables:
                for k in variables:
                    self.inventory.set_variable(host, k, variables[k])