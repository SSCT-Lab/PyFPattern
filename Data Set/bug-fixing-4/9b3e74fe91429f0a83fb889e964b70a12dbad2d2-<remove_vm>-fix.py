def remove_vm(self, vm):
    if (vm.summary.runtime.powerState.lower() == 'poweredon'):
        self.module.fail_json(msg=("Virtual machine %s found in 'powered on' state, please use 'force' parameter to remove or poweroff VM and try removing VM again." % vm.name))
    task = vm.Destroy()
    self.wait_for_task(task)
    if (task.info.state == 'error'):
        return {
            'changed': self.change_applied,
            'failed': True,
            'msg': task.info.error.msg,
            'op': 'destroy',
        }
    else:
        return {
            'changed': self.change_applied,
            'failed': False,
        }