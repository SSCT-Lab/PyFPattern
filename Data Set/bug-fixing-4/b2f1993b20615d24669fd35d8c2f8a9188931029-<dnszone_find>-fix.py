def dnszone_find(self, zone_name, details=None):
    itens = {
        'idnsname': zone_name,
    }
    if (details is not None):
        itens.update(details)
    return self._post_json(method='dnszone_find', name=zone_name, item=itens)