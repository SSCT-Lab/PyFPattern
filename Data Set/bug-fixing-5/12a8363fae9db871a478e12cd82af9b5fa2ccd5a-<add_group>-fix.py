def add_group(self, group):
    ' adds a group to inventory if not there already '
    if group:
        if (group not in self.groups):
            g = Group(group)
            self.groups[group] = g
            self._groups_dict_cache = {
                
            }
            display.debug(('Added group %s to inventory' % group))
        else:
            display.debug(('group %s already in inventory' % group))
    else:
        raise AnsibleError(('Invalid empty/false group name provided: %s' % group))