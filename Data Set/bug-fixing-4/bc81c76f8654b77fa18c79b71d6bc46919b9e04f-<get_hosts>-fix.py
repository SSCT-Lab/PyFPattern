def get_hosts(self, pattern='all', ignore_limits_and_restrictions=False):
    ' \n        Takes a pattern or list of patterns and returns a list of matching\n        inventory host names, taking into account any active restrictions\n        or applied subsets\n        '
    if isinstance(pattern, list):
        pattern_hash = ':'.join(pattern)
    else:
        pattern_hash = pattern
    if (not ignore_limits_and_restrictions):
        if self._subset:
            pattern_hash += (':%s' % to_unicode(self._subset))
        if self._restriction:
            pattern_hash += (':%s' % to_unicode(self._restriction))
    if (pattern_hash not in HOSTS_PATTERNS_CACHE):
        patterns = Inventory.split_host_pattern(pattern)
        hosts = self._evaluate_patterns(patterns)
        if (not ignore_limits_and_restrictions):
            if self._subset:
                subset = self._evaluate_patterns(self._subset)
                hosts = [h for h in hosts if (h in subset)]
            if (self._restriction is not None):
                hosts = [h for h in hosts if (h.name in self._restriction)]
        seen = set()
        HOSTS_PATTERNS_CACHE[pattern_hash] = [x for x in hosts if ((x not in seen) and (not seen.add(x)))]
    return HOSTS_PATTERNS_CACHE[pattern_hash][:]