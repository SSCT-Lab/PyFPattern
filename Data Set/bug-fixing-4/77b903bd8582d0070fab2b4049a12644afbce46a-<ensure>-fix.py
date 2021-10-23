def ensure(self):
    '\n        Function to manage internal state management\n        '
    results = dict(changed=False, host_lockdown_state=dict())
    change_list = []
    desired_state = self.params.get('state')
    for host in self.hosts:
        results['host_lockdown_state'][host.name] = dict(current_state='', desired_state=desired_state, previous_state='')
        changed = False
        try:
            if host.config.adminDisabled:
                results['host_lockdown_state'][host.name]['previous_state'] = 'present'
                if (desired_state == 'absent'):
                    host.ExitLockdownMode()
                    results['host_lockdown_state'][host.name]['current_state'] = 'absent'
                    changed = True
                else:
                    results['host_lockdown_state'][host.name]['current_state'] = 'present'
            elif (not host.config.adminDisabled):
                results['host_lockdown_state'][host.name]['previous_state'] = 'absent'
                if (desired_state == 'present'):
                    host.EnterLockdownMode()
                    results['host_lockdown_state'][host.name]['current_state'] = 'present'
                    changed = True
                else:
                    results['host_lockdown_state'][host.name]['current_state'] = 'absent'
        except vim.fault.HostConfigFault as host_config_fault:
            self.module.fail_json(msg=('Failed to manage lockdown mode for esxi hostname %s : %s' % (host.name, to_native(host_config_fault.msg))))
        except vim.fault.AdminDisabled as admin_disabled:
            self.module.fail_json(msg=('Failed to manage lockdown mode as administrator permission has been disabled for esxi hostname %s : %s' % (host.name, to_native(admin_disabled.msg))))
        except Exception as generic_exception:
            self.module.fail_json(msg=('Failed to manage lockdown mode due to generic exception for esxi hostname %s : %s' % (host.name, to_native(generic_exception))))
        change_list.append(changed)
    if any(change_list):
        results['changed'] = True
    self.module.exit_json(**results)