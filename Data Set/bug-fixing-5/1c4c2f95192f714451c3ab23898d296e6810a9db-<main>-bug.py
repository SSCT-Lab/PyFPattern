def main():
    argument_spec = meraki_argument_spec()
    argument_spec.update(state=dict(type='str', choices=['absent', 'present', 'query'], default='query'), net_name=dict(type='str', aliases=['network']), net_id=dict(type='str'), name=dict(type='str'), url=dict(type='str'), shared_secret=dict(type='str', no_log=True), webhook_id=dict(type='str'), test=dict(type='str', choices=['test', 'status']), test_id=dict(type='str'))
    result = dict(changed=False)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    meraki = MerakiModule(module, function='webhooks')
    meraki.params['follow_redirects'] = 'all'
    query_url = {
        'webhooks': '/networks/{net_id}/httpServers',
    }
    query_one_url = {
        'webhooks': '/networks/{net_id}/httpServers/{hookid}',
    }
    create_url = {
        'webhooks': '/networks/{net_id}/httpServers',
    }
    update_url = {
        'webhooks': '/networks/{net_id}/httpServers/{hookid}',
    }
    delete_url = {
        'webhooks': '/networks/{net_id}/httpServers/{hookid}',
    }
    test_url = {
        'webhooks': '/networks/{net_id}/httpServers/webhookTests',
    }
    test_status_url = {
        'webhooks': '/networks/{net_id}/httpServers/webhookTests/{testid}',
    }
    meraki.url_catalog['get_all'].update(query_url)
    meraki.url_catalog['get_one'].update(query_one_url)
    meraki.url_catalog['create'] = create_url
    meraki.url_catalog['update'] = update_url
    meraki.url_catalog['delete'] = delete_url
    meraki.url_catalog['test'] = test_url
    meraki.url_catalog['test_status'] = test_status_url
    org_id = meraki.params['org_id']
    if (org_id is None):
        org_id = meraki.get_org_id(meraki.params['org_name'])
    net_id = meraki.params['net_id']
    if (net_id is None):
        nets = meraki.get_nets(org_id=org_id)
        net_id = meraki.get_net_id(net_name=meraki.params['net_name'], data=nets)
    webhook_id = meraki.params['webhook_id']
    if ((webhook_id is None) and meraki.params['name']):
        webhooks = get_all_webhooks(meraki, net_id)
        webhook_id = get_webhook_id(meraki.params['name'], webhooks)
    if ((meraki.params['state'] == 'present') and (meraki.params['test'] is None)):
        payload = {
            'name': meraki.params['name'],
            'url': meraki.params['url'],
            'sharedSecret': meraki.params['shared_secret'],
        }
    if (meraki.params['state'] == 'query'):
        if (webhook_id is not None):
            path = meraki.construct_path('get_one', net_id=net_id, custom={
                'hookid': webhook_id,
            })
            response = meraki.request(path, method='GET')
            if (meraki.status == 200):
                meraki.result['data'] = response
        else:
            path = meraki.construct_path('get_all', net_id=net_id)
            response = meraki.request(path, method='GET')
            if (meraki.status == 200):
                meraki.result['data'] = response
    elif (meraki.params['state'] == 'present'):
        if (meraki.params['test'] == 'test'):
            payload = {
                'url': meraki.params['url'],
            }
            path = meraki.construct_path('test', net_id=net_id)
            response = meraki.request(path, method='POST', payload=json.dumps(payload))
            if (meraki.status == 200):
                meraki.result['data'] = response
                meraki.exit_json(**meraki.result)
        elif (meraki.params['test'] == 'status'):
            if (meraki.params['test_id'] is None):
                meraki.fail_json('test_id is required when querying test status.')
            path = meraki.construct_path('test_status', net_id=net_id, custom={
                'testid': meraki.params['test_id'],
            })
            response = meraki.request(path, method='GET')
            if (meraki.status == 200):
                meraki.result['data'] = response
                meraki.exit_json(**meraki.result)
        if (webhook_id is None):
            if (webhooks is None):
                wehooks = get_all_webhooks(meraki, net_id)
            webhook_id = get_webhook_id(meraki.params['name'], webhooks)
        if (webhook_id is None):
            if (meraki.check_mode is True):
                meraki.result['data'] = payload
                meraki.result['data']['networkId'] = net_id
                meraki.result['changed'] = True
                meraki.exit_json(**meraki.result)
            path = meraki.construct_path('create', net_id=net_id)
            response = meraki.request(path, method='POST', payload=json.dumps(payload))
            if (meraki.status == 201):
                meraki.result['data'] = response
                meraki.result['changed'] = True
        else:
            path = meraki.construct_path('get_one', net_id=net_id, custom={
                'hookid': webhook_id,
            })
            original = meraki.request(path, method='GET')
            if meraki.is_update_required(original, payload):
                if (meraki.check_mode is True):
                    diff = recursive_diff(original, payload)
                    original.update(payload)
                    meraki.result['diff'] = {
                        'before': diff[0],
                        'after': diff[1],
                    }
                    meraki.result['data'] = original
                    meraki.result['changed'] = True
                    meraki.exit_json(**meraki.result)
                path = meraki.construct_path('update', net_id=net_id, custom={
                    'hookid': webhook_id,
                })
                response = meraki.request(path, method='PUT', payload=json.dumps(payload))
                if (meraki.status == 200):
                    meraki.result['data'] = response
                    meraki.result['changed'] = True
            else:
                meraki.result['data'] = original
    elif (meraki.params['state'] == 'absent'):
        if (webhook_id is None):
            if (webhooks is None):
                webhooks = get_all_webhooks(meraki, net_id)
            webhook_id = get_webhook_id(meraki.params['name'], webhooks)
            if (webhook_id is None):
                meraki.fail_json(msg='There is no webhook with the name {0}'.format(meraki.params['name']))
        if webhook_id:
            if (meraki.module.check_mode is True):
                meraki.result['data'] = None
                meraki.result['changed'] = True
                meraki.exit_json(**meraki.result)
            path = meraki.construct_path('delete', net_id=net_id, custom={
                'hookid': webhook_id,
            })
            response = meraki.request(path, method='DELETE')
            if (meraki.status == 204):
                meraki.result['data'] = response
                meraki.result['changed'] = True
    meraki.exit_json(**meraki.result)