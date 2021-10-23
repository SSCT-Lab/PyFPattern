

def _add_host(self, host_info, iterator):
    '\n        Helper function to add a new host to inventory based on a task result.\n        '
    host_name = host_info.get('host_name')
    new_host = self._inventory.get_host(host_name)
    if (not new_host):
        new_host = Host(name=host_name)
        self._inventory._hosts_cache[host_name] = new_host
        allgroup = self._inventory.get_group('all')
        allgroup.add_host(new_host)
    new_host.vars = combine_vars(new_host.vars, self._inventory.get_host_vars(new_host))
    new_host.vars = combine_vars(new_host.vars, host_info.get('host_vars', dict()))
    new_groups = host_info.get('groups', [])
    for group_name in new_groups:
        if (not self._inventory.get_group(group_name)):
            new_group = Group(group_name)
            self._inventory.add_group(new_group)
            new_group.vars = self._inventory.get_group_variables(group_name)
        else:
            new_group = self._inventory.get_group(group_name)
        new_group.add_host(new_host)
        if (self._inventory.groups is not None):
            if (group_name in self._inventory.groups):
                if (new_host not in self._inventory.get_group(group_name).hosts):
                    self._inventory.get_group(group_name).hosts.append(new_host.name)
    self._inventory.clear_pattern_cache()
    self._variable_manager.invalidate_hostvars_cache(play=iterator._play)
