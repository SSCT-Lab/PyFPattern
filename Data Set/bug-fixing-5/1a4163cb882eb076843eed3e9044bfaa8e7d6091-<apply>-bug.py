def apply(self):
    '\n        Apply action to NVME subsystem\n        '
    netapp_utils.ems_log_event('na_ontap_nvme_subsystem', self.server)
    types = ['hosts', 'paths']
    current = self.get_subsystem()
    (add_host_map, remove_host_map) = (dict(), dict())
    cd_action = self.na_helper.get_cd_action(current, self.parameters)
    if ((cd_action is not 'delete') and (self.parameters['state'] == 'present')):
        (add_host_map, remove_host_map) = self.associate_host_map(types)
    if self.na_helper.changed:
        if self.module.check_mode:
            pass
        elif (cd_action == 'create'):
            self.create_subsystem()
            self.modify_host_map(add_host_map, remove_host_map)
        elif (cd_action == 'delete'):
            self.delete_subsystem()
        elif (cd_action is None):
            self.modify_host_map(add_host_map, remove_host_map)
    self.module.exit_json(changed=self.na_helper.changed)