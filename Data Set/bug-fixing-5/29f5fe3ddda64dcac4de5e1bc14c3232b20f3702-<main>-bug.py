def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(dict(esxi_hostname=dict(required=True, type='str'), device=dict(required=True, type='str'), current_switch_name=dict(required=True, type='str'), current_portgroup_name=dict(required=True, type='str'), migrate_switch_name=dict(required=True, type='str'), migrate_portgroup_name=dict(required=True, type='str')))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    if (not HAS_PYVMOMI):
        self.module.fail_json(msg='pyvmomi required for this module')
    vmware_migrate_vmk = VMwareMigrateVmk(module)
    vmware_migrate_vmk.process_state()