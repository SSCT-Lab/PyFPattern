def main():
    ' Main '
    argument_spec = vmware_argument_spec()
    argument_spec.update(name=dict(type='str'), datacenter=dict(type='str', aliases=['datacenter_name']), cluster=dict(type='str'), gather_nfs_mount_info=dict(type='bool', default=False), gather_vmfs_mount_info=dict(type='bool', default=False))
    module = AnsibleModule(argument_spec=argument_spec, required_one_of=[['cluster', 'datacenter']], supports_check_mode=True)
    result = dict(changed=False)
    pyv = PyVmomiHelper(module)
    if module.params['cluster']:
        dxs = pyv.lookup_datastore_by_cluster()
    else:
        dxs = pyv.lookup_datastore()
    vmware_host_datastore = VMwareHostDatastore(module)
    datastores = vmware_host_datastore.build_datastore_list(dxs)
    result['datastores'] = datastores
    module.exit_json(**result)