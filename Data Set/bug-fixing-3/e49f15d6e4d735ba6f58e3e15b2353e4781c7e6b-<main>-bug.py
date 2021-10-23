def main():
    argument_spec = ec2_argument_spec()
    argument_spec.update(dict(state=dict(choices=['present', 'absent'], default='present'), ip_address=dict(), port=dict(type='int'), type=dict(required=True, choices=['HTTP', 'HTTPS', 'HTTP_STR_MATCH', 'HTTPS_STR_MATCH', 'TCP']), resource_path=dict(), fqdn=dict(), string_match=dict(), request_interval=dict(type='int', choices=[10, 30], default=30), failure_threshold=dict(type='int', choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], default=3)))
    module = AnsibleModule(argument_spec=argument_spec)
    if (not HAS_BOTO):
        module.fail_json(msg='boto 2.27.0+ required for this module')
    state_in = module.params.get('state')
    ip_addr_in = module.params.get('ip_address')
    port_in = module.params.get('port')
    type_in = module.params.get('type')
    resource_path_in = module.params.get('resource_path')
    fqdn_in = module.params.get('fqdn')
    string_match_in = module.params.get('string_match')
    request_interval_in = module.params.get('request_interval')
    failure_threshold_in = module.params.get('failure_threshold')
    if ((ip_addr_in is None) and (fqdn_in is None)):
        module.fail_json(msg="parameter 'ip_address' or 'fqdn' is required")
    if (port_in is None):
        if (type_in in ['HTTP', 'HTTP_STR_MATCH']):
            port_in = 80
        elif (type_in in ['HTTPS', 'HTTPS_STR_MATCH']):
            port_in = 443
        else:
            module.fail_json(msg="parameter 'port' is required for 'type' TCP")
    if (type_in in ['HTTP_STR_MATCH', 'HTTPS_STR_MATCH']):
        if (string_match_in is None):
            module.fail_json(msg="parameter 'string_match' is required for the HTTP(S)_STR_MATCH types")
        elif (len(string_match_in) > 255):
            module.fail_json(msg="parameter 'string_match' is limited to 255 characters max")
    elif string_match_in:
        module.fail_json(msg="parameter 'string_match' argument is only for the HTTP(S)_STR_MATCH types")
    (region, ec2_url, aws_connect_kwargs) = get_aws_connection_info(module)
    try:
        conn = Route53Connection(**aws_connect_kwargs)
    except boto.exception.BotoServerError as e:
        module.fail_json(msg=e.error_message)
    changed = False
    action = None
    check_id = None
    wanted_config = HealthCheck(ip_addr_in, port_in, type_in, resource_path_in, fqdn_in, string_match_in, request_interval_in, failure_threshold_in)
    existing_check = find_health_check(conn, wanted_config)
    if existing_check:
        check_id = existing_check.Id
        existing_config = to_health_check(existing_check.HealthCheckConfig)
    if (state_in == 'present'):
        if (existing_check is None):
            action = 'create'
            check_id = create_health_check(conn, wanted_config).HealthCheck.Id
            changed = True
        else:
            diff = health_check_diff(existing_config, wanted_config)
            if (not diff):
                action = 'update'
                update_health_check(conn, existing_check.Id, int(existing_check.HealthCheckVersion), wanted_config)
                changed = True
    elif (state_in == 'absent'):
        if check_id:
            action = 'delete'
            conn.delete_health_check(check_id)
            changed = True
    else:
        module.fail_json(msg='Logic Error: Unknown state')
    module.exit_json(changed=changed, health_check=dict(id=check_id), action=action)