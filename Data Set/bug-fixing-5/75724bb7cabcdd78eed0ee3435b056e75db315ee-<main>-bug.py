def main():
    module = AnsibleModule(argument_spec=dict(account_subsystem=dict(type='bool', default=False), attributes=dict(type='list', default=["agblksize='4096'", "isnapshot='no'"]), auto_mount=dict(type='bool', default=True), device=dict(type='str'), filesystem=dict(type='str', required=True), fs_type=dict(type='str', default='jfs2'), permissions=dict(type='str', default='rw', choices=['rw', 'ro']), mount_group=dict(type='str'), nfs_server=dict(type='str'), rm_mount_point=dict(type='bool', default=False), size=dict(type='str'), state=dict(type='str', default='present', choices=['absent', 'mounted', 'present', 'unmounted']), vg=dict(type='str')), supports_check_mode=True)
    account_subsystem = module.params['account_subsystem']
    attributes = module.params['attributes']
    auto_mount = module.params['auto_mount']
    device = module.params['device']
    fs_type = module.params['fs_type']
    permissions = module.params['permissions']
    mount_group = module.params['mount_group']
    filesystem = module.params['filesystem']
    nfs_server = module.params['nfs_server']
    rm_mount_point = module.params['rm_mount_point']
    size = module.params['size']
    state = module.params['state']
    vg = module.params['vg']
    result = dict(changed=False, msg='')
    if (state == 'present'):
        fs_mounted = ismount(filesystem)
        fs_exists = _fs_exists(module, filesystem)
        if (fs_mounted or fs_exists):
            result['msg'] = ('File system %s already exists.' % filesystem)
            result['changed'] = False
            if (size is not None):
                (result['changed'], result['msg']) = resize_fs(module, filesystem, size)
        else:
            if (nfs_server is not None):
                if (device is None):
                    result['msg'] = 'Parameter "device" is required when "nfs_server" is defined.'
                    module.fail_json(**result)
                elif _check_nfs_device(module, nfs_server, device):
                    (result['changed'], result['msg']) = create_fs(module, fs_type, filesystem, vg, device, size, mount_group, auto_mount, account_subsystem, permissions, nfs_server, attributes)
            if (device is None):
                if (vg is None):
                    module.fail_json(**result)
                else:
                    (result['changed'], result['msg']) = create_fs(module, fs_type, filesystem, vg, device, size, mount_group, auto_mount, account_subsystem, permissions, nfs_server, attributes)
            if ((device is not None) and (nfs_server is None)):
                (result['changed'], result['msg']) = create_fs(module, fs_type, filesystem, vg, device, size, mount_group, auto_mount, account_subsystem, permissions, nfs_server, attributes)
    elif (state == 'absent'):
        if ismount(filesystem):
            result['msg'] = ('File system %s mounted.' % filesystem)
        else:
            fs_status = _fs_exists(module, filesystem)
            if (not fs_status):
                result['msg'] = ('File system %s does not exist.' % filesystem)
            else:
                (result['changed'], result['msg']) = remove_fs(module, filesystem, rm_mount_point)
    elif (state == 'mounted'):
        if ismount(filesystem):
            result['changed'] = False
            result['msg'] = ('File system %s already mounted.' % filesystem)
        else:
            (result['changed'], result['msg']) = mount_fs(module, filesystem)
    elif (state == 'unmounted'):
        if (not ismount(filesystem)):
            result['changed'] = False
            result['msg'] = ('File system %s already unmounted.' % filesystem)
        else:
            (result['changed'], result['msg']) = unmount_fs(module, filesystem)
    else:
        result['msg'] = ('Unexpected state %s.' % state)
        module.fail_json(**result)
    module.exit_json(**result)