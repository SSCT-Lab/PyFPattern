def main():
    argument_spec = vmware_argument_spec()
    argument_spec.update(cluster_name=dict(type='str', required=False), esxi_hostname=dict(type='str', required=False))
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=[['cluster_name', 'esxi_hostname']])
    vmware_lockdown_mgr = VmwareLockdownManager(module)
    vmware_lockdown_mgr.ensure()