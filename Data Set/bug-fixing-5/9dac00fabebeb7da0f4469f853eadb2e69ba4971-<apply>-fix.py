def apply(self):
    '\n        Apply action to cluster HA\n        '
    results = netapp_utils.get_cserver(self.server)
    cserver = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=results)
    netapp_utils.ems_log_event('na_ontap_cluster_ha', cserver)
    current = self.get_cluster_ha_enabled()
    cd_action = self.na_helper.get_cd_action(current, self.parameters)
    if (cd_action == 'create'):
        self.modify_cluster_ha('true')
    elif (cd_action == 'delete'):
        self.modify_cluster_ha('false')
    self.module.exit_json(changed=self.na_helper.changed)