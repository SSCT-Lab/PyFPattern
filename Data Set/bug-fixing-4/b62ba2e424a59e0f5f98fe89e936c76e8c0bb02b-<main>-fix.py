def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(esxi_hostname=dict(type='str', required=False))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    vm_host_manager = VMwareHostFactManager(module)
    vm_host_manager.all_facts()