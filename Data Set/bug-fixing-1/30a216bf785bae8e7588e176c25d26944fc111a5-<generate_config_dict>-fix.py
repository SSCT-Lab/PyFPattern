

def generate_config_dict(array):
    config_facts = {
        
    }
    api_version = array._list_available_rest_versions()
    config_facts['dns'] = array.get_dns()
    config_facts['smtp'] = array.list_alert_recipients()
    config_facts['snmp'] = array.list_snmp_managers()
    config_facts['directory_service'] = array.get_directory_service()
    if (S3_REQUIRED_API_VERSION in api_version):
        config_facts['directory_service_roles'] = {
            
        }
        roles = array.list_directory_service_roles()
        for role in range(0, len(roles)):
            role_name = roles[role]['name']
            config_facts['directory_service_roles'][role_name] = {
                'group': roles[role]['group'],
                'group_base': roles[role]['group_base'],
            }
    else:
        config_facts['directory_service'].update(array.get_directory_service(groups=True))
    config_facts['ntp'] = array.get(ntpserver=True)['ntpserver']
    config_facts['syslog'] = array.get(syslogserver=True)['syslogserver']
    config_facts['phonehome'] = array.get(phonehome=True)['phonehome']
    config_facts['proxy'] = array.get(proxy=True)['proxy']
    config_facts['relayhost'] = array.get(relayhost=True)['relayhost']
    config_facts['senderdomain'] = array.get(senderdomain=True)['senderdomain']
    config_facts['syslog'] = array.get(syslogserver=True)['syslogserver']
    config_facts['idle_timeout'] = array.get(idle_timeout=True)['idle_timeout']
    config_facts['scsi_timeout'] = array.get(scsi_timeout=True)['scsi_timeout']
    config_facts['ssl_certs'] = array.get_certificate()
    if (S3_REQUIRED_API_VERSION in api_version):
        config_facts['global_admin'] = array.get_global_admin_attributes()
    return config_facts
