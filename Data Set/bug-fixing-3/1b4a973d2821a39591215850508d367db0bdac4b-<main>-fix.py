def main():
    argument_spec = meraki_argument_spec()
    argument_spec.update(state=dict(type='str', choices=['present', 'query', 'absent'], required=True), name=dict(type='str'), email=dict(type='str'), org_access=dict(type='str', aliases=['orgAccess'], choices=['full', 'read-only', 'none']), tags=dict(type='json'), networks=dict(type='json'), org_name=dict(type='str', aliases=['organization']), org_id=dict(type='str'))
    result = dict(changed=False)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    meraki = MerakiModule(module, function='admin')
    meraki.function = 'admin'
    meraki.params['follow_redirects'] = 'all'
    query_urls = {
        'admin': '/organizations/{org_id}/admins',
    }
    create_urls = {
        'admin': '/organizations/{org_id}/admins',
    }
    update_urls = {
        'admin': '/organizations/{org_id}/admins/',
    }
    revoke_urls = {
        'admin': '/organizations/{org_id}/admins/',
    }
    meraki.url_catalog['query'] = query_urls
    meraki.url_catalog['create'] = create_urls
    meraki.url_catalog['update'] = update_urls
    meraki.url_catalog['revoke'] = revoke_urls
    try:
        meraki.params['auth_key'] = os.environ['MERAKI_KEY']
    except KeyError:
        pass
    if (meraki.params['auth_key'] is None):
        module.fail_json(msg='Meraki Dashboard API key not set')
    payload = None
    if module.check_mode:
        return result
    if (meraki.params['state'] == 'query'):
        meraki.mututally_exclusive = ['name', 'email']
        if ((not meraki.params['org_name']) and (not meraki.params['org_id'])):
            meraki.fail_json(msg='org_name or org_id required')
    meraki.required_if = [(['state'], ['absent'], ['email'])]
    org_id = meraki.params['org_id']
    if (not meraki.params['org_id']):
        org_id = meraki.get_org_id(meraki.params['org_name'])
    if (meraki.params['state'] == 'query'):
        admins = get_admins(meraki, org_id)
        if ((not meraki.params['name']) and (not meraki.params['email'])):
            meraki.result['data'] = admins
        if (meraki.params['name'] is not None):
            admin_id = get_admin_id(meraki, admins, name=meraki.params['name'])
            meraki.result['data'] = admin_id
            admin = get_admin(meraki, admins, admin_id)
            meraki.result['data'] = admin
        elif (meraki.params['email'] is not None):
            admin_id = get_admin_id(meraki, admins, email=meraki.params['email'])
            meraki.result['data'] = admin_id
            admin = get_admin(meraki, admins, admin_id)
            meraki.result['data'] = admin
    elif (meraki.params['state'] == 'present'):
        r = create_admin(meraki, org_id, meraki.params['name'], meraki.params['email'])
        if (r != (- 1)):
            meraki.result['data'] = r
    elif (meraki.params['state'] == 'absent'):
        admin_id = get_admin_id(meraki, get_admins(meraki, org_id), email=meraki.params['email'])
        r = delete_admin(meraki, org_id, admin_id)
        if (r != (- 1)):
            meraki.result['data'] = r
            meraki.result['changed'] = True
    meraki.exit_json(**meraki.result)