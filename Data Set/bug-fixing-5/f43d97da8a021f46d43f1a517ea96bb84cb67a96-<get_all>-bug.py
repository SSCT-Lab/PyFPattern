def get_all(self):
    results = netapp_utils.get_cserver(self.server)
    cserver = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=results)
    netapp_utils.ems_log_event('na_ontap_gather_facts', cserver)
    self.netapp_info['net_interface_info'] = self.get_generic_get_iter('net-interface-get-iter', attribute='net-interface-info', field='interface-name', query={
        'max-records': '1024',
    })
    self.netapp_info['nvme_info'] = self.get_generic_get_iter('nvme-get-iter', attribute='nvme-target-service-info', field='vserver', query={
        'max-records': '1024',
    })
    self.netapp_info['nvme_interface_info'] = self.get_generic_get_iter('nvme-interface-get-iter', attribute='nvme-interface-info', field='vserver', query={
        'max-records': '1024',
    })
    self.netapp_info['nvme_subsystem_info'] = self.get_generic_get_iter('nvme-subsystem-get-iter', attribute='nvme-subsystem-info', field='subsystem', query={
        'max-records': '1024',
    })
    self.netapp_info['nvme_namespace_info'] = self.get_generic_get_iter('nvme-namespace-get-iter', attribute='nvme-namespace-info', field='path', query={
        'max-records': '1024',
    })
    self.netapp_info['net_port_info'] = self.get_generic_get_iter('net-port-get-iter', attribute='net-port-info', field=('node', 'port'), query={
        'max-records': '1024',
    })
    self.netapp_info['cluster_node_info'] = self.get_generic_get_iter('cluster-node-get-iter', attribute='cluster-node-info', field='node-name', query={
        'max-records': '1024',
    })
    self.netapp_info['security_login_account_info'] = self.get_generic_get_iter('security-login-get-iter', attribute='security-login-account-info', field=('user-name', 'application', 'authentication-method'), query={
        'max-records': '1024',
    })
    self.netapp_info['aggregate_info'] = self.get_generic_get_iter('aggr-get-iter', attribute='aggr-attributes', field='aggregate-name', query={
        'max-records': '1024',
    })
    self.netapp_info['volume_info'] = self.get_generic_get_iter('volume-get-iter', attribute='volume-attributes', field=('name', 'owning-vserver-name'), query={
        'max-records': '1024',
    })
    self.netapp_info['lun_info'] = self.get_generic_get_iter('lun-get-iter', attribute='lun-info', field='path', query={
        'max-records': '1024',
    })
    self.netapp_info['storage_failover_info'] = self.get_generic_get_iter('cf-get-iter', attribute='storage-failover-info', field='node', query={
        'max-records': '1024',
    })
    self.netapp_info['net_ifgrp_info'] = self.get_ifgrp_info()
    self.netapp_info['vserver_motd_info'] = self.get_generic_get_iter('vserver-motd-get-iter', attribute='vserver-motd-info', field='vserver', query={
        'max-records': '1024',
    })
    self.netapp_info['vserver_login_banner_info'] = self.get_generic_get_iter('vserver-login-banner-get-iter', attribute='vserver-login-banner-info', field='vserver', query={
        'max-records': '1024',
    })
    self.netapp_info['security_key_manager_key_info'] = self.get_generic_get_iter('security-key-manager-key-get-iter', attribute='security-key-manager-key-info', field=('node', 'key-id'), query={
        'max-records': '1024',
    })
    self.netapp_info['vserver_info'] = self.get_generic_get_iter('vserver-get-iter', attribute='vserver-info', field='vserver-name', query={
        'max-records': '1024',
    })
    self.netapp_info['ontap_version'] = self.ontapi()
    return self.netapp_info