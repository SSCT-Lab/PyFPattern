def create_admin(meraki, org_id, name, email):
    payload = dict()
    payload['name'] = name
    payload['email'] = email
    is_admin_existing = find_admin(meraki, get_admins(meraki, org_id), email)
    if (meraki.params['org_access'] is not None):
        payload['orgAccess'] = meraki.params['org_access']
    if (meraki.params['tags'] is not None):
        payload['tags'] = json.loads(meraki.params['tags'])
    if (meraki.params['networks'] is not None):
        nets = meraki.get_nets(org_id=org_id)
        networks = network_factory(meraki, meraki.params['networks'], nets)
        payload['networks'] = networks
    if (is_admin_existing is None):
        path = meraki.construct_path('create', function='admin', org_id=org_id)
        r = meraki.request(path, method='POST', payload=json.dumps(payload))
        if (meraki.status == 201):
            meraki.result['changed'] = True
            return r
    elif (is_admin_existing is not None):
        if (not meraki.params['tags']):
            payload['tags'] = []
        if (not meraki.params['networks']):
            payload['networks'] = []
        if (meraki.is_update_required(is_admin_existing, payload) is True):
            path = (meraki.construct_path('update', function='admin', org_id=org_id) + is_admin_existing['id'])
            r = meraki.request(path, method='PUT', payload=json.dumps(payload))
            if (meraki.status == 200):
                meraki.result['changed'] = True
                return r
        else:
            return (- 1)