def apply(self):
    '\n        Apply action to create/delete or accept vserver peer\n        '
    results = netapp_utils.get_cserver(self.server)
    cserver = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=results)
    netapp_utils.ems_log_event('na_ontap_vserver_peer', cserver)
    current = self.vserver_peer_get()
    cd_action = self.na_helper.get_cd_action(current, self.parameters)
    if (cd_action == 'create'):
        self.vserver_peer_create()
        if self.is_remote_peer():
            self.vserver_peer_accept()
    elif (cd_action == 'delete'):
        self.vserver_peer_delete()
    self.module.exit_json(changed=self.na_helper.changed)