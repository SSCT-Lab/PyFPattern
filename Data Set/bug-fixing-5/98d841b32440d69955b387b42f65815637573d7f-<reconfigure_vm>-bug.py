def reconfigure_vm(self):
    self.configspec = vim.vm.ConfigSpec()
    self.configspec.deviceChange = []
    self.configure_guestid(vm_obj=self.current_vm_obj)
    self.configure_cpu_and_memory(vm_obj=self.current_vm_obj)
    self.configure_disks(vm_obj=self.current_vm_obj)
    self.configure_network(vm_obj=self.current_vm_obj)
    self.customize_customvalues(vm_obj=self.current_vm_obj)
    if (self.params['annotation'] and (self.current_vm_obj.config.annotation != self.params['annotation'])):
        self.configspec.annotation = str(self.params['annotation'])
        self.change_detected = True
    relospec = vim.vm.RelocateSpec()
    hostsystem = self.select_host()
    relospec.pool = self.select_resource_pool(hostsystem)
    change_applied = False
    if (relospec.pool != self.current_vm_obj.resourcePool):
        task = self.current_vm_obj.RelocateVM_Task(spec=relospec)
        self.wait_for_task(task)
        change_applied = True
    if self.change_detected:
        task = self.current_vm_obj.ReconfigVM_Task(spec=self.configspec)
        self.wait_for_task(task)
        change_applied = True
        if (task.info.state == 'error'):
            return {
                'changed': change_applied,
                'failed': True,
                'msg': task.info.error.msg,
            }
    if (self.params['uuid'] and self.params['name'] and (self.params['name'] != self.current_vm_obj.config.name)):
        task = self.current_vm_obj.Rename_Task(self.params['name'])
        self.wait_for_task(task)
        change_applied = True
        if (task.info.state == 'error'):
            return {
                'changed': change_applied,
                'failed': True,
                'msg': task.info.error.msg,
            }
    if self.params['is_template']:
        task = self.current_vm_obj.MarkAsTemplate()
        self.wait_for_task(task)
        change_applied = True
    vm_facts = self.gather_facts(self.current_vm_obj)
    return {
        'changed': change_applied,
        'failed': False,
        'instance': vm_facts,
    }