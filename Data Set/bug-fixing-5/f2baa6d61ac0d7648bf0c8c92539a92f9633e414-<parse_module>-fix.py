def parse_module(self, data):
    data = data['TABLE_modinfo']['ROW_modinfo']
    if isinstance(data, dict):
        data = [data]
    objects = list(self.transform_iterable(data, self.MODULE_MAP))
    return objects