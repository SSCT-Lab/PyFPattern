def serialize(self):
    parent_groups = []
    for parent in self.parent_groups:
        parent_groups.append(parent.serialize())
    self._hosts = None
    result = dict(name=self.name, vars=self.vars.copy(), parent_groups=parent_groups, depth=self.depth, hosts=self.hosts)
    return result