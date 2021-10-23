def update_cache(self):
    'Make calls to foreman and save the output in a cache'
    self.groups = dict()
    self.hosts = dict()
    for host in self._get_hosts():
        dns_name = host['name']
        group = 'hostgroup'
        val = (host.get(('%s_title' % group)) or host.get(('%s_name' % group)))
        if val:
            safe_key = self.to_safe(('%s%s_%s' % (self.group_prefix, group, val.lower())))
            self.inventory[safe_key].append(dns_name)
        for group in ['environment', 'location', 'organization']:
            val = host.get(('%s_name' % group))
            if val:
                safe_key = self.to_safe(('%s%s_%s' % (self.group_prefix, group, val.lower())))
                self.inventory[safe_key].append(dns_name)
        for group in ['lifecycle_environment', 'content_view']:
            val = host.get('content_facet_attributes', {
                
            }).get(('%s_name' % group))
            if val:
                safe_key = self.to_safe(('%s%s_%s' % (self.group_prefix, group, val.lower())))
                self.inventory[safe_key].append(dns_name)
        params = self._resolve_params(host)
        groupby = copy.copy(params)
        for (k, v) in host.items():
            if isinstance(v, str):
                groupby[k] = self.to_safe(v)
            elif isinstance(v, int):
                groupby[k] = v
        for pattern in self.group_patterns:
            try:
                key = pattern.format(**groupby)
                self.inventory[key].append(dns_name)
            except KeyError:
                pass
        self.cache[dns_name] = host
        self.params[dns_name] = params
        self.facts[dns_name] = self._get_facts(host)
        self.inventory['all'].append(dns_name)
    self._write_cache()