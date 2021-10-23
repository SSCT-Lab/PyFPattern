def state_create_dvs_host(self):
    (operation, changed, result) = ('add', True, None)
    if (not self.module.check_mode):
        (changed, result) = self.modify_dvs_host(operation)
    self.module.exit_json(changed=changed, result=to_native(result))