def main():
    argument_spec = f5_argument_spec
    meta_args = dict(session=dict(type='bool', default='no'), include=dict(type='raw', required=True, choices=['address_class', 'certificate', 'client_ssl_profile', 'device', 'device_group', 'interface', 'key', 'node', 'pool', 'provision', 'rule', 'self_ip', 'software', 'system_info', 'traffic_group', 'trunk', 'virtual_address', 'virtual_server', 'vlan']), filter=dict(type='str'))
    argument_spec.update(meta_args)
    module = AnsibleModule(argument_spec=argument_spec)
    if (not bigsuds_found):
        module.fail_json(msg='the python suds and bigsuds modules are required')
    server = module.params['server']
    server_port = module.params['server_port']
    user = module.params['user']
    password = module.params['password']
    validate_certs = module.params['validate_certs']
    session = module.params['session']
    fact_filter = module.params['filter']
    if validate_certs:
        import ssl
        if (not hasattr(ssl, 'SSLContext')):
            module.fail_json(msg='bigsuds does not support verifying certificates with python < 2.7.9.  Either update python or set validate_certs=False on the task')
    if fact_filter:
        regex = fnmatch.translate(fact_filter)
    else:
        regex = None
    if isinstance(module.params['include'], string_types):
        includes = module.params['include'].split(',')
    else:
        includes = module.params['include']
    include = [x.lower() for x in includes]
    valid_includes = ('address_class', 'certificate', 'client_ssl_profile', 'device', 'device_group', 'interface', 'key', 'node', 'pool', 'provision', 'rule', 'self_ip', 'software', 'system_info', 'traffic_group', 'trunk', 'virtual_address', 'virtual_server', 'vlan')
    include_test = ((x in valid_includes) for x in include)
    if (not all(include_test)):
        module.fail_json(msg=('Value of include must be one or more of: %s, got: %s' % (','.join(valid_includes), ','.join(include))))
    try:
        facts = {
            
        }
        if (len(include) > 0):
            f5 = F5(server, user, password, session, validate_certs, server_port)
            saved_active_folder = f5.get_active_folder()
            saved_recursive_query_state = f5.get_recursive_query_state()
            if (saved_active_folder != '/'):
                f5.set_active_folder('/')
            if (saved_recursive_query_state != 'STATE_ENABLED'):
                f5.enable_recursive_query_state()
            if ('interface' in include):
                facts['interface'] = generate_interface_dict(f5, regex)
            if ('self_ip' in include):
                facts['self_ip'] = generate_self_ip_dict(f5, regex)
            if ('trunk' in include):
                facts['trunk'] = generate_trunk_dict(f5, regex)
            if ('vlan' in include):
                facts['vlan'] = generate_vlan_dict(f5, regex)
            if ('virtual_server' in include):
                facts['virtual_server'] = generate_vs_dict(f5, regex)
            if ('pool' in include):
                facts['pool'] = generate_pool_dict(f5, regex)
            if ('provision' in include):
                facts['provision'] = generate_provision_dict(f5)
            if ('device' in include):
                facts['device'] = generate_device_dict(f5, regex)
            if ('device_group' in include):
                facts['device_group'] = generate_device_group_dict(f5, regex)
            if ('traffic_group' in include):
                facts['traffic_group'] = generate_traffic_group_dict(f5, regex)
            if ('rule' in include):
                facts['rule'] = generate_rule_dict(f5, regex)
            if ('node' in include):
                facts['node'] = generate_node_dict(f5, regex)
            if ('virtual_address' in include):
                facts['virtual_address'] = generate_virtual_address_dict(f5, regex)
            if ('address_class' in include):
                facts['address_class'] = generate_address_class_dict(f5, regex)
            if ('software' in include):
                facts['software'] = generate_software_list(f5)
            if ('certificate' in include):
                facts['certificate'] = generate_certificate_dict(f5, regex)
            if ('key' in include):
                facts['key'] = generate_key_dict(f5, regex)
            if ('client_ssl_profile' in include):
                facts['client_ssl_profile'] = generate_client_ssl_profile_dict(f5, regex)
            if ('system_info' in include):
                facts['system_info'] = generate_system_info_dict(f5)
            if (saved_active_folder and (saved_active_folder != '/')):
                f5.set_active_folder(saved_active_folder)
            if (saved_recursive_query_state and (saved_recursive_query_state != 'STATE_ENABLED')):
                f5.set_recursive_query_state(saved_recursive_query_state)
        result = dict(ansible_facts=facts)
        result.update(**facts)
    except Exception as e:
        module.fail_json(msg=('received exception: %s\ntraceback: %s' % (e, traceback.format_exc())))
    module.exit_json(**result)