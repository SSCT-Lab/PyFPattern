def process_state(self):
    try:
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
        host_states[self.state][self.check_host_state()]()
    except vmodl.RuntimeFault as runtime_fault:
        self.module.fail_json(msg=runtime_fault.msg)
    except vmodl.MethodFault as method_fault:
        self.module.fail_json(msg=method_fault.msg)
    except Exception as e:
        self.module.fail_json(msg=str(e))