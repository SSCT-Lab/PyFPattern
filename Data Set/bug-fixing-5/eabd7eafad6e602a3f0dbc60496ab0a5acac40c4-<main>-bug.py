def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(datacenter_name=dict(type='str', required=True), cluster_name=dict(type='str', required=True), esxi_hostname=dict(type='str', required=True), esxi_username=dict(type='str', required=False), esxi_password=dict(type='str', required=False, no_log=True), state=dict(default='present', choices=['present', 'absent', 'add_or_reconnect', 'reconnect'], type='str'))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_if=[['state', 'present', ['esxi_username', 'esxi_password']], ['state', 'add_or_reconnect', ['esxi_username', 'esxi_password']]])
    if (not HAS_PYVMOMI):
        module.fail_json(msg='pyvmomi is required for this module')
    vmware_host = VMwareHost(module)
    vmware_host.process_state()