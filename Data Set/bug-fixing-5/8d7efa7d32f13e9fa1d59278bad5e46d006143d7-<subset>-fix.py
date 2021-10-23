def subset(self, subset_pattern):
    "\n        Limits inventory results to a subset of inventory that matches a given\n        pattern, such as to select a given geographic of numeric slice amongst\n        a previous 'hosts' selection that only select roles, or vice versa.\n        Corresponds to --limit parameter to ansible-playbook\n        "
    if (subset_pattern is None):
        self._subset = None
    else:
        subset_patterns = split_host_pattern(subset_pattern)
        results = []
        for x in subset_patterns:
            if x.startswith('@'):
                fd = open(x[1:])
                results.extend([l.strip() for l in fd.read().split('\n')])
                fd.close()
            else:
                results.append(x)
        self._subset = results