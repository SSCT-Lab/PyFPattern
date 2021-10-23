def apply(self):
    results = netapp_utils.get_cserver(self.server)
    cserver = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=results)
    netapp_utils.ems_log_event('na_ontap_fcp', cserver)
    exists = self.get_fcp()
    changed = False
    if (self.parameters['state'] == 'present'):
        if exists:
            if (self.parameters['status'] == 'up'):
                if (not self.current_status()):
                    self.start_fcp()
                    changed = True
            elif self.current_status():
                self.stop_fcp()
                changed = True
        else:
            self.create_fcp()
            if (self.parameters['status'] == 'up'):
                self.start_fcp()
            elif (self.parameters['status'] == 'down'):
                self.stop_fcp()
            changed = True
    elif exists:
        if self.current_status():
            self.stop_fcp()
        self.destroy_fcp()
        changed = True
    self.module.exit_json(changed=changed)