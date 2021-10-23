

def main():
    module = AnsibleModule(argument_spec=dict(host=dict(type='str', default='127.0.0.1'), port=dict(type='int'), username=dict(type='str', default='cobbler'), password=dict(type='str', no_log=True), use_ssl=dict(type='bool', default=True), validate_certs=dict(type='bool', default=True), name=dict(type='str'), interfaces=dict(type='dict'), properties=dict(type='dict'), sync=dict(type='bool', default=False), state=dict(type='str', default='present', choices=['absent', 'present', 'query'])), supports_check_mode=True)
    username = module.params['username']
    password = module.params['password']
    port = module.params['port']
    use_ssl = module.params['use_ssl']
    validate_certs = module.params['validate_certs']
    name = module.params['name']
    state = module.params['state']
    module.params['proto'] = ('https' if use_ssl else 'http')
    if (not port):
        module.params['port'] = ('443' if use_ssl else '80')
    result = dict(changed=False)
    start = datetime.datetime.utcnow()
    ssl_context = None
    if (not validate_certs):
        try:
            ssl_context = ssl.create_unverified_context()
        except AttributeError:
            ssl._create_default_context = ssl._create_unverified_context
        else:
            ssl._create_default_https_context = ssl._create_unverified_https_context
    url = '{proto}://{host}:{port}/cobbler_api'.format(**module.params)
    if ssl_context:
        conn = xmlrpc_client.ServerProxy(url, context=ssl_context)
    else:
        conn = xmlrpc_client.Server(url)
    try:
        token = conn.login(username, password)
    except xmlrpc_client.Fault as e:
        module.fail_json(msg="Failed to log in to Cobbler '{url}' as '{username}'. {error}".format(url=url, error=to_text(e), **module.params))
    except Exception as e:
        module.fail_json(msg="Connection to '{url}' failed. {error}".format(url=url, error=to_text(e), **module.params))
    system = getsystem(conn, name, token)
    if (state == 'query'):
        if name:
            result['system'] = system
        else:
            result['systems'] = conn.get_systems()
    elif (state == 'present'):
        if system:
            system_id = conn.get_system_handle(name, token)
            for (key, value) in iteritems(module.params['properties']):
                if (key not in system):
                    module.warn("Property '{0}' is not a valid system property.".format(key))
                if (system[key] != value):
                    try:
                        conn.modify_system(system_id, key, value, token)
                        result['changed'] = True
                    except Exception as e:
                        module.fail_json(msg="Unable to change '{0}' to '{1}'. {2}".format(key, value, e))
        else:
            system_id = conn.new_system(token)
            conn.modify_system(system_id, 'name', name, token)
            result['changed'] = True
            if module.params['properties']:
                for (key, value) in iteritems(module.params['properties']):
                    try:
                        conn.modify_system(system_id, key, value, token)
                    except Exception as e:
                        module.fail_json(msg="Unable to change '{0}' to '{1}'. {2}".format(key, value, e))
        interface_properties = dict()
        if module.params['interfaces']:
            for (device, values) in iteritems(module.params['interfaces']):
                for (key, value) in iteritems(values):
                    if (key == 'name'):
                        continue
                    if (key not in IFPROPS_MAPPING):
                        module.warn("Property '{0}' is not a valid system property.".format(key))
                    if ((not system) or (system['interfaces'][device][IFPROPS_MAPPING[key]] != value)):
                        result['changed'] = True
                    interface_properties['{0}-{1}'.format(key, device)] = value
            if (result['changed'] is True):
                conn.modify_system(system_id, 'modify_interface', interface_properties, token)
        if ((not module.check_mode) and result['changed']):
            conn.save_system(system_id, token)
    elif (state == 'absent'):
        if system:
            if (not module.check_mode):
                conn.remove_system(name, token)
            result['changed'] = True
    if ((not module.check_mode) and module.params['sync'] and result['changed']):
        try:
            conn.sync(token)
        except Exception as e:
            module.fail_json(msg='Failed to sync Cobbler. {0}'.format(to_text(e)))
    if (state in ('absent', 'present')):
        result['system'] = getsystem(conn, name, token)
        if module._diff:
            result['diff'] = dict(before=system, after=result['system'])
    elapsed = (datetime.datetime.utcnow() - start)
    module.exit_json(elapsed=elapsed.seconds, **result)
