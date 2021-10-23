@property
def shippable_test_groups(self):
    '\n        :rtype: dict[str, set[int]]\n        '
    if (not self._shippable_test_groups):
        matches = [re.search('^[ #]+- env: T=(?P<group>[^/]+)/(?P<params>.+)/(?P<number>[1-9][0-9]?)$', line) for line in self.shippable_yml_lines]
        entries = [(match.group('group'), int(match.group('number'))) for match in matches if match]
        for (key, value) in entries:
            if (key not in self._shippable_test_groups):
                self._shippable_test_groups[key] = set()
            self._shippable_test_groups[key].add(value)
    return self._shippable_test_groups