def _parse(self, data):
    '\n        Populates self.groups from the given array of lines. Raises an error on\n        any parse failure.\n        '
    self._compile_patterns()
    for group_name in data.keys():
        self._parse_groups(group_name, data[group_name])
    for group in self.groups.values():
        if ((group.depth == 0) and (group.name not in ('all', 'ungrouped'))):
            self.groups['all'].add_child_group(Group(group_name))