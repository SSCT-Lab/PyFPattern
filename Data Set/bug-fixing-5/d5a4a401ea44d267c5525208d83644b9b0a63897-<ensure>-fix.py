def ensure(module, client):
    zone_name = module.params['zone_name']
    record_name = module.params['record_name']
    record_ttl = module.params.get('record_ttl')
    state = module.params['state']
    ipa_dnsrecord = client.dnsrecord_find(zone_name, record_name)
    module_dnsrecord = dict(record_type=module.params['record_type'], record_value=module.params['record_value'], record_ttl=to_native(record_ttl, nonstring='passthru'))
    changed = False
    if (state == 'present'):
        if (not ipa_dnsrecord):
            changed = True
            if (not module.check_mode):
                client.dnsrecord_add(zone_name=zone_name, record_name=record_name, details=module_dnsrecord)
        else:
            diff = get_dnsrecord_diff(client, ipa_dnsrecord, module_dnsrecord)
            if (len(diff) > 0):
                changed = True
                if (not module.check_mode):
                    client.dnsrecord_mod(zone_name=zone_name, record_name=record_name, details=module_dnsrecord)
    elif ipa_dnsrecord:
        changed = True
        if (not module.check_mode):
            client.dnsrecord_del(zone_name=zone_name, record_name=record_name, details=module_dnsrecord)
    return (changed, client.dnsrecord_find(zone_name, record_name))