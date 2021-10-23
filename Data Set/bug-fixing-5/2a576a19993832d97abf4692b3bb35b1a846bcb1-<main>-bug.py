def main():
    argument_spec = f5_argument_spec()
    argument_spec.update(dict(state=dict(type='str', default='present', choices=['present', 'absent', 'disabled', 'enabled']), name=dict(type='str', required=True, aliases=['vs']), destination=dict(type='str', aliases=['address', 'ip']), port=dict(type='int'), all_policies=dict(type='list'), all_profiles=dict(type='list'), all_rules=dict(type='list'), enabled_vlans=dict(type='list'), pool=dict(type='str'), description=dict(type='str'), snat=dict(type='str'), route_advertisement_state=dict(type='str', default='disabled', choices=['enabled', 'disabled']), default_persistence_profile=dict(type='str'), fallback_persistence_profile=dict(type='str')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not bigsuds_found):
        module.fail_json(msg='the python bigsuds module is required')
    if module.params['validate_certs']:
        import ssl
        if (not hasattr(ssl, 'SSLContext')):
            module.fail_json(msg='bigsuds does not support verifying certificates with python < 2.7.9.  Either update python or set validate_certs=False on the task')
    server = module.params['server']
    server_port = module.params['server_port']
    user = module.params['user']
    password = module.params['password']
    state = module.params['state']
    partition = module.params['partition']
    validate_certs = module.params['validate_certs']
    name = fq_name(partition, module.params['name'])
    destination = module.params['destination']
    port = module.params['port']
    all_profiles = fq_list_names(partition, module.params['all_profiles'])
    all_policies = fq_list_names(partition, module.params['all_policies'])
    all_rules = fq_list_names(partition, module.params['all_rules'])
    enabled_vlans = module.params['enabled_vlans']
    if ((enabled_vlans is None) or ('ALL' in enabled_vlans)):
        all_enabled_vlans = enabled_vlans
    else:
        all_enabled_vlans = fq_list_names(partition, enabled_vlans)
    pool = fq_name(partition, module.params['pool'])
    description = module.params['description']
    snat = module.params['snat']
    route_advertisement_state = module.params['route_advertisement_state']
    default_persistence_profile = fq_name(partition, module.params['default_persistence_profile'])
    fallback_persistence_profile = module.params['fallback_persistence_profile']
    if (1 > port > 65535):
        module.fail_json(msg='valid ports must be in range 1 - 65535')
    try:
        api = bigip_api(server, user, password, validate_certs, port=server_port)
        result = {
            'changed': False,
        }
        if (state == 'absent'):
            if (not module.check_mode):
                if vs_exists(api, name):
                    try:
                        vs_remove(api, name)
                        result = {
                            'changed': True,
                            'deleted': name,
                        }
                    except bigsuds.OperationFailed as e:
                        if ('was not found' in str(e)):
                            result['changed'] = False
                        else:
                            raise
            else:
                result = {
                    'changed': True,
                }
        else:
            update = False
            if (not vs_exists(api, name)):
                if ((not destination) or (not port)):
                    module.fail_json(msg='both destination and port must be supplied to create a VS')
                if (not module.check_mode):
                    try:
                        vs_create(api, name, destination, port, pool)
                        set_profiles(api, name, all_profiles)
                        set_policies(api, name, all_policies)
                        set_enabled_vlans(api, name, all_enabled_vlans)
                        set_rules(api, name, all_rules)
                        set_snat(api, name, snat)
                        set_description(api, name, description)
                        set_default_persistence_profiles(api, name, default_persistence_profile)
                        set_fallback_persistence_profile(api, partition, name, fallback_persistence_profile)
                        set_state(api, name, state)
                        set_route_advertisement_state(api, destination, partition, route_advertisement_state)
                        result = {
                            'changed': True,
                        }
                    except bigsuds.OperationFailed as e:
                        raise Exception(('Error on creating Virtual Server : %s' % e))
                else:
                    result = {
                        'changed': True,
                    }
            else:
                update = True
            if update:
                if (not module.check_mode):
                    try:
                        api.System.Session.start_transaction()
                        result['changed'] |= set_destination(api, name, fq_name(partition, destination))
                        result['changed'] |= set_port(api, name, port)
                        result['changed'] |= set_pool(api, name, pool)
                        result['changed'] |= set_description(api, name, description)
                        result['changed'] |= set_snat(api, name, snat)
                        result['changed'] |= set_profiles(api, name, all_profiles)
                        result['changed'] |= set_policies(api, name, all_policies)
                        result['changed'] |= set_enabled_vlans(api, name, all_enabled_vlans)
                        result['changed'] |= set_rules(api, name, all_rules)
                        result['changed'] |= set_default_persistence_profiles(api, name, default_persistence_profile)
                        result['changed'] |= set_fallback_persistence_profile(api, partition, name, fallback_persistence_profile)
                        result['changed'] |= set_state(api, name, state)
                        result['changed'] |= set_route_advertisement_state(api, destination, partition, route_advertisement_state)
                        api.System.Session.submit_transaction()
                    except Exception as e:
                        raise Exception(('Error on updating Virtual Server : %s' % e))
                else:
                    result = {
                        'changed': True,
                    }
    except Exception as e:
        module.fail_json(msg=('received exception: %s' % e))
    module.exit_json(**result)