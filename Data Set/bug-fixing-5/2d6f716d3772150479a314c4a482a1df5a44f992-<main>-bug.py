def main():
    properties = {
        'str': ['boot', 'disk_driver', 'dns_domain', 'fs_allowed', 'hostname', 'image_uuid', 'internal_metadata_namespace', 'kernel_version', 'limit_priv', 'nic_driver', 'qemu_opts', 'qemu_extra_opts', 'spice_opts', 'uuid', 'vga', 'zfs_data_compression', 'zfs_root_compression', 'zpool'],
        'bool': ['archive_on_delete', 'autoboot', 'debug', 'delegate_dataset', 'docker', 'firewall_enabled', 'force', 'indestructible_delegated', 'indestructible_zoneroot', 'maintain_resolvers', 'nowait'],
        'int': ['cpu_cap', 'cpu_shares', 'max_locked_memory', 'max_lwps', 'max_physical_memory', 'max_swap', 'mdata_exec_timeout', 'quota', 'ram', 'tmpfs', 'vcpus', 'virtio_txburst', 'virtio_txtimer', 'vnc_port', 'zfs_data_recsize', 'zfs_filesystem_limit', 'zfs_io_priority', 'zfs_root_recsize', 'zfs_snapshot_limit'],
        'dict': ['customer_metadata', 'internal_metadata', 'routes'],
        'list': ['disks', 'nics', 'resolvers', 'filesystems'],
    }
    options = dict(state=dict(default='running', type='str', choices=['present', 'running', 'absent', 'deleted', 'stopped', 'created', 'restarted', 'rebooted']), name=dict(default=None, type='str', aliases=['alias']), brand=dict(default='joyent', type='str', choices=['joyent', 'joyent-minimal', 'kvm', 'lx']), cpu_type=dict(default='qemu64', type='str', choices=['host', 'qemu64']), spice_password=dict(type='str', no_log=True), vnc_password=dict(type='str', no_log=True))
    for type in properties:
        for p in properties[type]:
            option = dict(default=None, type=type)
            options[p] = option
    module = AnsibleModule(argument_spec=options, supports_check_mode=True, required_one_of=[['name', 'uuid']])
    module.vmadm = module.get_bin_path('vmadm', required=True)
    p = module.params
    uuid = p['uuid']
    state = p['state']
    if (state in ['present', 'running']):
        vm_state = 'running'
    elif (state in ['stopped', 'created']):
        vm_state = 'stopped'
    elif (state in ['absent', 'deleted']):
        vm_state = 'deleted'
    elif (state in ['restarted', 'rebooted']):
        vm_state = 'rebooted'
    result = {
        'state': state,
    }
    if (not uuid):
        uuid = get_vm_uuid(module, p['name'])
        if ((uuid is None) and (vm_state == 'deleted')):
            result['name'] = p['name']
            module.exit_json(**result)
    validate_uuids(module)
    if p['name']:
        result['name'] = p['name']
    result['uuid'] = uuid
    if (uuid == '*'):
        result['changed'] = manage_all_vms(module, vm_state)
        module.exit_json(**result)
    current_vm_state = get_vm_prop(module, uuid, 'state')
    if ((not current_vm_state) and (vm_state == 'deleted')):
        result['changed'] = False
    elif module.check_mode:
        if ((not current_vm_state) or (get_vm_prop(module, uuid, 'state') != state)):
            result['changed'] = True
        else:
            result['changed'] = False
        module.exit_json(**result)
    elif (not current_vm_state):
        (result['changed'], result['uuid']) = new_vm(module, uuid, vm_state)
    else:
        result['changed'] = vm_state_transition(module, uuid, vm_state)
    module.exit_json(**result)