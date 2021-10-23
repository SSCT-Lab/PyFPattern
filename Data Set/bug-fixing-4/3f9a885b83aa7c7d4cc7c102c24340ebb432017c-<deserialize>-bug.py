def deserialize(self, data):
    self.__init__()
    self.name = data.get('name')
    self.vars = data.get('vars', dict())
    self.depth = data.get('depth', 0)
    parent_groups = data.get('parent_groups', [])
    for parent_data in parent_groups:
        g = Group()
        g.deserialize(parent_data)
        self.parent_groups.append(g)