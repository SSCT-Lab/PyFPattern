def process_state(self):
    host_states = {
        'absent': {
            'present': self.state_remove_host,
            'absent': self.state_exit_unchanged,
        },
        'present': {
            'present': self.state_exit_unchanged,
            'absent': self.state_add_host,
        },
        'add_or_reconnect': {
            'present': self.state_reconnect_host,
            'absent': self.state_add_host,
        },
        'reconnect': {
            'present': self.state_reconnect_host,
        },
    }
    try:
        host_states[self.state][self.check_host_state()]()
    except vmodl.RuntimeFault as runtime_fault:
        self.module.fail_json(msg=to_native(runtime_fault.msg))
    except vmodl.MethodFault as method_fault:
        self.module.fail_json(msg=to_native(method_fault.msg))
    except Exception as e:
        self.module.fail_json(msg=to_native(e))