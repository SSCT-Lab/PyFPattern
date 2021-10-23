def main():
    module = AnsibleModule(argument_spec=dict(state=dict(default='present', choices=['present', 'absent'], type='str'), name=dict(required=True, aliases=['src', 'source'], type='str'), login_user=dict(default='guest', type='str'), login_password=dict(default='guest', type='str', no_log=True), login_host=dict(default='localhost', type='str'), login_port=dict(default='15672', type='str'), vhost=dict(default='/', type='str'), destination=dict(required=True, aliases=['dst', 'dest'], type='str'), destination_type=dict(required=True, aliases=['type', 'dest_type'], choices=['queue', 'exchange'], type='str'), routing_key=dict(default='#', type='str'), arguments=dict(default=dict(), type='dict')), supports_check_mode=True)
    if (not HAS_REQUESTS):
        module.fail_json(msg='requests library is required for this module. To install, use `pip install requests`')
    result = dict(changed=False, name=module.params['name'])
    if (module.params['destination_type'] == 'queue'):
        dest_type = 'q'
    else:
        dest_type = 'e'
    if (module.params['routing_key'] == ''):
        props = '~'
    else:
        props = urllib_parse.quote(module.params['routing_key'], '')
    base_url = ('http://%s:%s/api/bindings' % (module.params['login_host'], module.params['login_port']))
    url = ('%s/%s/e/%s/%s/%s/%s' % (base_url, urllib_parse.quote(module.params['vhost'], ''), urllib_parse.quote(module.params['name'], ''), dest_type, urllib_parse.quote(module.params['destination'], ''), props))
    r = requests.get(url, auth=(module.params['login_user'], module.params['login_password']))
    if (r.status_code == 200):
        binding_exists = True
        response = r.json()
    elif (r.status_code == 404):
        binding_exists = False
        response = r.text
    else:
        module.fail_json(msg='Invalid response from RESTAPI when trying to check if exchange exists', details=r.text)
    if (module.params['state'] == 'present'):
        change_required = (not binding_exists)
    else:
        change_required = binding_exists
    if module.check_mode:
        result['changed'] = change_required
        result['details'] = response
        result['arguments'] = module.params['arguments']
        module.exit_json(**result)
    if change_required:
        if (module.params['state'] == 'present'):
            url = ('%s/%s/e/%s/%s/%s' % (base_url, urllib_parse.quote(module.params['vhost'], ''), urllib_parse.quote(module.params['name'], ''), dest_type, urllib_parse.quote(module.params['destination'], '')))
            r = requests.post(url, auth=(module.params['login_user'], module.params['login_password']), headers={
                'content-type': 'application/json',
            }, data=json.dumps({
                'routing_key': module.params['routing_key'],
                'arguments': module.params['arguments'],
            }))
        elif (module.params['state'] == 'absent'):
            r = requests.delete(url, auth=(module.params['login_user'], module.params['login_password']))
        if ((r.status_code == 204) or (r.status_code == 201)):
            result['changed'] = True
            result['destination'] = module.params['destination']
            module.exit_json(**result)
        else:
            module.fail_json(msg='Error creating exchange', status=r.status_code, details=r.text)
    else:
        result['changed'] = False
        module.exit_json(**result)