def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(dhcp_options_id=dict(type='str', default=None), domain_name=dict(type='str', default=None), dns_servers=dict(type='list', default=None), ntp_servers=dict(type='list', default=None), netbios_name_servers=dict(type='list', default=None), netbios_node_type=dict(type='int', default=None), vpc_id=dict(type='str', default=None), delete_old=dict(type='bool', default=True), inherit_existing=dict(type='bool', default=False), tags=dict(type='dict', default=None, aliases=['resource_tags']), state=dict(type='str', default='present', choices=['present', 'absent'])))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    params = module.params
    found = False
    changed = False
    new_options = collections.defaultdict((lambda : None))
    (region, ec2_url, boto_params) = get_aws_connection_info(module)
    connection = connect_to_aws(boto.vpc, region, **boto_params)
    existing_options = None
    if (not params['dhcp_options_id']):
        if (params['dns_servers'] is not None):
            new_options['domain-name-servers'] = params['dns_servers']
        if (params['netbios_name_servers'] is not None):
            new_options['netbios-name-servers'] = params['netbios_name_servers']
        if (params['ntp_servers'] is not None):
            new_options['ntp-servers'] = params['ntp_servers']
        if (params['domain_name'] is not None):
            new_options['domain-name'] = [params['domain_name']]
        if (params['netbios_node_type'] is not None):
            new_options['netbios-node-type'] = [str(params['netbios_node_type'])]
        if params['vpc_id']:
            existing_options = fetch_dhcp_options_for_vpc(connection, params['vpc_id'])
            if params['inherit_existing']:
                if existing_options:
                    for option in ['domain-name-servers', 'netbios-name-servers', 'ntp-servers', 'domain-name', 'netbios-node-type']:
                        if (existing_options.options.get(option) and (new_options[option] != []) and ((not new_options[option]) or ([''] == new_options[option]))):
                            new_options[option] = existing_options.options.get(option)
            if (existing_options and (new_options == existing_options.options)):
                module.exit_json(changed=changed, new_options=new_options, dhcp_options_id=existing_options.id)
        (found, dhcp_option) = match_dhcp_options(connection, params['tags'], new_options)
    else:
        supplied_options = connection.get_all_dhcp_options(filters={
            'dhcp-options-id': params['dhcp_options_id'],
        })
        if (len(supplied_options) != 1):
            if (params['state'] != 'absent'):
                module.fail_json(msg=' a dhcp_options_id was supplied, but does not exist')
        else:
            found = True
            dhcp_option = supplied_options[0]
            if ((params['state'] != 'absent') and params['tags']):
                ensure_tags(connection, dhcp_option.id, params['tags'], False, module.check_mode)
    if (params['state'] == 'absent'):
        if (not module.check_mode):
            if found:
                changed = remove_dhcp_options_by_id(connection, dhcp_option.id)
        module.exit_json(changed=changed, new_options={
            
        })
    elif ((not module.check_mode) and (not found)):
        if (not found):
            if new_options['netbios-node-type']:
                new_options['netbios-node-type'] = new_options['netbios-node-type'][0]
            if new_options['domain-name']:
                new_options['domain-name'] = new_options['domain-name'][0]
            dhcp_option = connection.create_dhcp_options(new_options['domain-name'], new_options['domain-name-servers'], new_options['ntp-servers'], new_options['netbios-name-servers'], new_options['netbios-node-type'])
            changed = True
            if params['tags']:
                ensure_tags(connection, dhcp_option.id, params['tags'], False, module.check_mode)
    if (params['vpc_id'] and (not module.check_mode)):
        changed = True
        connection.associate_dhcp_options(dhcp_option.id, params['vpc_id'])
        if (params['delete_old'] and existing_options):
            remove_dhcp_options_by_id(connection, existing_options.id)
    module.exit_json(changed=changed, new_options=new_options, dhcp_options_id=dhcp_option.id)