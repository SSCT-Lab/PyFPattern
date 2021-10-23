

def main():
    argument_spec = meraki_argument_spec()
    argument_spec.update(net_id=dict(type='str'), type=dict(type='str', choices=['wireless', 'switch', 'appliance', 'combined'], aliases=['net_type']), tags=dict(type='str'), timezone=dict(type='str'), net_name=dict(type='str', aliases=['name', 'network']), state=dict(type='str', choices=['present', 'query', 'absent'], default='present'), disable_my_meraki=dict(type='bool'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    meraki = MerakiModule(module, function='network')
    module.params['follow_redirects'] = 'all'
    payload = None
    create_urls = {
        'network': '/organizations/{org_id}/networks',
    }
    update_urls = {
        'network': '/networks/{net_id}',
    }
    delete_urls = {
        'network': '/networks/{net_id}',
    }
    meraki.url_catalog['create'] = create_urls
    meraki.url_catalog['update'] = update_urls
    meraki.url_catalog['delete'] = delete_urls
    if ((not meraki.params['org_name']) and (not meraki.params['org_id'])):
        meraki.fail_json(msg='org_name or org_id parameters are required')
    if (meraki.params['state'] != 'query'):
        if ((not meraki.params['net_name']) or meraki.params['net_id']):
            meraki.fail_json(msg='net_name or net_id is required for present or absent states')
    if (meraki.params['net_name'] and meraki.params['net_id']):
        meraki.fail_json(msg='net_name and net_id are mutually exclusive')
    if module.check_mode:
        return meraki.result
    if (meraki.params['state'] == 'present'):
        payload = dict()
        if meraki.params['net_name']:
            payload['name'] = meraki.params['net_name']
        if meraki.params['type']:
            payload['type'] = meraki.params['type']
            if (meraki.params['type'] == 'combined'):
                payload['type'] = 'switch wireless appliance'
        if meraki.params['tags']:
            payload['tags'] = construct_tags(meraki.params['tags'])
        if meraki.params['timezone']:
            payload['timeZone'] = meraki.params['timezone']
        if meraki.params['disable_my_meraki']:
            payload['disableMyMerakiCom'] = meraki.params['disable_my_meraki']
    org_id = meraki.params['org_id']
    if (not org_id):
        org_id = meraki.get_org_id(meraki.params['org_name'])
    nets = meraki.get_nets(org_id=org_id)
    if (meraki.params['state'] == 'query'):
        if ((not meraki.params['net_name']) and (not meraki.params['net_id'])):
            meraki.result['data'] = nets
        elif (meraki.params['net_name'] or (meraki.params['net_id'] is not None)):
            meraki.result['data'] = meraki.get_net(meraki.params['org_name'], meraki.params['net_name'], data=nets)
    elif (meraki.params['state'] == 'present'):
        if meraki.params['net_name']:
            if (is_net_valid(meraki, meraki.params['net_name'], nets) is False):
                path = meraki.construct_path('create', org_id=org_id)
                r = meraki.request(path, method='POST', payload=json.dumps(payload))
                if (meraki.status == 201):
                    meraki.result['data'] = r
                    meraki.result['changed'] = True
            else:
                net = meraki.get_net(meraki.params['org_name'], meraki.params['net_name'], data=nets)
                if meraki.is_update_required(net, payload):
                    path = meraki.construct_path('update', net_id=meraki.get_net_id(net_name=meraki.params['net_name'], data=nets))
                    r = meraki.request(path, method='PUT', payload=json.dumps(payload))
                    if (meraki.status == 200):
                        meraki.result['data'] = r
                        meraki.result['changed'] = True
    elif (meraki.params['state'] == 'absent'):
        if (is_net_valid(meraki, meraki.params['net_name'], nets) is True):
            net_id = meraki.get_net_id(net_name=meraki.params['net_name'], data=nets)
            path = meraki.construct_path('delete', net_id=net_id)
            r = meraki.request(path, method='DELETE')
            if (meraki.status == 204):
                meraki.result['changed'] = True
    meraki.exit_json(**meraki.result)
