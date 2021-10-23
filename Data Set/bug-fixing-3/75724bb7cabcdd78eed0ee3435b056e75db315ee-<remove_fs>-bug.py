def remove_fs(module, filesystem, rm_mount_point):
    ' Remove an LVM file system or NFS entry. '
    rm_mount_point_opt = {
        True: '-r',
        False: '',
    }
    rm_mount_point = rm_mount_point_opt[rm_mount_point]
    rmfs_cmd = module.get_bin_path('rmfs', True)
    if (not module.check_mode):
        (rc, rmfs_out, err) = module.run_command(('%s -r %s %s' % (rmfs_cmd, rm_mount_point, filesystem)))
        if (rc != 0):
            module.fail_json(msg='Failed to run rmfs.', rc=rc, err=err)
        else:
            changed = True
            msg = rmfs_out
            if (not rmfs_out):
                msg = ('File system %s removed.' % filesystem)
            return (changed, msg)
    else:
        changed = True
        msg = ''
        return (changed, msg)