def run_module():
    module_args = dict(cpm_action=dict(choices=['getuser', 'adduser', 'edituser', 'deleteuser'], required=True), cpm_url=dict(type='str', required=True), cpm_username=dict(type='str', required=True), cpm_password=dict(type='str', required=True, no_log=True), user_name=dict(type='str', required=True), user_pass=dict(type='str', required=False, default=None, no_log=True), user_accesslevel=dict(type='int', required=False, default=None, choices=[0, 1, 2, 3]), user_accessssh=dict(type='int', required=False, default=None, choices=[0, 1]), user_accessserial=dict(type='int', required=False, default=None, choices=[0, 1]), user_accessweb=dict(type='int', required=False, default=None, choices=[0, 1]), user_accessapi=dict(type='int', required=False, default=None, choices=[0, 1]), user_accessmonitor=dict(type='int', required=False, default=None, choices=[0, 1]), user_accessoutbound=dict(type='int', required=False, default=None, choices=[0, 1]), user_portaccess=dict(type='str', required=False, default=None), user_plugaccess=dict(type='str', required=False, default=None), user_groupaccess=dict(type='str', required=False, default=None), user_callbackphone=dict(type='str', required=False, default=None), use_https=dict(type='bool', default=True), validate_certs=dict(type='bool', default=True), use_proxy=dict(type='bool', default=False))
    result = dict(changed=False, data='')
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    if module.check_mode:
        return result
    auth = to_text(base64.b64encode(to_bytes('{0}:{1}'.format(module.params['cpm_username'], module.params['cpm_password']), errors='surrogate_or_strict')))
    if (module.params['use_https'] is True):
        protocol = 'https://'
    else:
        protocol = 'http://'
    payload = None
    if (module.params['cpm_action'] == 'getuser'):
        fullurl = ('%s%s/api/v2/config/users?username=%s' % (protocol, module.params['cpm_url'], module.params['user_name']))
        method = 'GET'
    elif (module.params['cpm_action'] == 'adduser'):
        if ((module.params['user_pass'] is None) or (len(module.params['user_pass']) == 0)):
            module.fail_json(msg='user_pass not defined.', **result)
        payload = assemble_json(module)
        fullurl = ('%s%s/api/v2/config/users' % (protocol, module.params['cpm_url']))
        method = 'POST'
    elif (module.params['cpm_action'] == 'edituser'):
        payload = assemble_json(module)
        fullurl = ('%s%s/api/v2/config/users' % (protocol, module.params['cpm_url']))
        method = 'PUT'
    elif (module.params['cpm_action'] == 'deleteuser'):
        fullurl = ('%s%s/api/v2/config/users?username=%s' % (protocol, module.params['cpm_url'], module.params['user_name']))
        method = 'DELETE'
    try:
        response = open_url(fullurl, data=payload, method=method, validate_certs=module.params['validate_certs'], use_proxy=module.params['use_proxy'], headers={
            'Content-Type': 'application/json',
            'Authorization': ('Basic %s' % auth),
        })
        if (method != 'GET'):
            result['changed'] = True
    except HTTPError as e:
        fail_json = dict(msg='Received HTTP error for {0} : {1}'.format(fullurl, to_native(e)), changed=False)
        module.fail_json(**fail_json)
    except URLError as e:
        fail_json = dict(msg='Failed lookup url for {0} : {1}'.format(fullurl, to_native(e)), changed=False)
        module.fail_json(**fail_json)
    except SSLValidationError as e:
        fail_json = dict(msg='Error validating the servers certificate for {0} : {1}'.format(fullurl, to_native(e)), changed=False)
        module.fail_json(**fail_json)
    except ConnectionError as e:
        fail_json = dict(msg='Error connecting to  for {0} : {1}'.format(fullurl, to_native(e)), changed=False)
        module.fail_json(**fail_json)
    result['data'] = to_text(response.read())
    module.exit_json(**result)