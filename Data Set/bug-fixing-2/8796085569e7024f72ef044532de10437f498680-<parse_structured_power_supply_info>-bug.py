

def parse_structured_power_supply_info(self, data):
    if data.get('powersup').get('TABLE_psinfo_n3k'):
        data = data['powersup']['TABLE_psinfo_n3k']['ROW_psinfo_n3k']
    else:
        data = data['powersup']['TABLE_psinfo']['ROW_psinfo']
    objects = list(self.transform_iterable(data, self.POWERSUP_MAP))
    return objects
