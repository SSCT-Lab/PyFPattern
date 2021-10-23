def reconfigure_vm(self):
    self.configspec = vim.vm.ConfigSpec()
    self.configspec.deviceChange = []
    self.configure_guestid(vm_obj=self.current_vm_obj)
    self.configure_cpu_and_memory(vm_obj=self.current_vm_obj)
    self.configure_hardware_params(vm_obj=self.current_vm_obj)
    self.configure_disks(vm_obj=self.current_vm_obj)
    self.configure_network(vm_obj=self.current_vm_obj)
    self.configure_cdrom(vm_obj=self.current_vm_obj)
    self.customize_customvalues(vm_obj=self.current_vm_obj)
    if (self.params['annotation'] and (self.current_vm_obj.config.annotation != self.params['annotation'])):
        self.configspec.annotation = str(self.params['annotation'])
        self.change_detected = True
    change_applied = False
    relospec = vim.vm.RelocateSpec()
    if self.params['resource_pool']:
        relospec.pool = self.select_resource_pool_by_name(self.params['resource_pool'])
        if (relospec.pool is None):
            self.module.fail_json(msg=('Unable to find resource pool "%(resource_pool)s"' % self.params))
        elif (relospec.pool != self.current_vm_obj.resourcePool):
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
    if (self.params['is_template'] and (not self.current_vm_obj.config.template)):
        try:
            self.current_vm_obj.MarkAsTemplate()
        except vmodl.fault.NotSupported as e:
            self.module.fail_json(msg=('Failed to mark virtual machine [%s] as template: %s' % (self.params['name'], e.msg)))
        change_applied = True
    elif ((not self.params['is_template']) and self.current_vm_obj.config.template):
        if self.params['resource_pool']:
            resource_pool = self.select_resource_pool_by_name(self.params['resource_pool'])
            if (resource_pool is None):
                self.module.fail_json(msg=('Unable to find resource pool "%(resource_pool)s"' % self.params))
            self.current_vm_obj.MarkAsVirtualMachine(pool=resource_pool)
            uuid_action = [x for x in self.current_vm_obj.config.extraConfig if (x.key == 'uuid.action')]
            if (not uuid_action):
                uuid_action_opt = vim.option.OptionValue()
                uuid_action_opt.key = 'uuid.action'
                uuid_action_opt.value = 'create'
                self.configspec.extraConfig.append(uuid_action_opt)
                self.change_detected = True
            change_applied = True
        else:
            self.module.fail_json(msg='Resource pool must be specified when converting template to VM!')
    vm_facts = self.gather_facts(self.current_vm_obj)
    return {
        'changed': change_applied,
        'failed': False,
        'instance': vm_facts,
    }