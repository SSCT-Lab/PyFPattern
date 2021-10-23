def _enumerate_matches(self, pattern):
    '\n        Returns a list of host names matching the given pattern according to the\n        rules explained above in _match_one_pattern.\n        '
    results = []
    hostnames = set()

    def __append_host_to_results(host):
        if (host.name not in hostnames):
            hostnames.add(host.name)
            results.append(host)
    groups = self.get_groups()
    for group in groups.values():
        if (pattern == 'all'):
            for host in group.get_hosts():
                if host.implicit:
                    continue
                __append_host_to_results(host)
        elif (self._match(group.name, pattern) and (group.name not in ('all', 'ungrouped'))):
            for host in group.get_hosts():
                if host.implicit:
                    continue
                __append_host_to_results(host)
        else:
            matching_hosts = self._match_list(group.get_hosts(), 'name', pattern)
            for host in matching_hosts:
                __append_host_to_results(host)
    if ((pattern in C.LOCALHOST) and (len(results) == 0)):
        new_host = self._create_implicit_localhost(pattern)
        results.append(new_host)
    return results