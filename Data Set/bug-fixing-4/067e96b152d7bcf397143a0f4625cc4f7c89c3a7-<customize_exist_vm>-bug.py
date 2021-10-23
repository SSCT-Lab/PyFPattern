def customize_exist_vm(self):
    task = None
    network_changes = False
    for nw in self.params['networks']:
        for key in nw:
            if (key not in ('device_type', 'mac', 'name', 'vlan', 'type', 'start_connected')):
                network_changes = True
                break
    if ((len(self.params['customization']) > 1) or network_changes or self.params.get('customization_spec')):
        self.customize_vm(vm_obj=self.current_vm_obj)
    try:
        task = self.current_vm_obj.CustomizeVM_Task(self.customspec)
    except vim.fault.CustomizationFault as e:
        self.module.fail_json(msg=('Failed to customization virtual machine due to CustomizationFault: %s' % to_native(e.msg)))
    except vim.fault.RuntimeFault as e:
        self.module.fail_json(msg=('failed to customization virtual machine due to RuntimeFault: %s' % to_native(e.msg)))
    except Exception as e:
        self.module.fail_json(msg=('failed to customization virtual machine due to fault: %s' % to_native(e.msg)))
    self.wait_for_task(task)
    if (task.info.state == 'error'):
        return {
            'changed': self.change_applied,
            'failed': True,
            'msg': task.info.error.msg,
            'op': 'customize_exist',
        }
    if self.params['wait_for_customization']:
        set_vm_power_state(self.content, self.current_vm_obj, 'poweredon', force=False)
        is_customization_ok = self.wait_for_customization(self.current_vm_obj)
        if (not is_customization_ok):
            return {
                'changed': self.change_applied,
                'failed': True,
                'op': 'wait_for_customize_exist',
            }
    return {
        'changed': self.change_applied,
        'failed': False,
    }