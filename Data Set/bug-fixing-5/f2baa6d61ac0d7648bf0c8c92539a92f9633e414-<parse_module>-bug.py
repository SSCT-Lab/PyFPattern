def parse_module(self, data):
    data = data['TABLE_modinfo']['ROW_modinfo']
    objects = list(self.transform_iterable(data, self.MODULE_MAP))
    return objects