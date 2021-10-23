def parse_power_supply_info(self, data):
    data = data['powersup']['TABLE_psinfo']['ROW_psinfo']
    objects = list(self.transform_iterable(data, self.POWERSUP_MAP))
    return objects