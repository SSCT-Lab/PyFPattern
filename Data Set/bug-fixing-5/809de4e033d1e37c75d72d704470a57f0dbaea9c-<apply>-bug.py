def apply(self):
    property_changed = False
    iscsi_service_exists = False
    netapp_utils.ems_log_event('na_ontap_iscsi', self.server)
    iscsi_service_detail = self.get_iscsi()
    if iscsi_service_detail:
        self.is_started = iscsi_service_detail['is_started']
        iscsi_service_exists = True
        if (self.state == 'absent'):
            property_changed = True
        elif (self.state == 'present'):
            is_started = ('started' if self.is_started else 'stopped')
            property_changed = (is_started != self.service_state)
    elif (self.state == 'present'):
        property_changed = True
    if property_changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if (not iscsi_service_exists):
                self.create_iscsi_service()
            elif (self.service_state == 'started'):
                self.start_iscsi_service()
            else:
                self.stop_iscsi_service()
        elif (self.state == 'absent'):
            self.delete_iscsi_service()
    changed = property_changed
    self.module.exit_json(changed=changed)