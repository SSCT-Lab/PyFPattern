def reconfigure_vm(self):
    self.configspec = vim.vm.ConfigSpec()
    self.configspec.deviceChange = []
    self.configure_guestid(vm_obj=self.current_vm_obj)
    self.configure_cpu_and_memory(vm_obj=self.current_vm_obj)
    self.configure_hardware_params(vm_obj=self.current_vm_obj)
    self.configure_disks(vm_obj=self.current_vm_obj)
    self.configure_network(vm_obj=self.current_vm_obj)
    self.configure_cdrom(vm_obj=self.current_vm_obj)
    self.customize_customvalues(vm_obj=self.current_vm_obj, config_spec=self.configspec)
    self.configure_resource_alloc_info(vm_obj=self.current_vm_obj)
    self.configure_vapp_properties(vm_obj=self.current_vm_obj)
    if (self.params['annotation'] and (self.current_vm_obj.config.annotation != self.params['annotation'])):
        self.configspec.annotation = str(self.params['annotation'])
        self.change_detected = True
    relospec = vim.vm.RelocateSpec()
    if self.params['resource_pool']:
        relospec.pool = self.get_resource_pool()
        if (relospec.pool != self.current_vm_obj.resourcePool):
            task = self.current_vm_obj.RelocateVM_Task(spec=relospec)
            self.wait_for_task(task)
            if (task.info.state == 'error'):
                return {
                    'changed': self.change_applied,
                    'failed': True,
                    'msg': task.info.error.msg,
                    'op': 'relocate',
                }
    if self.change_detected:
        task = None
        try:
            task = self.current_vm_obj.ReconfigVM_Task(spec=self.configspec)
        except vim.fault.RestrictedVersion as e:
            self.module.fail_json(msg=('Failed to reconfigure virtual machine due to product versioning restrictions: %s' % to_native(e.msg)))
        self.wait_for_task(task)
        if (task.info.state == 'error'):
            return {
                'changed': self.change_applied,
                'failed': True,
                'msg': task.info.error.msg,
                'op': 'reconfig',
            }
    if (self.params['uuid'] and self.params['name'] and (self.params['name'] != self.current_vm_obj.config.name)):
        task = self.current_vm_obj.Rename_Task(self.params['name'])
        self.wait_for_task(task)
        if (task.info.state == 'error'):
            return {
                'changed': self.change_applied,
                'failed': True,
                'msg': task.info.error.msg,
                'op': 'rename',
            }
    if (self.params['is_template'] and (not self.current_vm_obj.config.template)):
        try:
            self.current_vm_obj.MarkAsTemplate()
            self.change_applied = True
        except vmodl.fault.NotSupported as e:
            self.module.fail_json(msg=('Failed to mark virtual machine [%s] as template: %s' % (self.params['name'], e.msg)))
    elif ((not self.params['is_template']) and self.current_vm_obj.config.template):
        resource_pool = self.get_resource_pool()
        kwargs = dict(pool=resource_pool)
        if self.params.get('esxi_hostname', None):
            host_system_obj = self.select_host()
            kwargs.update(host=host_system_obj)
        try:
            self.current_vm_obj.MarkAsVirtualMachine(**kwargs)
            self.change_applied = True
        except vim.fault.InvalidState as invalid_state:
            self.module.fail_json(msg=('Virtual machine is not marked as template : %s' % to_native(invalid_state.msg)))
        except vim.fault.InvalidDatastore as invalid_ds:
            self.module.fail_json(msg=('Converting template to virtual machine operation cannot be performed on the target datastores: %s' % to_native(invalid_ds.msg)))
        except vim.fault.CannotAccessVmComponent as cannot_access:
            self.module.fail_json(msg=('Failed to convert template to virtual machine as operation unable access virtual machine component: %s' % to_native(cannot_access.msg)))
        except vmodl.fault.InvalidArgument as invalid_argument:
            self.module.fail_json(msg=('Failed to convert template to virtual machine due to : %s' % to_native(invalid_argument.msg)))
        except Exception as generic_exc:
            self.module.fail_json(msg=('Failed to convert template to virtual machine due to generic error : %s' % to_native(generic_exc)))
        uuid_action = [x for x in self.current_vm_obj.config.extraConfig if (x.key == 'uuid.action')]
        if (not uuid_action):
            uuid_action_opt = vim.option.OptionValue()
            uuid_action_opt.key = 'uuid.action'
            uuid_action_opt.value = 'create'
            self.configspec.extraConfig.append(uuid_action_opt)
        self.change_detected = True
    vm_facts = self.gather_facts(self.current_vm_obj)
    return {
        'changed': self.change_applied,
        'failed': False,
        'instance': vm_facts,
    }