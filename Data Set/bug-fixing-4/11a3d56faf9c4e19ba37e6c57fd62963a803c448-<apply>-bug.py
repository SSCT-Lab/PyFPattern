def apply(self):
    changed = False
    vserver_details = self.get_vserver()
    if (vserver_details is not None):
        results = netapp_utils.get_cserver(self.server)
        cserver = netapp_utils.setup_ontap_zapi(module=self.module, vserver=results)
        netapp_utils.ems_log_event('na_ontap_svm', cserver)
    rename_vserver = False
    modify_protocols = False
    modify_aggr_list = False
    obj = open('vserver-log', 'a')
    if (vserver_details is not None):
        if (self.state == 'absent'):
            changed = True
        elif (self.state == 'present'):
            if ((self.new_name is not None) and (self.new_name != self.name)):
                rename_vserver = True
                changed = True
            if (self.allowed_protocols is not None):
                self.allowed_protocols.sort()
                vserver_details['allowed_protocols'].sort()
                if (self.allowed_protocols != vserver_details['allowed_protocols']):
                    modify_protocols = True
                    changed = True
            if (self.aggr_list is not None):
                self.aggr_list.sort()
                vserver_details['aggr_list'].sort()
                if (self.aggr_list != vserver_details['aggr_list']):
                    modify_aggr_list = True
                    changed = True
    elif (self.state == 'present'):
        changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if (vserver_details is None):
                self.create_vserver()
            else:
                if rename_vserver:
                    self.rename_vserver()
                if (modify_protocols or modify_aggr_list):
                    self.modify_vserver(modify_protocols, modify_aggr_list)
        elif (self.state == 'absent'):
            self.delete_vserver()
    self.module.exit_json(changed=changed)