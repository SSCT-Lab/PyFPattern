def main():
    ' Module main '
    argument_spec = dict(state=dict(choices=['present', 'absent'], default='present'), local_user_name=dict(type='str'), local_password=dict(type='str', no_log=True), local_service_type=dict(type='str'), local_ftp_dir=dict(type='str'), local_user_level=dict(type='str'), local_user_group=dict(type='str'), radius_group_name=dict(type='str'), radius_server_type=dict(choices=['Authentication', 'Accounting']), radius_server_ip=dict(type='str'), radius_server_ipv6=dict(type='str'), radius_server_port=dict(type='str'), radius_server_mode=dict(choices=['Secondary-server', 'Primary-server']), radius_vpn_name=dict(type='str'), radius_server_name=dict(type='str'), hwtacacs_template=dict(type='str'), hwtacacs_server_ip=dict(type='str'), hwtacacs_server_ipv6=dict(type='str'), hwtacacs_server_type=dict(choices=['Authentication', 'Authorization', 'Accounting', 'Common']), hwtacacs_is_secondary_server=dict(required=False, default=False, type='bool'), hwtacacs_vpn_name=dict(type='str'), hwtacacs_is_public_net=dict(required=False, default=False, type='bool'), hwtacacs_server_host_name=dict(type='str'))
    argument_spec.update(ce_argument_spec)
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    check_module_argument(module=module)
    changed = False
    proposed = dict()
    existing = dict()
    end_state = dict()
    updates = []
    state = module.params['state']
    local_user_name = module.params['local_user_name']
    local_password = module.params['local_password']
    local_service_type = module.params['local_service_type']
    local_ftp_dir = module.params['local_ftp_dir']
    local_user_level = module.params['local_user_level']
    local_user_group = module.params['local_user_group']
    radius_group_name = module.params['radius_group_name']
    radius_server_type = module.params['radius_server_type']
    radius_server_ip = module.params['radius_server_ip']
    radius_server_ipv6 = module.params['radius_server_ipv6']
    radius_server_port = module.params['radius_server_port']
    radius_server_mode = module.params['radius_server_mode']
    radius_vpn_name = module.params['radius_vpn_name']
    radius_server_name = module.params['radius_server_name']
    hwtacacs_template = module.params['hwtacacs_template']
    hwtacacs_server_ip = module.params['hwtacacs_server_ip']
    hwtacacs_server_ipv6 = module.params['hwtacacs_server_ipv6']
    hwtacacs_server_type = module.params['hwtacacs_server_type']
    hwtacacs_is_secondary_server = module.params['hwtacacs_is_secondary_server']
    hwtacacs_vpn_name = module.params['hwtacacs_vpn_name']
    hwtacacs_is_public_net = module.params['hwtacacs_is_public_net']
    hwtacacs_server_host_name = module.params['hwtacacs_server_host_name']
    ce_aaa_server_host = AaaServerHost()
    if (not ce_aaa_server_host):
        module.fail_json(msg='Error: Construct ce_aaa_server failed.')
    proposed['state'] = state
    if local_user_name:
        proposed['local_user_name'] = local_user_name
    if local_password:
        proposed['local_password'] = '******'
    if local_service_type:
        proposed['local_service_type'] = local_service_type
    if local_ftp_dir:
        proposed['local_ftp_dir'] = local_ftp_dir
    if local_user_level:
        proposed['local_user_level'] = local_user_level
    if local_user_group:
        proposed['local_user_group'] = local_user_group
    if radius_group_name:
        proposed['radius_group_name'] = radius_group_name
    if radius_server_type:
        proposed['radius_server_type'] = radius_server_type
    if radius_server_ip:
        proposed['radius_server_ip'] = radius_server_ip
    if radius_server_ipv6:
        proposed['radius_server_ipv6'] = radius_server_ipv6
    if radius_server_port:
        proposed['radius_server_port'] = radius_server_port
    if radius_server_mode:
        proposed['radius_server_mode'] = radius_server_mode
    if radius_vpn_name:
        proposed['radius_vpn_name'] = radius_vpn_name
    if radius_server_name:
        proposed['radius_server_name'] = radius_server_name
    if hwtacacs_template:
        proposed['hwtacacs_template'] = hwtacacs_template
    if hwtacacs_server_ip:
        proposed['hwtacacs_server_ip'] = hwtacacs_server_ip
    if hwtacacs_server_ipv6:
        proposed['hwtacacs_server_ipv6'] = hwtacacs_server_ipv6
    if hwtacacs_server_type:
        proposed['hwtacacs_server_type'] = hwtacacs_server_type
    proposed['hwtacacs_is_secondary_server'] = hwtacacs_is_secondary_server
    if hwtacacs_vpn_name:
        proposed['hwtacacs_vpn_name'] = hwtacacs_vpn_name
    proposed['hwtacacs_is_public_net'] = hwtacacs_is_public_net
    if hwtacacs_server_host_name:
        proposed['hwtacacs_server_host_name'] = hwtacacs_server_host_name
    if local_user_name:
        if ((state == 'present') and (not local_password)):
            module.fail_json(msg='Error: Please input local_password when config local user.')
        local_user_result = ce_aaa_server_host.get_local_user_info(module=module)
        existing['local user name'] = local_user_result['local_user_info']
        if (state == 'present'):
            if local_user_result['need_cfg']:
                cmd = ce_aaa_server_host.merge_local_user_info(module=module)
                changed = True
                updates.append(cmd)
        elif local_user_result['need_cfg']:
            if ((not local_service_type) and (not local_ftp_dir) and (not local_user_level) and (not local_user_group)):
                cmd = ce_aaa_server_host.delete_local_user_info(module=module)
            else:
                cmd = ce_aaa_server_host.merge_local_user_info(module=module)
            changed = True
            updates.append(cmd)
        local_user_result = ce_aaa_server_host.get_local_user_info(module=module)
        end_state['local user name'] = local_user_result['local_user_info']
    if radius_group_name:
        if ((not radius_server_ip) and (not radius_server_ipv6) and (not radius_server_name)):
            module.fail_json(msg='Error: Please input radius_server_ip or radius_server_ipv6 or radius_server_name.')
        if (radius_server_ip and radius_server_ipv6):
            module.fail_json(msg='Error: Please do not input radius_server_ip and radius_server_ipv6 at the same time.')
        if ((not radius_server_type) or (not radius_server_port) or (not radius_server_mode) or (not radius_vpn_name)):
            module.fail_json(msg='Error: Please input radius_server_type radius_server_port radius_server_mode radius_vpn_name.')
        if radius_server_ip:
            rds_server_ipv4_result = ce_aaa_server_host.get_radius_server_cfg_ipv4(module=module)
        if radius_server_ipv6:
            rds_server_ipv6_result = ce_aaa_server_host.get_radius_server_cfg_ipv6(module=module)
        if radius_server_name:
            rds_server_name_result = ce_aaa_server_host.get_radius_server_name(module=module)
        if (radius_server_ip and rds_server_ipv4_result['radius_server_ip_v4']):
            existing['radius server ipv4'] = rds_server_ipv4_result['radius_server_ip_v4']
        if (radius_server_ipv6 and rds_server_ipv6_result['radius_server_ip_v6']):
            existing['radius server ipv6'] = rds_server_ipv6_result['radius_server_ip_v6']
        if (radius_server_name and rds_server_name_result['radius_server_name_cfg']):
            existing['radius server name cfg'] = rds_server_name_result['radius_server_name_cfg']
        if (state == 'present'):
            if (radius_server_ip and rds_server_ipv4_result['need_cfg']):
                cmd = ce_aaa_server_host.merge_radius_server_cfg_ipv4(module=module)
                changed = True
                updates.append(cmd)
            if (radius_server_ipv6 and rds_server_ipv6_result['need_cfg']):
                cmd = ce_aaa_server_host.merge_radius_server_cfg_ipv6(module=module)
                changed = True
                updates.append(cmd)
            if (radius_server_name and rds_server_name_result['need_cfg']):
                cmd = ce_aaa_server_host.merge_radius_server_name(module=module)
                changed = True
                updates.append(cmd)
        else:
            if (radius_server_ip and rds_server_ipv4_result['need_cfg']):
                cmd = ce_aaa_server_host.delete_radius_server_cfg_ipv4(module=module)
                changed = True
                updates.append(cmd)
            if (radius_server_ipv6 and rds_server_ipv6_result['need_cfg']):
                cmd = ce_aaa_server_host.delete_radius_server_cfg_ipv6(module=module)
                changed = True
                updates.append(cmd)
            if (radius_server_name and rds_server_name_result['need_cfg']):
                cmd = ce_aaa_server_host.delete_radius_server_name(module=module)
                changed = True
                updates.append(cmd)
        if radius_server_ip:
            rds_server_ipv4_result = ce_aaa_server_host.get_radius_server_cfg_ipv4(module=module)
        if radius_server_ipv6:
            rds_server_ipv6_result = ce_aaa_server_host.get_radius_server_cfg_ipv6(module=module)
        if radius_server_name:
            rds_server_name_result = ce_aaa_server_host.get_radius_server_name(module=module)
        if (radius_server_ip and rds_server_ipv4_result['radius_server_ip_v4']):
            end_state['radius server ipv4'] = rds_server_ipv4_result['radius_server_ip_v4']
        if (radius_server_ipv6 and rds_server_ipv6_result['radius_server_ip_v6']):
            end_state['radius server ipv6'] = rds_server_ipv6_result['radius_server_ip_v6']
        if (radius_server_name and rds_server_name_result['radius_server_name_cfg']):
            end_state['radius server name cfg'] = rds_server_name_result['radius_server_name_cfg']
    if hwtacacs_template:
        if ((not hwtacacs_server_ip) and (not hwtacacs_server_ipv6) and (not hwtacacs_server_host_name)):
            module.fail_json(msg='Error: Please input hwtacacs_server_ip or hwtacacs_server_ipv6 or hwtacacs_server_host_name.')
        if ((not hwtacacs_server_type) or (not hwtacacs_vpn_name)):
            module.fail_json(msg='Error: Please input hwtacacs_server_type hwtacacs_vpn_name.')
        if (hwtacacs_server_ip and hwtacacs_server_ipv6):
            module.fail_json(msg='Error: Please do not set hwtacacs_server_ip and hwtacacs_server_ipv6 at the same time.')
        if (hwtacacs_vpn_name and (hwtacacs_vpn_name != '_public_')):
            if hwtacacs_is_public_net:
                module.fail_json(msg='Error: Please do not set vpn and public net at the same time.')
        if hwtacacs_server_ip:
            hwtacacs_server_ipv4_result = ce_aaa_server_host.get_hwtacacs_server_cfg_ipv4(module=module)
        if hwtacacs_server_ipv6:
            hwtacacs_server_ipv6_result = ce_aaa_server_host.get_hwtacacs_server_cfg_ipv6(module=module)
        if hwtacacs_server_host_name:
            hwtacacs_host_name_result = ce_aaa_server_host.get_hwtacacs_host_server_cfg(module=module)
        if (hwtacacs_server_ip and hwtacacs_server_ipv4_result['hwtacacs_server_cfg_ipv4']):
            existing['hwtacacs server cfg ipv4'] = hwtacacs_server_ipv4_result['hwtacacs_server_cfg_ipv4']
        if (hwtacacs_server_ipv6 and hwtacacs_server_ipv6_result['hwtacacs_server_cfg_ipv6']):
            existing['hwtacacs server cfg ipv6'] = hwtacacs_server_ipv6_result['hwtacacs_server_cfg_ipv6']
        if (hwtacacs_server_host_name and hwtacacs_host_name_result['hwtacacs_server_name_cfg']):
            existing['hwtacacs server name cfg'] = hwtacacs_host_name_result['hwtacacs_server_name_cfg']
        if (state == 'present'):
            if (hwtacacs_server_ip and hwtacacs_server_ipv4_result['need_cfg']):
                cmd = ce_aaa_server_host.merge_hwtacacs_server_cfg_ipv4(module=module)
                changed = True
                updates.append(cmd)
            if (hwtacacs_server_ipv6 and hwtacacs_server_ipv6_result['need_cfg']):
                cmd = ce_aaa_server_host.merge_hwtacacs_server_cfg_ipv6(module=module)
                changed = True
                updates.append(cmd)
            if (hwtacacs_server_host_name and hwtacacs_host_name_result['need_cfg']):
                cmd = ce_aaa_server_host.merge_hwtacacs_host_server_cfg(module=module)
                changed = True
                updates.append(cmd)
        else:
            if (hwtacacs_server_ip and hwtacacs_server_ipv4_result['need_cfg']):
                cmd = ce_aaa_server_host.delete_hwtacacs_server_cfg_ipv4(module=module)
                changed = True
                updates.append(cmd)
            if (hwtacacs_server_ipv6 and hwtacacs_server_ipv6_result['need_cfg']):
                cmd = ce_aaa_server_host.delete_hwtacacs_server_cfg_ipv6(module=module)
                changed = True
                updates.append(cmd)
            if (hwtacacs_server_host_name and hwtacacs_host_name_result['need_cfg']):
                cmd = ce_aaa_server_host.delete_hwtacacs_host_server_cfg(module=module)
                changed = True
                updates.append(cmd)
        if hwtacacs_server_ip:
            hwtacacs_server_ipv4_result = ce_aaa_server_host.get_hwtacacs_server_cfg_ipv4(module=module)
        if hwtacacs_server_ipv6:
            hwtacacs_server_ipv6_result = ce_aaa_server_host.get_hwtacacs_server_cfg_ipv6(module=module)
        if hwtacacs_server_host_name:
            hwtacacs_host_name_result = ce_aaa_server_host.get_hwtacacs_host_server_cfg(module=module)
        if (hwtacacs_server_ip and hwtacacs_server_ipv4_result['hwtacacs_server_cfg_ipv4']):
            end_state['hwtacacs server cfg ipv4'] = hwtacacs_server_ipv4_result['hwtacacs_server_cfg_ipv4']
        if (hwtacacs_server_ipv6 and hwtacacs_server_ipv6_result['hwtacacs_server_cfg_ipv6']):
            end_state['hwtacacs server cfg ipv6'] = hwtacacs_server_ipv6_result['hwtacacs_server_cfg_ipv6']
        if (hwtacacs_server_host_name and hwtacacs_host_name_result['hwtacacs_server_name_cfg']):
            end_state['hwtacacs server name cfg'] = hwtacacs_host_name_result['hwtacacs_server_name_cfg']
    results = dict()
    results['proposed'] = proposed
    results['existing'] = existing
    results['changed'] = changed
    results['end_state'] = end_state
    results['updates'] = updates
    module.exit_json(**results)