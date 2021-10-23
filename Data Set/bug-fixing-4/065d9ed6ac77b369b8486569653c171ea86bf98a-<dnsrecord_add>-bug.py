def dnsrecord_add(self, zone_name=None, record_name=None, details=None):
    item = dict(idnsname=record_name)
    if (details['record_type'] == 'A'):
        item.update(a_part_ip_address=details['record_value'])
    elif (details['record_type'] == 'AAAA'):
        item.update(aaaa_part_ip_address=details['record_value'])
    elif (details['record_type'] == 'A6'):
        item.update(a6_part_data=details['record_value'])
    elif (details['record_type'] == 'CNAME'):
        item.update(cname_part_hostname=details['record_value'])
    elif (details['record_type'] == 'DNAME'):
        item.update(dname_part_target=details['record_value'])
    elif (details['record_type'] == 'PTR'):
        item.update(ptr_part_hostname=details['record_value'])
    elif (details['record_type'] == 'TXT'):
        item.update(txtrecord=details['record_value'])
    return self._post_json(method='dnsrecord_add', name=zone_name, item=item)