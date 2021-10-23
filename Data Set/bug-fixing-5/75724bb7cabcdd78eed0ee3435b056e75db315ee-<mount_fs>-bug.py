def mount_fs(module, filesystem):
    ' Mount a file system. '
    mount_cmd = module.get_bin_path('mount', True)
    if (not module.check_mode):
        (rc, mount_out, err) = module.run_command(('%s %s' % (mount_cmd, filesystem)))
        if (rc != 0):
            module.fail_json('Failed to run mount.', rc=rc, err=err)
        else:
            changed = True
            msg = ('File system %s mounted.' % filesystem)
            return (changed, msg)
    else:
        changed = True
        msg = ''
        return (changed, msg)