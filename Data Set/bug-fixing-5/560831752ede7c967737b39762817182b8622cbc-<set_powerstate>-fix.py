def set_powerstate(self, vm, state, force):
    '\n        Set the power status for a VM determined by the current and\n        requested states. force is forceful\n        '
    facts = self.gather_facts(vm)
    expected_state = state.replace('_', '').lower()
    current_state = facts['hw_power_status'].lower()
    result = {
        
    }
    if ((not force) and (current_state not in ['poweredon', 'poweredoff'])):
        return ('VM is in %s power state. Force is required!' % current_state)
    if (current_state == expected_state):
        result['changed'] = False
        result['failed'] = False
    else:
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
                    result = {
                        'changed': False,
                        'failed': True,
                        'msg': ('Cannot restart VM in the current state %s' % current_state),
                    }
            elif (expected_state == 'suspended'):
                if (current_state in ('poweredon', 'poweringon')):
                    task = vm.Suspend()
                else:
                    result = {
                        'changed': False,
                        'failed': True,
                        'msg': ('Cannot suspend VM in the current state %s' % current_state),
                    }
        except Exception:
            e = get_exception()
            result = {
                'changed': False,
                'failed': True,
                'msg': e,
            }
        if task:
            self.wait_for_task(task)
            if (task.info.state == 'error'):
                result = {
                    'changed': False,
                    'failed': True,
                    'msg': task.info.error.msg,
                }
            else:
                result = {
                    'changed': True,
                    'failed': False,
                }
    if result['changed']:
        newvm = self.getvm(uuid=vm.config.uuid)
        facts = self.gather_facts(newvm)
        result['instance'] = facts
    return result