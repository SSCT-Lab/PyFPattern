def get_dnsrecord_dict(details=None):
    module_dnsrecord = dict()
    if ((details['record_type'] == 'A') and details['record_value']):
        module_dnsrecord.update(arecord=details['record_value'])
    elif ((details['record_type'] == 'AAAA') and details['record_value']):
        module_dnsrecord.update(aaaarecord=details['record_value'])
    elif ((details['record_type'] == 'A6') and details['record_value']):
        module_dnsrecord.update(a6record=details['record_value'])
    elif ((details['record_type'] == 'CNAME') and details['record_value']):
        module_dnsrecord.update(cnamerecord=details['record_value'])
    elif ((details['record_type'] == 'DNAME') and details['record_value']):
        module_dnsrecord.update(dnamerecord=details['record_value'])
    elif ((details['record_type'] == 'PTR') and details['record_value']):
        module_dnsrecord.update(ptrrecord=details['record_value'])
    elif ((details['record_type'] == 'TXT') and details['record_value']):
        module_dnsrecord.update(txtrecord=details['record_value'])
    return module_dnsrecord