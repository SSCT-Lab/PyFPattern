def list_groups(api):
    '\n    This function prints a list of all host groups. This function requires\n    one argument, the FreeIPA/IPA API object.\n    '
    inventory = {
        
    }
    hostvars = {
        
    }
    ipa_version = api.Command.env()['result']['version']
    result = api.Command.hostgroup_find()['result']
    for hostgroup in result:
        members = []
        if (StrictVersion(ipa_version) >= StrictVersion('4.0.0')):
            hostgroup_name = hostgroup['cn'][0]
            hostgroup = api.Command.hostgroup_show(hostgroup_name)['result']
        if ('member_host' in hostgroup):
            members = [host for host in hostgroup['member_host']]
        if ('memberindirect_host' in hostgroup):
            members += (host for host in hostgroup['memberindirect_host'])
        inventory[hostgroup['cn'][0]] = {
            'hosts': [host for host in members],
        }
        for member in members:
            hostvars[member] = {
                
            }
    inventory['_meta'] = {
        'hostvars': hostvars,
    }
    inv_string = json.dumps(inventory, indent=1, sort_keys=True)
    print(inv_string)
    return None