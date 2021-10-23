def dnszone_add(self, zone_name=None, details=None):
    itens = {
        
    }
    if (details is not None):
        itens.update(details)
    return self._post_json(method='dnszone_add', name=zone_name, item=itens)