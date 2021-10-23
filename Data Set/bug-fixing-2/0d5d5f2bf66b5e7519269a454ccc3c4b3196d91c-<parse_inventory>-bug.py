

def parse_inventory(self, host_list):
    if isinstance(host_list, string_types):
        if (',' in host_list):
            host_list = host_list.split(',')
            host_list = [h for h in host_list if (h and h.strip())]
    self.parser = None
    ungrouped = Group('ungrouped')
    all = Group('all')
    all.add_child_group(ungrouped)
    base_groups = frozenset([all, ungrouped])
    self.groups = dict(all=all, ungrouped=ungrouped)
    if (host_list is None):
        pass
    elif isinstance(host_list, list):
        for h in host_list:
            try:
                (host, port) = parse_address(h, allow_ranges=False)
            except AnsibleError as e:
                display.vvv(('Unable to parse address from hostname, leaving unchanged: %s' % to_text(e)))
                host = h
                port = None
            new_host = Host(host, port)
            if (h in C.LOCALHOST):
                if (self.localhost is not None):
                    display.warning(('A duplicate localhost-like entry was found (%s). First found localhost was %s' % (h, self.localhost.name)))
                display.vvvv(('Set default localhost to %s' % h))
                self.localhost = new_host
            all.add_host(new_host)
    elif self._loader.path_exists(host_list):
        if self.is_directory(host_list):
            host_list = os.path.join(self.host_list, '')
            self.parser = InventoryDirectory(loader=self._loader, groups=self.groups, filename=host_list)
        else:
            self.parser = get_file_parser(host_list, self.groups, self._loader)
            vars_loader.add_directory(self._basedir, with_subdir=True)
        if (not self.parser):
            raise AnsibleError(('Unable to parse %s as an inventory source' % host_list))
    else:
        display.warning(('Host file not found: %s' % to_text(host_list)))
    self._vars_plugins = [x for x in vars_loader.all(self)]
    group_names = set()
    for g in self.groups:
        group = self.groups[g]
        group.vars = combine_vars(group.vars, self.get_group_variables(group.name))
        self.get_group_vars(group)
        group_names.add(group.name)
    host_names = set()
    for host in self.get_hosts(ignore_limits=True, ignore_restrictions=True):
        host.vars = combine_vars(host.vars, self.get_host_variables(host.name))
        self.get_host_vars(host)
        host_names.add(host.name)
        mygroups = host.get_groups()
        if (all not in mygroups):
            all.add_host(host)
        if (ungrouped in mygroups):
            if set(mygroups).difference(base_groups):
                host.remove_group(ungrouped)
        else:
            length = len(mygroups)
            if ((length == 0) or ((length == 1) and (all in mygroups))):
                ungrouped.add_host(host)
    for conflict in group_names.intersection(host_names):
        display.warning(('Found both group and host with same name: %s' % conflict))
