def process_state(self):
    '\n        Function to manage internal state of vSwitch\n        '
    vswitch_states = {
        'absent': {
            'present': self.state_destroy_vswitch,
            'absent': self.state_exit_unchanged,
        },
        'present': {
            'present': self.state_update_vswitch,
            'absent': self.state_create_vswitch,
        },
    }
    try:
        vswitch_states[self.state][self.check_vswitch_configuration()]()
    except vmodl.RuntimeFault as runtime_fault:
        self.module.fail_json(msg=to_native(runtime_fault.msg))
    except vmodl.MethodFault as method_fault:
        self.module.fail_json(msg=to_native(method_fault.msg))
    except Exception as e:
        self.module.fail_json(msg=to_native(e))