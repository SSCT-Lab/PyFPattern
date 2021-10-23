

def _graph_group(self, group, depth=0):
    result = [self._graph_name(('@%s:' % group.name), depth)]
    depth = (depth + 1)
    for kid in sorted(group.child_groups, key=attrgetter('name')):
        result.extend(self._graph_group(kid, depth))
    if (group.name != 'all'):
        for host in sorted(group.hosts, key=attrgetter('name')):
            result.append(self._graph_name(host.name, depth))
            result.extend(self._show_vars(host.get_vars(), (depth + 1)))
    result.extend(self._show_vars(self._get_group_variables(group), depth))
    return result
