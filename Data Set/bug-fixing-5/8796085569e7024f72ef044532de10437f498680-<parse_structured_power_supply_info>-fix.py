def parse_structured_power_supply_info(self, data):
    if data.get('powersup').get('TABLE_psinfo_n3k'):
        fact = data['powersup']['TABLE_psinfo_n3k']['ROW_psinfo_n3k']
    elif isinstance(data['powersup']['TABLE_psinfo'], list):
        fact = []
        for i in data['powersup']['TABLE_psinfo']:
            fact.append(i['ROW_psinfo'])
    else:
        fact = data['powersup']['TABLE_psinfo']['ROW_psinfo']
    objects = list(self.transform_iterable(fact, self.POWERSUP_MAP))
    return objects