def _merge_groups(self, group, newgroup):
    ' Merge all of instance newgroup into group,\n            update parent/child relationships\n            group lists may still contain group objects that exist in self with\n            same name, but was instanciated as a different object in some other\n            inventory parser; these are handled later '
    if (group.name != newgroup.name):
        raise AnsibleError(('Cannot merge inventory group %s with %s' % (group.name, newgroup.name)))
    group.depth = max([group.depth, newgroup.depth])
    for host in newgroup.hosts:
        grouphosts = dict([(h.name, h) for h in group.hosts])
        if (host.name in grouphosts):
            self._merge_hosts(grouphosts[host.name], host)
        else:
            group.add_host(self.hosts[host.name])
            for hostgroup in [g for g in host.groups]:
                if ((hostgroup.name == group.name) and (hostgroup != self.groups[group.name])):
                    self.hosts[host.name].groups.remove(hostgroup)
    for newchild in newgroup.child_groups:
        childgroups = dict([(g.name, g) for g in group.child_groups])
        if (newchild.name not in childgroups):
            self.groups[group.name].add_child_group(newchild)
    for newparent in newgroup.parent_groups:
        parentgroups = dict([(g.name, g) for g in group.parent_groups])
        if (newparent.name not in parentgroups):
            if (newparent.name not in self.groups):
                self.groups[newparent.name] = newparent
            self.groups[newparent.name].add_child_group(group)
    group.vars = combine_vars(group.vars, newgroup.vars)