def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(dict(switch_name=dict(required=True, type='str'), nic_name=dict(required=False, type='str'), number_of_ports=dict(required=False, type='int', default=128), mtu=dict(required=False, type='int', default=1500), state=dict(default='present', choices=['present', 'absent'], type='str')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if (not HAS_PYVMOMI):
        module.fail_json(msg='pyvmomi is required for this module')
    host_virtual_switch = VMwareHostVirtualSwitch(module)
    host_virtual_switch.process_state()