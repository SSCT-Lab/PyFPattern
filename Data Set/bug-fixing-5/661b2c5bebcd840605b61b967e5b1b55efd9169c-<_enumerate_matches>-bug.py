def _enumerate_matches(self, pattern):
    '\n        Returns a list of host names matching the given pattern according to the\n        rules explained above in _match_one_pattern.\n        '
    results = []

    def __append_host_to_results(host):
        if (host.name not in results):
            if (not host.implicit):
                results.append(host)
    matched = False
    for group in self._inventory.groups.values():
        if self._match(to_text(group.name), pattern):
            matched = True
            for host in group.get_hosts():
                __append_host_to_results(host)
        else:
            matching_hosts = self._match_list(group.get_hosts(), 'name', pattern)
            if matching_hosts:
                matched = True
                for host in matching_hosts:
                    __append_host_to_results(host)
    if ((not results) and (pattern in C.LOCALHOST)):
        implicit = self._inventory.get_host(pattern)
        if implicit:
            results.append(implicit)
            matched = True
    if (not matched):
        display.warning(('Could not match supplied host pattern, ignoring: %s' % pattern))
    return results