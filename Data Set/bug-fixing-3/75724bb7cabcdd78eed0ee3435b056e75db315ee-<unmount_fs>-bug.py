def unmount_fs(module, filesystem):
    ' Unmount a file system.'
    unmount_cmd = module.get_bin_path('unmount', True)
    if (not module.check_mode):
        (rc, unmount_out, err) = module.run_command(('%s %s' % (unmount_cmd, filesystem)))
        if (rc != 0):
            module.fail_json('Failed to run unmount.', rc=rc, err=err)
        else:
            changed = True
            msg = ('File system %s unmounted.' % filesystem)
            return (changed, msg)
    else:
        changed = True
        msg = ''
        return (changed, msg)