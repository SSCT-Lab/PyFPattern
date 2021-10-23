def reconcile_inventory(self):
    ' Ensure inventory basic rules, run after updates '
    display.debug('Reconcile groups and hosts in inventory.')
    self.current_source = None
    group_names = set()
    for g in self.groups:
        group = self.groups[g]
        group_names.add(group.name)
        if ((group.name != 'all') and (not group.get_ancestors())):
            self.add_child('all', group.name)
    host_names = set()
    for host in self.hosts.values():
        host_names.add(host.name)
        mygroups = host.get_groups()
        if (('all' not in mygroups) and (not host.implicit)):
            self.add_child('all', host.name)
        if (self.groups['ungrouped'] in mygroups):
            if set(mygroups).difference(set([self.groups['all'], self.groups['ungrouped']])):
                host.remove_group(self.groups['ungrouped'])
        elif (not host.implicit):
            length = len(mygroups)
            if ((length == 0) or ((length == 1) and (all in mygroups))):
                self.add_child('ungrouped', host.name)
        if host.implicit:
            host.vars = combine_vars(self.groups['all'].get_vars(), host.vars)
    for conflict in group_names.intersection(host_names):
        display.warning(('Found both group and host with same name: %s' % conflict))
    self._groups_dict_cache = {
        
    }