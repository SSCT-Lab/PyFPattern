def dnszone_find(self, zone_name):
    return self._post_json(method='dnszone_find', name=zone_name, item={
        'idnsname': zone_name,
    })