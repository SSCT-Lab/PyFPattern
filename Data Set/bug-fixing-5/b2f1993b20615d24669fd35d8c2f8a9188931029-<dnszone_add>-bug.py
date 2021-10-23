def dnszone_add(self, zone_name=None, details=None):
    return self._post_json(method='dnszone_add', name=zone_name, item={
        
    })