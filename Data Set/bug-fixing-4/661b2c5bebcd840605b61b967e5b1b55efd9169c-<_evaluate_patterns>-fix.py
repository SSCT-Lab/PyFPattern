def _evaluate_patterns(self, patterns):
    '\n        Takes a list of patterns and returns a list of matching host names,\n        taking into account any negative and intersection patterns.\n        '
    patterns = order_patterns(patterns)
    hosts = []
    for p in patterns:
        if (p in self._inventory.hosts):
            hosts.append(self._inventory.get_host(p))
        else:
            that = self._match_one_pattern(p)
            if p.startswith('!'):
                hosts = [h for h in hosts if (h not in frozenset(that))]
            elif p.startswith('&'):
                hosts = [h for h in hosts if (h in frozenset(that))]
            else:
                hosts.extend([h for h in that if (h.name not in frozenset([y.name for y in hosts]))])
    return hosts