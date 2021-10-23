def __init__(self, name=None):
    self.depth = 0
    self.name = name
    self.hosts = []
    self.vars = {
        
    }
    self.child_groups = []
    self.parent_groups = []
    self._hosts_cache = None
    self.priority = 1