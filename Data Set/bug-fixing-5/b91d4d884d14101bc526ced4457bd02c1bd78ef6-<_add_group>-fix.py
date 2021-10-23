def _add_group(self, host, result_item):
    '\n        Helper function to add a group (if it does not exist), and to assign the\n        specified host to that group.\n        '
    changed = False
    real_host = self._inventory.get_host(host.name)
    group_name = result_item.get('add_group')
    new_group = self._inventory.get_group(group_name)
    if (not new_group):
        new_group = Group(name=group_name)
        self._inventory.add_group(new_group)
        new_group.vars = self._inventory.get_group_vars(new_group)
        allgroup = self._inventory.get_group('all')
        allgroup.add_child_group(new_group)
        changed = True
    if (group_name not in host.get_groups()):
        new_group.add_host(real_host)
        changed = True
    if changed:
        self._inventory.clear_group_dict_cache()
    return changed