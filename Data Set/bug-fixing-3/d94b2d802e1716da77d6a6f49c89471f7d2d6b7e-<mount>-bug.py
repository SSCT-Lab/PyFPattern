def mount(module, args):
    'Mount up a path or remount if needed.'
    mount_bin = module.get_bin_path('mount', required=True)
    name = args['name']
    cmd = [mount_bin]
    if ismount(name):
        return remount(module, mount_bin, args)
    if (get_platform().lower() == 'openbsd'):
        if (module.params['fstab'] is not None):
            module.fail_json(msg='OpenBSD does not support alternate fstab files.  Do not specify the fstab parameter for OpenBSD hosts')
    else:
        cmd += _set_fstab_args(args['fstab'])
    cmd += [name]
    (rc, out, err) = module.run_command(cmd)
    if (rc == 0):
        return (0, '')
    else:
        return (rc, (out + err))