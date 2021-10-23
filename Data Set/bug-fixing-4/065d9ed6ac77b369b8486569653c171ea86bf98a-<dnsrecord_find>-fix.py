def dnsrecord_find(self, zone_name, record_name):
    return self._post_json(method='dnsrecord_find', name=zone_name, item={
        'idnsname': record_name,
        'all': True,
    })