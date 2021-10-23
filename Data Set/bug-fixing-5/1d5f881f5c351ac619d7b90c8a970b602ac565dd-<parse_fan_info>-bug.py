def parse_fan_info(self, data):
    objects = list()
    if data.get('fandetails'):
        data = data['fandetails']['TABLE_faninfo']['ROW_faninfo']
    elif data.get('fandetails_3k'):
        data = data['fandetails_3k']['TABLE_faninfo']['ROW_faninfo']
    else:
        return objects
    objects = list(self.transform_iterable(data, self.FAN_MAP))
    return objects