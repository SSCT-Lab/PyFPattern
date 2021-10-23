def serialize(self):
    parent_groups = []
    for parent in self.parent_groups:
        parent_groups.append(parent.serialize())
    result = dict(name=self.name, vars=self.vars.copy(), parent_groups=parent_groups, depth=self.depth)
    return result