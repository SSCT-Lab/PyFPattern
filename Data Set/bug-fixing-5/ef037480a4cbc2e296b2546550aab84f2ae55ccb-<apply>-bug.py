def apply(self):
    'Apply action to aggregate'
    changed = False
    size_changed = False
    aggregate_exists = self.get_aggr()
    rename_aggregate = False
    results = netapp_utils.get_cserver(self.server)
    cserver = netapp_utils.setup_na_ontap_zapi(module=self.module, vserver=results)
    netapp_utils.ems_log_event('na_ontap_aggregate', cserver)
    if aggregate_exists:
        if (self.state == 'absent'):
            changed = True
        elif (self.state == 'present'):
            if self.service_state:
                changed = True
            if ((self.rename is not None) and (self.name != self.rename)):
                rename_aggregate = True
                changed = True
    elif (self.state == 'present'):
        if ((self.rename is None) and self.disk_count):
            changed = True
    if changed:
        if self.module.check_mode:
            pass
        elif (self.state == 'present'):
            if (not aggregate_exists):
                self.create_aggr()
                if (self.service_state == 'offline'):
                    self.aggregate_offline()
            else:
                if (self.service_state == 'online'):
                    size_changed = self.aggregate_online()
                elif (self.service_state == 'offline'):
                    size_changed = self.aggregate_offline()
                if rename_aggregate:
                    self.rename_aggregate()
                if ((not size_changed) and (not rename_aggregate)):
                    changed = False
        elif (self.state == 'absent'):
            if (self.service_state == 'offline'):
                self.aggregate_offline()
            self.delete_aggr()
    self.module.exit_json(changed=changed)