def _parse_groups(self, group, group_data):
    if (group not in self.groups):
        self.groups[group] = Group(name=group)
    if isinstance(group_data, dict):
        for section in ['vars', 'children', 'hosts']:
            if ((section in group_data) and isinstance(group_data[section], string_types)):
                group_data[section] = {
                    group_data[section]: None,
                }
        if group_data.get('vars', False):
            for var in group_data['vars']:
                if (var != 'ansible_group_priority'):
                    self.groups[group].set_variable(var, group_data['vars'][var])
                else:
                    self.groups[group].set_priority(group_data['vars'][var])
        if group_data.get('children', False):
            for subgroup in group_data['children']:
                self._parse_groups(subgroup, group_data['children'][subgroup])
                self.groups[group].add_child_group(self.groups[subgroup])
        if group_data.get('hosts', False):
            for host_pattern in group_data['hosts']:
                hosts = self._parse_host(host_pattern, group_data['hosts'][host_pattern])
                for h in hosts:
                    self.groups[group].add_host(h)