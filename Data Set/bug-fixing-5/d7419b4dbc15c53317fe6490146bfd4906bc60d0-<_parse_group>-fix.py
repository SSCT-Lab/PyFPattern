def _parse_group(self, group, group_data):
    self.inventory.add_group(group)
    if isinstance(group_data, MutableMapping):
        for section in ['vars', 'children', 'hosts']:
            if (section in group_data):
                if isinstance(group_data[section], string_types):
                    group_data[section] = {
                        group_data[section]: None,
                    }
                if (not isinstance(group_data[section], MutableMapping)):
                    raise AnsibleParserError(('Invalid "%s" entry for "%s" group, requires a dictionary, found "%s" instead.' % (section, group, type(group_data[section]))))
        for key in group_data:
            if (key == 'vars'):
                for var in group_data['vars']:
                    self.inventory.set_variable(group, var, group_data['vars'][var])
            elif (key == 'children'):
                for subgroup in group_data['children']:
                    self._parse_group(subgroup, group_data['children'][subgroup])
                    self.inventory.add_child(group, subgroup)
            elif (key == 'hosts'):
                for host_pattern in group_data['hosts']:
                    (hosts, port) = self._parse_host(host_pattern)
                    self._populate_host_vars(hosts, (group_data['hosts'][host_pattern] or {
                        
                    }), group, port)
            else:
                self.display.warning(('Skipping unexpected key (%s) in group (%s), only "vars", "children" and "hosts" are valid' % (key, group)))
    else:
        self.display.warning(("Skipping '%s' as this is not a valid group name" % group))