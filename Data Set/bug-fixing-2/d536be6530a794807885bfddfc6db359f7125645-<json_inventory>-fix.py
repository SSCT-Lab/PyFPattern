

def json_inventory(self, top):
    seen = set()

    def format_group(group):
        results = {
            
        }
        results[group.name] = {
            
        }
        if (group.name != 'all'):
            results[group.name]['hosts'] = [h.name for h in sorted(group.hosts, key=attrgetter('name'))]
        results[group.name]['children'] = []
        for subgroup in sorted(group.child_groups, key=attrgetter('name')):
            results[group.name]['children'].append(subgroup.name)
            if (subgroup.name not in seen):
                results.update(format_group(subgroup))
                seen.add(subgroup.name)
        if self.options.export:
            results[group.name]['vars'] = self._get_group_variables(group)
        self._remove_empty(results[group.name])
        if (not results[group.name]):
            del results[group.name]
        return results
    results = format_group(top)
    results['_meta'] = {
        'hostvars': {
            
        },
    }
    hosts = self.inventory.get_hosts()
    for host in hosts:
        hvars = self._get_host_variables(host)
        if hvars:
            self._remove_internal(hvars)
            results['_meta']['hostvars'][host.name] = hvars
    return results
