def is_bind_mounted(module, linux_mounts, dest, src=None, fstype=None):
    'Return whether the dest is bind mounted\n\n    :arg module: The AnsibleModule (used for helper functions)\n    :arg dest: The directory to be mounted under. This is the primary means\n        of identifying whether the destination is mounted.\n    :kwarg src: The source directory. If specified, this is used to help\n        ensure that we are detecting that the correct source is mounted there.\n    :kwarg fstype: The filesystem type. If specified this is also used to\n        help ensure that we are detecting the right mount.\n    :kwarg linux_mounts: Cached list of mounts for Linux.\n    :returns: True if the dest is mounted with src otherwise False.\n    '
    is_mounted = False
    if ((get_platform() == 'Linux') and (linux_mounts is not None)):
        if (src is None):
            if (dest in linux_mounts):
                is_mounted = True
        elif ((dest in linux_mounts) and (linux_mounts[dest]['src'] == src)):
            is_mounted = True
    else:
        bin_path = module.get_bin_path('mount', required=True)
        cmd = ('%s -l' % bin_path)
        (rc, out, err) = module.run_command(cmd)
        mounts = []
        if len(out):
            mounts = to_native(out).strip().split('\n')
        for mnt in mounts:
            arguments = mnt.split()
            if (((arguments[0] == src) or (src is None)) and (arguments[2] == dest) and ((arguments[4] == fstype) or (fstype is None))):
                is_mounted = True
            if is_mounted:
                break
    return is_mounted