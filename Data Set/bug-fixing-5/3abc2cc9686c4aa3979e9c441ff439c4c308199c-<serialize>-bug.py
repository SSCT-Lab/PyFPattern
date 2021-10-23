def serialize(self):
    self._groups_dict_cache = None
    data = {
        'groups': self.groups,
        'hosts': self.hosts,
        'local': self.locahost,
        'source': self.current_source,
    }
    return data