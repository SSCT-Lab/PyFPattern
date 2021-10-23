def _parse_groups(self, group, group_data):
    if (group not in self.groups):
        self.groups[group] = Group(name=group)
    if isinstance(group_data, dict):
        for section in ['vars', 'children', 'hosts']:
            if ((section in group_data) and isinstance(group_data[section], string_types)):
                group_data[section] = {
                    group_data[section]: None,
                }
        if ('vars' in group_data):
            for var in group_data['vars']:
                if (var != 'ansible_group_priority'):
                    self.groups[group].set_variable(var, group_data['vars'][var])
                else:
                    self.groups[group].set_priority(group_data['vars'][var])
        if ('children' in group_data):
            for subgroup in group_data['children']:
                self._parse_groups(subgroup, group_data['children'][subgroup])
                self.groups[group].add_child_group(self.groups[subgroup])
        if ('hosts' in group_data):
            for host_pattern in group_data['hosts']:
                hosts = self._parse_host(host_pattern, group_data['hosts'][host_pattern])
                for h in hosts:
                    self.groups[group].add_host(h)