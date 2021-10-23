def get_hosts(self, pattern='all', ignore_limits=False, ignore_restrictions=False, order=None):
    '\n        Takes a pattern or list of patterns and returns a list of matching\n        inventory host names, taking into account any active restrictions\n        or applied subsets\n        '
    if isinstance(pattern, list):
        pattern_hash = ':'.join(pattern)
    else:
        pattern_hash = pattern
    if ((not ignore_limits) and self._subset):
        pattern_hash += (':%s' % to_text(self._subset, errors='surrogate_or_strict'))
    if ((not ignore_restrictions) and self._restriction):
        pattern_hash += (':%s' % to_text(self._restriction, errors='surrogate_or_strict'))
    if (pattern_hash not in self._hosts_patterns_cache):
        patterns = split_host_pattern(pattern)
        hosts = self._evaluate_patterns(patterns)
        if ((not ignore_limits) and self._subset):
            subset = self._evaluate_patterns(self._subset)
            hosts = [h for h in hosts if (h in subset)]
        if ((not ignore_restrictions) and self._restriction):
            hosts = [h for h in hosts if (h.name in self._restriction)]
        seen = set()
        self._hosts_patterns_cache[pattern_hash] = [x for x in hosts if ((x not in seen) and (not seen.add(x)))]
    if (order in ['sorted', 'reverse_sorted']):
        from operator import attrgetter
        hosts = sorted(self._hosts_patterns_cache[pattern_hash][:], key=attrgetter('name'), reverse=(order == 'reverse_sorted'))
    elif (order == 'reverse_inventory'):
        hosts = sorted(self._hosts_patterns_cache[pattern_hash][:], reverse=True)
    else:
        hosts = self._hosts_patterns_cache[pattern_hash][:]
        if (order == 'shuffle'):
            from random import shuffle
            shuffle(hosts)
        elif (order not in [None, 'inventory']):
            AnsibleOptionsError(("Invalid 'order' specified for inventory hosts: %s" % order))
    return hosts