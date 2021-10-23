def ensure(module, client):
    zone_name = module.params['zone_name']
    state = module.params['state']
    dynamicupdate = module.params['dynamicupdate']
    ipa_dnszone = client.dnszone_find(zone_name)
    changed = False
    if (state == 'present'):
        if (not ipa_dnszone):
            changed = True
            if (not module.check_mode):
                client.dnszone_add(zone_name=zone_name, details={
                    'idnsallowdynupdate': dynamicupdate,
                })
        else:
            changed = False
    elif ipa_dnszone:
        changed = True
        if (not module.check_mode):
            client.dnszone_del(zone_name=zone_name)
    return (changed, client.dnszone_find(zone_name))