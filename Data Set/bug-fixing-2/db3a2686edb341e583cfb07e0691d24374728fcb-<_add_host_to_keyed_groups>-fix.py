

def _add_host_to_keyed_groups(self, keys, variables, host, strict=False):
    ' helper to create groups for plugins based on variable values and add the corresponding hosts to it'
    if (keys and isinstance(keys, list)):
        for keyed in keys:
            if (keyed and isinstance(keyed, dict)):
                variables = combine_vars(variables, self.inventory.get_host(host).get_vars())
                try:
                    key = self._compose(keyed.get('key'), variables)
                except Exception as e:
                    if strict:
                        raise AnsibleParserError(('Could not generate group for host %s from %s entry: %s' % (host, keyed.get('key'), to_native(e))))
                    continue
                if key:
                    prefix = keyed.get('prefix', '')
                    sep = keyed.get('separator', '_')
                    raw_parent_name = keyed.get('parent_group', None)
                    new_raw_group_names = []
                    if isinstance(key, string_types):
                        new_raw_group_names.append(key)
                    elif isinstance(key, list):
                        for name in key:
                            new_raw_group_names.append(name)
                    elif isinstance(key, Mapping):
                        for (gname, gval) in key.items():
                            name = ('%s%s%s' % (gname, sep, gval))
                            new_raw_group_names.append(name)
                    else:
                        raise AnsibleParserError(('Invalid group name format, expected a string or a list of them or dictionary, got: %s' % type(key)))
                    for bare_name in new_raw_group_names:
                        gname = self._sanitize_group_name(('%s%s%s' % (prefix, sep, bare_name)))
                        result_gname = self.inventory.add_group(gname)
                        self.inventory.add_child(result_gname, host)
                        if raw_parent_name:
                            parent_name = self._sanitize_group_name(raw_parent_name)
                            self.inventory.add_group(parent_name)
                            self.inventory.add_child(parent_name, result_gname)
                elif strict:
                    raise AnsibleParserError('No key or key resulted empty, invalid entry')
            else:
                raise AnsibleParserError(('Invalid keyed group entry, it must be a dictionary: %s ' % keyed))
