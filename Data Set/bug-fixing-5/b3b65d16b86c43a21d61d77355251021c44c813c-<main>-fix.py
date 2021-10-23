def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(cluster_name=dict(type='str', required=False), esxi_hostname=dict(type='str', required=False))
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=[['cluster_name', 'esxi_hostname']], supports_check_mode=True)
    vmware_host_service_config = VmwareServiceManager(module)
    module.exit_json(changed=False, host_service_facts=vmware_host_service_config.gather_host_facts())