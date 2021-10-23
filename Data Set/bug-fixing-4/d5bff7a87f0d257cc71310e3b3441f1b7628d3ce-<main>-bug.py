def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(name=dict(type='str'), uuid=dict(type='str'), moid=dict(type='str'), folder=dict(type='str'), datacenter=dict(type='str', default='ha-datacenter'), export_dir=dict(type='str'), export_with_images=dict(type='bool', default=False))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True, required_one_of=[['name', 'uuid', 'moid']])
    pyv = VMwareExportVmOvf(module)
    vm = pyv.get_vm()
    if vm:
        vm_facts = pyv.gather_facts(vm)
        vm_power_state = vm_facts['hw_power_status'].lower()
        if (vm_power_state != 'poweredoff'):
            module.fail_json(msg='VM state should be poweredoff to export')
        results = pyv.export_to_ovf_files(vm_obj=vm)
    else:
        module.fail_json(msg='The specified virtual machine not found')
    module.exit_json(**results)