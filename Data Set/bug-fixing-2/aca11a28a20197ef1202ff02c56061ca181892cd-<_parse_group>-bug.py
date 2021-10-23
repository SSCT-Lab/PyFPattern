

def _parse_group(self, group, group_data):
    if self.patterns['groupname'].match(group):
        self.inventory.add_group(group)
        if isinstance(group_data, dict):
            for section in ['vars', 'children', 'hosts']:
                if ((section in group_data) and isinstance(group_data[section], string_types)):
                    group_data[section] = {
                        group_data[section]: None,
                    }
            if ('vars' in group_data):
                for var in group_data['vars']:
                    self.inventory.set_variable(group, var, group_data['vars'][var])
            if ('children' in group_data):
                for subgroup in group_data['children']:
                    self._parse_group(subgroup, group_data['children'][subgroup])
                    self.inventory.add_child(group, subgroup)
            if ('hosts' in group_data):
                for host_pattern in group_data['hosts']:
                    (hosts, port) = self._parse_host(host_pattern)
                    self.populate_host_vars(hosts, (group_data['hosts'][host_pattern] or {
                        
                    }), group, port)
    else:
        self.display.warning(("Skipping '%s' as this is not a valid group name" % group))
