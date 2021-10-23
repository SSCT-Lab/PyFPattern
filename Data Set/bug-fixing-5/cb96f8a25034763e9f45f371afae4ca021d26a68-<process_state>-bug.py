def process_state(self):
    try:
        dvs_host_states = {
            'absent': {
                'present': self.state_destroy_dvs_host,
                'absent': self.state_exit_unchanged,
            },
            'present': {
                'update': self.state_update_dvs_host,
                'present': self.state_exit_unchanged,
                'absent': self.state_create_dvs_host,
            },
        }
        dvs_host_states[self.state][self.check_dvs_host_state()]()
    except vmodl.RuntimeFault as runtime_fault:
        self.module.fail_json(msg=runtime_fault.msg)
    except vmodl.MethodFault as method_fault:
        self.module.fail_json(msg=method_fault.msg)
    except Exception as e:
        self.module.fail_json(msg=str(e))