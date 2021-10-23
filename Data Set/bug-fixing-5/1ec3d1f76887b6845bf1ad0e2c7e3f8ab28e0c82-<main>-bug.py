def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(dict(datacenter_name=dict(required=True, type='str'), state=dict(default='present', choices=['present', 'absent'], type='str')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_PYVMOMI):
        module.fail_json(msg='pyvmomi is required for this module')
    context = connect_to_api(module)
    state = module.params.get('state')
    if (state == 'present'):
        create_datacenter(context, module)
    if (state == 'absent'):
        destroy_datacenter(context, module)