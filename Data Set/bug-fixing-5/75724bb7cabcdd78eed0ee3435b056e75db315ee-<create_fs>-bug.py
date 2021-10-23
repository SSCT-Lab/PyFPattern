def create_fs(module, fs_type, filesystem, vg, device, size, mount_group, auto_mount, account_subsystem, permissions, nfs_server, attributes):
    ' Create LVM file system or NFS remote mount point. '
    attributes = ' -a '.join(attributes)
    account_subsys_opt = {
        True: '-t yes',
        False: '-t no',
    }
    if (nfs_server is not None):
        auto_mount_opt = {
            True: '-A',
            False: '-a',
        }
    else:
        auto_mount_opt = {
            True: '-A yes',
            False: '-A no',
        }
    if (size is None):
        size = ''
    else:
        size = ('-a size=%s' % size)
    if (device is None):
        device = ''
    else:
        device = ('-d %s' % device)
    if (vg is None):
        vg = ''
    else:
        (vg_state, msg) = _validate_vg(module, vg)
        if vg_state:
            vg = ('-g %s' % vg)
        else:
            changed = False
            return (changed, msg)
    if (mount_group is None):
        mount_group = ''
    else:
        mount_group = ('-u %s' % mount_group)
    auto_mount = auto_mount_opt[auto_mount]
    account_subsystem = account_subsys_opt[account_subsystem]
    if (nfs_server is not None):
        mknfsmnt_cmd = module.get_bin_path('mknfsmnt', True)
        if (not module.check_mode):
            (rc, mknfsmnt_out, err) = module.run_command(('%s -f "%s" %s -h "%s" -t "%s" "%s" -w "bg"' % (mknfsmnt_cmd, filesystem, device, nfs_server, permissions, auto_mount)))
            if (rc != 0):
                module.fail_json(msg='Failed to run mknfsmnt.', rc=rc, err=err)
            else:
                changed = True
                msg = ('NFS file system %s created.' % filesystem)
                return (changed, msg)
        else:
            changed = True
            msg = ''
            return (changed, msg)
    else:
        crfs_cmd = module.get_bin_path('crfs', True)
        if (not module.check_mode):
            (rc, crfs_out, err) = module.run_command(('%s -v %s -m %s %s %s %s %s %s -p %s %s -a %s' % (crfs_cmd, fs_type, filesystem, vg, device, mount_group, auto_mount, account_subsystem, permissions, size, attributes)))
            if (rc == 10):
                module.exit_json(msg=('Using a existent previously defined logical volume, volume group needs to be empty. %s' % err))
            elif (rc != 0):
                module.fail_json(msg='Failed to run crfs.', rc=rc, err=err)
            else:
                changed = True
                return (changed, crfs_out)
        else:
            changed = True
            msg = ''
            return (changed, msg)