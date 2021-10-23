def main():
    argument_spec = vmware_argument_spec()
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)
    vmware_vm_facts = VmwareVmFacts(module)
    _virtual_machines = vmware_vm_facts.get_all_virtual_machines()
    module.exit_json(changed=False, virtual_machines=_virtual_machines)