def main():
    argument_spec = dict(adom=dict(required=False, type='str'), mode=dict(choices=['add', 'set', 'delete', 'update'], type='str', default='add'), provisioning_template=dict(required=False, type='str'), provision_targets=dict(required=False, type='str'), device_unique_name=dict(required=False, type='str'), snmp_status=dict(required=False, type='str', choices=['enable', 'disable']), snmp_v2c_query_port=dict(required=False, type='int'), snmp_v2c_trap_port=dict(required=False, type='int'), snmp_v2c_status=dict(required=False, type='str', choices=['enable', 'disable']), snmp_v2c_trap_status=dict(required=False, type='str', choices=['enable', 'disable']), snmp_v2c_query_status=dict(required=False, type='str', choices=['enable', 'disable']), snmp_v2c_name=dict(required=False, type='str', no_log=True), snmp_v2c_id=dict(required=False, type='int'), snmp_v2c_trap_src_ipv4=dict(required=False, type='str'), snmp_v2c_trap_hosts_ipv4=dict(required=False, type='str'), snmp_v2c_query_hosts_ipv4=dict(required=False, type='str'), snmpv3_auth_proto=dict(required=False, type='str', choices=['md5', 'sha']), snmpv3_auth_pwd=dict(required=False, type='str', no_log=True), snmpv3_name=dict(required=False, type='str'), snmpv3_notify_hosts=dict(required=False, type='str'), snmpv3_priv_proto=dict(required=False, type='str', choices=['aes', 'des', 'aes256', 'aes256cisco']), snmpv3_priv_pwd=dict(required=False, type='str', no_log=True), snmpv3_queries=dict(required=False, type='str', choices=['enable', 'disable']), snmpv3_query_port=dict(required=False, type='int'), snmpv3_security_level=dict(required=False, type='str', choices=['no-auth-no-priv', 'auth-no-priv', 'auth-priv']), snmpv3_source_ip=dict(required=False, type='str'), snmpv3_status=dict(required=False, type='str', choices=['enable', 'disable']), snmpv3_trap_rport=dict(required=False, type='int'), snmpv3_trap_status=dict(required=False, type='str', choices=['enable', 'disable']), syslog_port=dict(required=False, type='int'), syslog_server=dict(required=False, type='str'), syslog_mode=dict(required=False, type='str', choices=['udp', 'legacy-reliable', 'reliable'], default='udp'), syslog_status=dict(required=False, type='str', choices=['enable', 'disable']), syslog_filter=dict(required=False, type='str', choices=['emergency', 'alert', 'critical', 'error', 'warning', 'notification', 'information', 'debug']), syslog_enc_algorithm=dict(required=False, type='str', choices=['high', 'low', 'disable', 'high-medium'], default='disable'), syslog_facility=dict(required=False, type='str', choices=['kernel', 'user', 'mail', 'daemon', 'auth', 'syslog', 'lpr', 'news', 'uucp', 'cron', 'authpriv', 'ftp', 'ntp', 'audit', 'alert', 'clock', 'local0', 'local1', 'local2', 'local3', 'local4', 'local5', 'local6', 'local7'], default='syslog'), syslog_certificate=dict(required=False, type='str'), ntp_status=dict(required=False, type='str', choices=['enable', 'disable']), ntp_sync_interval=dict(required=False, type='int'), ntp_type=dict(required=False, type='str', choices=['fortiguard', 'custom']), ntp_server=dict(required=False, type='str'), ntp_auth=dict(required=False, type='str', choices=['enable', 'disable']), ntp_auth_pwd=dict(required=False, type='str', no_log=True), ntp_v3=dict(required=False, type='str', choices=['enable', 'disable']), admin_https_redirect=dict(required=False, type='str', choices=['enable', 'disable']), admin_https_port=dict(required=False, type='int'), admin_http_port=dict(required=False, type='int'), admin_timeout=dict(required=False, type='int'), admin_language=dict(required=False, type='str', choices=['english', 'simch', 'japanese', 'korean', 'spanish', 'trach', 'french', 'portuguese']), admin_switch_controller=dict(required=False, type='str', choices=['enable', 'disable']), admin_gui_theme=dict(required=False, type='str', choices=['green', 'red', 'blue', 'melongene', 'mariner']), admin_enable_fortiguard=dict(required=False, type='str', choices=['none', 'direct', 'this-fmg']), admin_fortianalyzer_target=dict(required=False, type='str'), admin_fortiguard_target=dict(required=False, type='str'), smtp_username=dict(required=False, type='str'), smtp_password=dict(required=False, type='str', no_log=True), smtp_port=dict(required=False, type='int'), smtp_replyto=dict(required=False, type='str'), smtp_conn_sec=dict(required=False, type='str', choices=['none', 'starttls', 'smtps']), smtp_server=dict(required=False, type='str'), smtp_source_ipv4=dict(required=False, type='str'), smtp_validate_cert=dict(required=False, type='str', choices=['enable', 'disable']), dns_suffix=dict(required=False, type='str'), dns_primary_ipv4=dict(required=False, type='str'), dns_secondary_ipv4=dict(required=False, type='str'), delete_provisioning_template=dict(required=False, type='str'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    paramgram = {
        'adom': module.params['adom'],
        'mode': module.params['mode'],
        'provision_targets': module.params['provision_targets'],
        'provisioning_template': module.params['provisioning_template'],
        'snmp_status': module.params['snmp_status'],
        'snmp_v2c_query_port': module.params['snmp_v2c_query_port'],
        'snmp_v2c_trap_port': module.params['snmp_v2c_trap_port'],
        'snmp_v2c_status': module.params['snmp_v2c_status'],
        'snmp_v2c_trap_status': module.params['snmp_v2c_trap_status'],
        'snmp_v2c_query_status': module.params['snmp_v2c_query_status'],
        'snmp_v2c_name': module.params['snmp_v2c_name'],
        'snmp_v2c_id': module.params['snmp_v2c_id'],
        'snmp_v2c_trap_src_ipv4': module.params['snmp_v2c_trap_src_ipv4'],
        'snmp_v2c_trap_hosts_ipv4': module.params['snmp_v2c_trap_hosts_ipv4'],
        'snmp_v2c_query_hosts_ipv4': module.params['snmp_v2c_query_hosts_ipv4'],
        'snmpv3_auth_proto': module.params['snmpv3_auth_proto'],
        'snmpv3_auth_pwd': module.params['snmpv3_auth_pwd'],
        'snmpv3_name': module.params['snmpv3_name'],
        'snmpv3_notify_hosts': module.params['snmpv3_notify_hosts'],
        'snmpv3_priv_proto': module.params['snmpv3_priv_proto'],
        'snmpv3_priv_pwd': module.params['snmpv3_priv_pwd'],
        'snmpv3_queries': module.params['snmpv3_queries'],
        'snmpv3_query_port': module.params['snmpv3_query_port'],
        'snmpv3_security_level': module.params['snmpv3_security_level'],
        'snmpv3_source_ip': module.params['snmpv3_source_ip'],
        'snmpv3_status': module.params['snmpv3_status'],
        'snmpv3_trap_rport': module.params['snmpv3_trap_rport'],
        'snmpv3_trap_status': module.params['snmpv3_trap_status'],
        'syslog_port': module.params['syslog_port'],
        'syslog_server': module.params['syslog_server'],
        'syslog_mode': module.params['syslog_mode'],
        'syslog_status': module.params['syslog_status'],
        'syslog_filter': module.params['syslog_filter'],
        'syslog_facility': module.params['syslog_facility'],
        'syslog_enc_algorithm': module.params['syslog_enc_algorithm'],
        'syslog_certificate': module.params['syslog_certificate'],
        'ntp_status': module.params['ntp_status'],
        'ntp_sync_interval': module.params['ntp_sync_interval'],
        'ntp_type': module.params['ntp_type'],
        'ntp_server': module.params['ntp_server'],
        'ntp_auth': module.params['ntp_auth'],
        'ntp_auth_pwd': module.params['ntp_auth_pwd'],
        'ntp_v3': module.params['ntp_v3'],
        'admin_https_redirect': module.params['admin_https_redirect'],
        'admin_https_port': module.params['admin_https_port'],
        'admin_http_port': module.params['admin_http_port'],
        'admin_timeout': module.params['admin_timeout'],
        'admin_language': module.params['admin_language'],
        'admin_switch_controller': module.params['admin_switch_controller'],
        'admin_gui_theme': module.params['admin_gui_theme'],
        'admin_enable_fortiguard': module.params['admin_enable_fortiguard'],
        'admin_fortianalyzer_target': module.params['admin_fortianalyzer_target'],
        'admin_fortiguard_target': module.params['admin_fortiguard_target'],
        'smtp_username': module.params['smtp_username'],
        'smtp_password': module.params['smtp_password'],
        'smtp_port': module.params['smtp_port'],
        'smtp_replyto': module.params['smtp_replyto'],
        'smtp_conn_sec': module.params['smtp_conn_sec'],
        'smtp_server': module.params['smtp_server'],
        'smtp_source_ipv4': module.params['smtp_source_ipv4'],
        'smtp_validate_cert': module.params['smtp_validate_cert'],
        'dns_suffix': module.params['dns_suffix'],
        'dns_primary_ipv4': module.params['dns_primary_ipv4'],
        'dns_secondary_ipv4': module.params['dns_secondary_ipv4'],
        'delete_provisioning_template': module.params['delete_provisioning_template'],
    }
    module.paramgram = paramgram
    fmgr = None
    if module._socket_path:
        connection = Connection(module._socket_path)
        fmgr = FortiManagerHandler(connection, module)
        fmgr.tools = FMGRCommon()
    else:
        module.fail_json(**FAIL_SOCKET_MSG)
    results = DEFAULT_RESULT_OBJ
    try:
        if (paramgram['delete_provisioning_template'] is not None):
            results = set_devprof(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results, good_codes=[0, (- 10), (- 1)], ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram), stop_on_success=True)
    except Exception as err:
        raise FMGBaseException(err)
    try:
        devprof = get_devprof(fmgr, paramgram)
        if (devprof[0] != 0):
            results = set_devprof(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results, good_codes=[0, (- 2)], stop_on_success=False, ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))
    except Exception as err:
        raise FMGBaseException(err)
    try:
        if (paramgram['snmp_status'] is not None):
            results = set_devprof_snmp(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results, good_codes=[0], stop_on_success=False, ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))
        if all(((v is not None) for v in (paramgram['snmp_v2c_query_port'], paramgram['snmp_v2c_trap_port'], paramgram['snmp_v2c_status'], paramgram['snmp_v2c_trap_status'], paramgram['snmp_v2c_query_status'], paramgram['snmp_v2c_name'], paramgram['snmp_v2c_id']))):
            results = set_devprof_snmp_v2c(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results, good_codes=[0, (- 10033)], stop_on_success=True, ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))
        if all(((v is not None) for v in [paramgram['snmpv3_auth_proto'], paramgram['snmpv3_auth_pwd'], paramgram['snmpv3_name'], paramgram['snmpv3_notify_hosts'], paramgram['snmpv3_priv_proto'], paramgram['snmpv3_priv_pwd'], paramgram['snmpv3_queries'], paramgram['snmpv3_query_port'], paramgram['snmpv3_security_level'], paramgram['snmpv3_source_ip'], paramgram['snmpv3_status'], paramgram['snmpv3_trap_rport'], paramgram['snmpv3_trap_status']])):
            results = set_devprof_snmp_v3(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results, good_codes=[0, (- 10033), (- 10000), (- 3)], stop_on_success=True, ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))
    except Exception as err:
        raise FMGBaseException(err)
    try:
        if all(((v is not None) for v in [paramgram['syslog_port'], paramgram['syslog_mode'], paramgram['syslog_server'], paramgram['syslog_status']])):
            results = set_devprof_syslog(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results, good_codes=[0, (- 10033), (- 10000), (- 3)], ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))
    except Exception as err:
        raise FMGBaseException(err)
    try:
        if (paramgram['syslog_filter'] is not None):
            results = set_devprof_syslog_filter(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results, good_codes=[0], ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))
    except Exception as err:
        raise FMGBaseException(err)
    try:
        if paramgram['ntp_status']:
            if ((paramgram['ntp_type'] == 'custom') and (paramgram['ntp_server'] is None)):
                module.exit_json(msg='You requested custom NTP type but did not provide ntp_server parameter.')
            if ((paramgram['ntp_auth'] == 'enable') and (paramgram['ntp_auth_pwd'] is None)):
                module.exit_json(msg='You requested NTP Authentication but did not provide ntp_auth_pwd parameter.')
            results = set_devprof_ntp(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results, good_codes=[0], ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))
    except Exception as err:
        raise FMGBaseException(err)
    try:
        if any(((v is not None) for v in (paramgram['admin_https_redirect'], paramgram['admin_https_port'], paramgram['admin_http_port'], paramgram['admin_timeout'], paramgram['admin_language'], paramgram['admin_switch_controller'], paramgram['admin_gui_theme']))):
            results = set_devprof_admin(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results, good_codes=[0], stop_on_success=False, ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))
    except Exception as err:
        raise FMGBaseException(err)
    try:
        if (paramgram['admin_enable_fortiguard'] is not None):
            results = set_devprof_toggle_fg(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results, good_codes=[0], stop_on_success=False, ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))
            results = set_devprof_fg(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results, good_codes=[0], stop_on_success=False, ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))
    except Exception as err:
        raise FMGBaseException(err)
    try:
        if all(((v is not None) for v in (paramgram['smtp_username'], paramgram['smtp_password'], paramgram['smtp_port'], paramgram['smtp_replyto'], paramgram['smtp_conn_sec'], paramgram['smtp_server'], paramgram['smtp_source_ipv4'], paramgram['smtp_validate_cert']))):
            results = set_devprof_smtp(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results, good_codes=[0], stop_on_success=False, ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))
    except Exception as err:
        raise FMGBaseException(err)
    try:
        if any(((v is not None) for v in (paramgram['dns_suffix'], paramgram['dns_primary_ipv4'], paramgram['dns_secondary_ipv4']))):
            results = set_devprof_dns(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results, good_codes=[0], stop_on_success=False, ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))
    except Exception as err:
        raise FMGBaseException(err)
    try:
        if (paramgram['admin_fortianalyzer_target'] is not None):
            results = set_devprof_faz(fmgr, paramgram)
            fmgr.govern_response(module=module, results=results, good_codes=[0], stop_on_success=False, ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))
    except Exception as err:
        raise FMGBaseException(err)
    try:
        if (paramgram['provision_targets'] is not None):
            if (paramgram['mode'] != 'delete'):
                results = set_devprof_scope(fmgr, paramgram)
                fmgr.govern_response(module=module, results=results, good_codes=[0], stop_on_success=False, ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))
            if (paramgram['mode'] == 'delete'):
                targets_to_add = list()
                try:
                    current_scope = get_devprof_scope(fmgr, paramgram)
                    targets_to_remove = paramgram['provision_targets'].strip().split(',')
                    targets = current_scope[1][1]['scope member']
                    for target in targets:
                        if (target['name'] not in targets_to_remove):
                            target_append = {
                                'name': target['name'],
                            }
                            targets_to_add.append(target_append)
                except BaseException:
                    pass
                paramgram['targets_to_add'] = targets_to_add
                results = set_devprof_scope(fmgr, paramgram)
                fmgr.govern_response(module=module, results=results, good_codes=[0, (- 10033), (- 10000), (- 3)], ansible_facts=fmgr.construct_ansible_facts(results, module.params, paramgram))
    except Exception as err:
        raise FMGBaseException(err)
    return module.exit_json(**results[1])