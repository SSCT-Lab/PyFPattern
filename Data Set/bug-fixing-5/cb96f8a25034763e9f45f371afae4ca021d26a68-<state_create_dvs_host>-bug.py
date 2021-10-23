def state_create_dvs_host(self):
    operation = 'add'
    changed = True
    result = None
    if (not self.module.check_mode):
        (changed, result) = self.modify_dvs_host(operation)
    self.module.exit_json(changed=changed, result=str(result))