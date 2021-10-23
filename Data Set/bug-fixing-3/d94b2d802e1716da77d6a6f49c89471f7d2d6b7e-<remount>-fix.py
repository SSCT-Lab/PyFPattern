def remount(module, args):
    "Try to use 'remount' first and fallback to (u)mount if unsupported."
    mount_bin = module.get_bin_path('mount', required=True)
    cmd = [mount_bin]
    if get_platform().lower().endswith('bsd'):
        cmd += ['-u']
    else:
        cmd += ['-o', 'remount']
    if (get_platform().lower() == 'openbsd'):
        if (module.params['fstab'] is not None):
            module.fail_json(msg='OpenBSD does not support alternate fstab files. Do not specify the fstab parameter for OpenBSD hosts')
    else:
        cmd += _set_fstab_args(args['fstab'])
    cmd += [args['name']]
    out = err = ''
    try:
        if get_platform().lower().endswith('bsd'):
            rc = 1
        else:
            (rc, out, err) = module.run_command(cmd)
    except:
        rc = 1
    msg = ''
    if (rc != 0):
        msg = (out + err)
        (rc, msg) = umount(module, args['name'])
        if (rc == 0):
            (rc, msg) = mount(module, args)
    return (rc, msg)