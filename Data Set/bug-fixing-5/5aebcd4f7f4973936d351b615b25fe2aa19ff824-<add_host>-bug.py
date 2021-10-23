def add_host(self, host, group=None, port=None):
    ' adds a host to inventory and possibly a group if not there already '
    g = None
    if group:
        if (group in self.groups):
            g = self.groups[group]
        else:
            raise AnsibleError(('Could not find group %s in inventory' % group))
    if (host not in self.hosts):
        h = Host(host, port)
        self.hosts[host] = h
        if self.current_source:
            self.set_variable(host, 'inventory_file', os.path.basename(self.current_source))
            self.set_variable(host, 'inventory_dir', basedir(self.current_source))
        else:
            self.set_variable(host, 'inventory_file', None)
            self.set_variable(host, 'inventory_dir', None)
        display.debug(('Added host %s to inventory' % host))
        if (host in C.LOCALHOST):
            if (self.localhost is None):
                self.localhost = self.hosts[host]
                display.vvvv(('Set default localhost to %s' % h))
            else:
                display.warning(('A duplicate localhost-like entry was found (%s). First found localhost was %s' % (h, self.localhost.name)))
    else:
        h = self.hosts[host]
    if (g and (h not in g.get_hosts())):
        g.add_host(h)
        self._groups_dict_cache = {
            
        }
        display.debug(('Added host %s to group %s' % (host, group)))