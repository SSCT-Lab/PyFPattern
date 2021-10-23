def set_powerstate(self, vm, state, force):
    '\n        Set the power status for a VM determined by the current and\n        requested states. force is forceful\n        '
    facts = self.gather_facts(vm)
    expected_state = state.replace('_', '').lower()
    current_state = facts['hw_power_status'].lower()
    result = dict(changed=False, failed=False)
    if ((not force) and (current_state not in ['poweredon', 'poweredoff'])):
        result['failed'] = True
        result['msg'] = ('VM is in %s power state. Force is required!' % current_state)
        return result
    if (current_state != expected_state):
        task = None
        try:
            if (expected_state == 'poweredoff'):
                task = vm.PowerOff()
            elif (expected_state == 'poweredon'):
                task = vm.PowerOn()
            elif (expected_state == 'restarted'):
                if (current_state in ('poweredon', 'poweringon', 'resetting', 'poweredoff')):
                    task = vm.Reset()
                else:
                    result['failed'] = True
                    result['msg'] = ('Cannot restart VM in the current state %s' % current_state)
            elif (expected_state == 'suspended'):
                if (current_state in ('poweredon', 'poweringon')):
                    task = vm.Suspend()
                else:
                    result['failed'] = True
                    result['msg'] = ('Cannot suspend VM in the current state %s' % current_state)
            elif (expected_state in ['shutdownguest', 'rebootguest']):
                if ((current_state == 'poweredon') and (vm.guest.toolsRunningStatus == 'guestToolsRunning')):
                    if (expected_state == 'shutdownguest'):
                        task = vm.ShutdownGuest()
                    else:
                        task = vm.RebootGuest()
                    result['changed'] = True
                else:
                    result['failed'] = True
                    result['msg'] = ('VM %s must be in poweredon state & tools should be installed for guest shutdown/reboot' % vm.name)
        except Exception as e:
            result['failed'] = True
            result['msg'] = to_text(e)
        if task:
            self.wait_for_task(task)
            if (task.info.state == 'error'):
                result['failed'] = True
                result['msg'] = str(task.info.error.msg)
            else:
                result['changed'] = True
    if result['changed']:
        newvm = self.getvm(uuid=vm.config.uuid)
        facts = self.gather_facts(newvm)
        result['instance'] = facts
    return result