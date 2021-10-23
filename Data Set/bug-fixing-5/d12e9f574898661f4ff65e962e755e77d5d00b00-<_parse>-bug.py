def _parse(self, err):
    all_hosts = {
        
    }
    try:
        self.raw = self._loader.load(self.data)
    except Exception as e:
        sys.stderr.write((err + '\n'))
        raise AnsibleError('failed to parse executable inventory script results from {0}: {1}'.format(to_native(self.filename), to_native(e)))
    if (not isinstance(self.raw, Mapping)):
        sys.stderr.write((err + '\n'))
        raise AnsibleError('failed to parse executable inventory script results from {0}: data needs to be formatted as a json dict'.format(to_native(self.filename)))
    group = None
    for (group_name, data) in self.raw.items():
        if (group_name == '_meta'):
            if ('hostvars' in data):
                self.host_vars_from_top = data['hostvars']
                continue
        if (group_name not in self.groups):
            group = self.groups[group_name] = Group(group_name)
        group = self.groups[group_name]
        host = None
        if (not isinstance(data, dict)):
            data = {
                'hosts': data,
            }
        elif (not any(((k in data) for k in ('hosts', 'vars', 'children')))):
            data = {
                'hosts': [group_name],
                'vars': data,
            }
        if ('hosts' in data):
            if (not isinstance(data['hosts'], list)):
                raise AnsibleError(('You defined a group "%s" with bad data for the host list:\n %s' % (group_name, data)))
            for hostname in data['hosts']:
                if (hostname not in all_hosts):
                    all_hosts[hostname] = Host(hostname)
                host = all_hosts[hostname]
                group.add_host(host)
        if ('vars' in data):
            if (not isinstance(data['vars'], dict)):
                raise AnsibleError(('You defined a group "%s" with bad data for variables:\n %s' % (group_name, data)))
            for (k, v) in iteritems(data['vars']):
                group.set_variable(k, v)
    for (group_name, data) in self.raw.items():
        if (group_name == '_meta'):
            continue
        if (isinstance(data, dict) and ('children' in data)):
            for child_name in data['children']:
                if (child_name in self.groups):
                    self.groups[group_name].add_child_group(self.groups[child_name])
    for group in self.groups.values():
        if ((group.depth == 0) and (group.name not in ('all', 'ungrouped'))):
            self.groups['all'].add_child_group(group)