def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(dict(esxi_hostname=dict(required=True, type='str'), switch_name=dict(required=True, type='str'), vmnics=dict(required=True, type='list'), state=dict(default='present', choices=['present', 'absent'], type='str')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    if (not HAS_COLLECTIONS_COUNTER):
        module.fail_json(msg='collections.Counter from Python-2.7 is required for this module')
    vmware_dvs_host = VMwareDvsHost(module)
    vmware_dvs_host.process_state()