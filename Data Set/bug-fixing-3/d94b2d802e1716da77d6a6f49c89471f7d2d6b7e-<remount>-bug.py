def remount(module, mount_bin, args):
    ' will try to use -o remount first and fallback to unmount/mount if unsupported'
    msg = ''
    cmd = [mount_bin]
    if get_platform().lower().endswith('bsd'):
        cmd += ['-u']
    else:
        cmd += ['-o', 'remount']
    if (get_platform().lower() == 'openbsd'):
        if (module.params['fstab'] is not None):
            module.fail_json(msg='OpenBSD does not support alternate fstab files.  Do not specify the fstab parameter for OpenBSD hosts')
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
    if (rc != 0):
        msg = (out + err)
        if ismount(args['name']):
            (rc, msg) = umount(module, args['name'])
        if (rc == 0):
            (rc, msg) = mount(module, args)
    return (rc, msg)