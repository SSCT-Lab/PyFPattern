def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(dict(datacenter_name=dict(required=True, type='str'), state=dict(default='present', choices=['present', 'absent'], type='str')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    vmware_datacenter_mgr = VmwareDatacenterManager(module)
    vmware_datacenter_mgr.ensure()