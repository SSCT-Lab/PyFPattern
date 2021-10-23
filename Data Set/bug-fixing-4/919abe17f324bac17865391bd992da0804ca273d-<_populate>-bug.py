def _populate(self):
    for host in self._get_hosts():
        if host.get('name'):
            self.inventory.add_host(host['name'])
            group_name = host.get('hostgroup_title', host.get('hostgroup_name'))
            if group_name:
                group_name = self.to_safe(('%s%s' % (self.get_option('group_prefix'), group_name.lower())))
                self.inventory.add_group(group_name)
                self.inventory.add_child(group_name, host['name'])
            try:
                for (k, v) in host.items():
                    if (k not in ('name', 'hostgroup_title', 'hostgroup_name')):
                        try:
                            self.inventory.set_variable(host['name'], (self.get_option('vars_prefix') + k), v)
                        except ValueError as e:
                            self.display.warning(('Could not set host info hostvar for %s, skipping %s: %s' % (host, k, to_native(e))))
            except ValueError as e:
                self.display.warning(('Could not get host info for %s, skipping: %s' % (host['name'], to_native(e))))
            if self.get_option('want_params'):
                for (k, v) in self._get_all_params_by_id(host['id']).items():
                    try:
                        self.inventory.set_variable(host['name'], k, v)
                    except ValueError as e:
                        self.display.warning(('Could not set parameter hostvar for %s, skipping %s: %s' % (host, k, to_native(e))))
            if self.get_option('want_facts'):
                self.inventory.set_variable(host['name'], 'ansible_facts', self._get_facts(host))