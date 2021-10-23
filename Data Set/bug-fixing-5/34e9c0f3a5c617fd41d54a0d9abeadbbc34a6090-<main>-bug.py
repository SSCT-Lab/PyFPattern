def main():
    fw_rules = dict(policy=dict(type='str', choices=['allow', 'deny']), protocol=dict(type='str', choices=['tcp', 'udp', 'icmp', 'any']), dest_port=dict(type='str'), dest_cidr=dict(type='str'), comment=dict(type='str'))
    argument_spec = meraki_argument_spec()
    argument_spec.update(state=dict(type='str', choices=['present', 'query'], default='present'), net_name=dict(type='str'), net_id=dict(type='str'), number=dict(type='str', aliases=['ssid_number']), ssid_name=dict(type='str', aliases=['ssid']), rules=dict(type='list', default=None, elements='dict', options=fw_rules), allow_lan_access=dict(type='bool', default=True))
    result = dict(changed=False)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    meraki = MerakiModule(module, function='mr_l3_firewall')
    meraki.params['follow_redirects'] = 'all'
    query_urls = {
        'mr_l3_firewall': '/networks/{net_id}/ssids/',
    }
    update_urls = {
        'mr_l3_firewall': '/networks/{net_id}/ssids/',
    }
    meraki.url_catalog['get_all'].update(query_urls)
    meraki.url_catalog['update'] = update_urls
    payload = None
    if module.check_mode:
        meraki.exit_json(**meraki.result)
    org_id = meraki.params['org_id']
    orgs = None
    if (org_id is None):
        orgs = meraki.get_orgs()
        for org in orgs:
            if (org['name'] == meraki.params['org_name']):
                org_id = org['id']
    net_id = meraki.params['net_id']
    if (net_id is None):
        if (orgs is None):
            orgs = meraki.get_orgs()
        net_id = meraki.get_net_id(net_name=meraki.params['net_name'], data=meraki.get_nets(org_id=org_id))
    number = meraki.params['number']
    if meraki.params['ssid_name']:
        number = get_ssid_number(meraki.params['ssid_name'], get_ssids(meraki, net_id))
    if (meraki.params['state'] == 'query'):
        meraki.result['data'] = get_rules(meraki, net_id, number)
    elif (meraki.params['state'] == 'present'):
        rules = get_rules(meraki, net_id, number)
        path = meraki.construct_path('get_all', net_id=net_id)
        path = ((path + number) + '/l3FirewallRules')
        if meraki.params['rules']:
            payload = assemble_payload(meraki)
        else:
            payload = dict()
        update = False
        try:
            if (len(rules) != len(payload['rules'])):
                update = True
            if (update is False):
                for r in range((len(rules) - 2)):
                    if (meraki.is_update_required(rules[r], payload[r]) is True):
                        update = True
        except KeyError:
            pass
        if (rules[(len(rules) - 2)] != meraki.params['allow_lan_access']):
            update = True
        if (update is True):
            payload['allowLanAccess'] = meraki.params['allow_lan_access']
            response = meraki.request(path, method='PUT', payload=json.dumps(payload))
            if (meraki.status == 200):
                meraki.result['data'] = response
                meraki.result['changed'] = True
    meraki.exit_json(**meraki.result)