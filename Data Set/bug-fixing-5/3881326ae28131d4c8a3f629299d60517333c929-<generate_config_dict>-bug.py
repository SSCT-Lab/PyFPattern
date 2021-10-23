def generate_config_dict(array):
    config_info = {
        
    }
    api_version = array._list_available_rest_versions()
    config_info['dns'] = array.get_dns()
    config_info['smtp'] = array.list_alert_recipients()
    config_info['snmp'] = array.list_snmp_managers()
    config_info['snmp_v3_engine_id'] = array.get_snmp_engine_id()['engine_id']
    config_info['directory_service'] = array.get_directory_service()
    if (S3_REQUIRED_API_VERSION in api_version):
        config_info['directory_service_roles'] = {
            
        }
        roles = array.list_directory_service_roles()
        for role in range(0, len(roles)):
            role_name = roles[role]['name']
            config_info['directory_service_roles'][role_name] = {
                'group': roles[role]['group'],
                'group_base': roles[role]['group_base'],
            }
    else:
        config_info['directory_service'].update(array.get_directory_service(groups=True))
    config_info['ntp'] = array.get(ntpserver=True)['ntpserver']
    config_info['syslog'] = array.get(syslogserver=True)['syslogserver']
    config_info['phonehome'] = array.get(phonehome=True)['phonehome']
    config_info['proxy'] = array.get(proxy=True)['proxy']
    config_info['relayhost'] = array.get(relayhost=True)['relayhost']
    config_info['senderdomain'] = array.get(senderdomain=True)['senderdomain']
    config_info['syslog'] = array.get(syslogserver=True)['syslogserver']
    config_info['idle_timeout'] = array.get(idle_timeout=True)['idle_timeout']
    config_info['scsi_timeout'] = array.get(scsi_timeout=True)['scsi_timeout']
    config_info['ssl_certs'] = array.get_certificate()
    if (S3_REQUIRED_API_VERSION in api_version):
        config_info['global_admin'] = array.get_global_admin_attributes()
    return config_info