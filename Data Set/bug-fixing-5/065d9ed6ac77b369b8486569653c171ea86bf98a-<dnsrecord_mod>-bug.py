def dnsrecord_mod(self, zone_name=None, record_name=None, details=None):
    item = get_dnsrecord_dict(details)
    item.update(idnsname=record_name)
    return self._post_json(method='dnsrecord_mod', name=zone_name, item=item)