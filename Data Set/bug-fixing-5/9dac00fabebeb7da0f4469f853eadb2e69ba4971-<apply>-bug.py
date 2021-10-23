def apply(self):
    '\n        Apply action to cluster HA\n        '
    changed = False
    results = netapp_utils.get_cserver(self.server)
    cserver = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=results)
    netapp_utils.ems_log_event('na_ontap_cluster', cserver)
    if (self.state == 'present'):
        self.modify_cluster_ha('true')
        changed = True
    elif (self.state == 'absent'):
        self.modify_cluster_ha('false')
        changed = True
    self.module.exit_json(changed=changed)