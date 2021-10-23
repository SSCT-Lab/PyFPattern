def main():
    module = AnsibleModule(argument_spec=dict(fstype=dict(required=True, aliases=['type']), dev=dict(required=True, aliases=['device']), opts=dict(), force=dict(type='bool', default='no'), resizefs=dict(type='bool', default='no')), supports_check_mode=True)
    fs_cmd_map = {
        'ext2': {
            'mkfs': 'mkfs.ext2',
            'grow': 'resize2fs',
            'grow_flag': None,
            'force_flag': '-F',
            'fsinfo': 'tune2fs',
        },
        'ext3': {
            'mkfs': 'mkfs.ext3',
            'grow': 'resize2fs',
            'grow_flag': None,
            'force_flag': '-F',
            'fsinfo': 'tune2fs',
        },
        'ext4': {
            'mkfs': 'mkfs.ext4',
            'grow': 'resize2fs',
            'grow_flag': None,
            'force_flag': '-F',
            'fsinfo': 'tune2fs',
        },
        'reiserfs': {
            'mkfs': 'mkfs.reiserfs',
            'grow': 'resize_reiserfs',
            'grow_flag': None,
            'force_flag': '-f',
            'fsinfo': 'reiserfstune',
        },
        'ext4dev': {
            'mkfs': 'mkfs.ext4',
            'grow': 'resize2fs',
            'grow_flag': None,
            'force_flag': '-F',
            'fsinfo': 'tune2fs',
        },
        'xfs': {
            'mkfs': 'mkfs.xfs',
            'grow': 'xfs_growfs',
            'grow_flag': None,
            'force_flag': '-f',
            'fsinfo': 'xfs_info',
        },
        'btrfs': {
            'mkfs': 'mkfs.btrfs',
            'grow': 'btrfs',
            'grow_flag': 'filesystem resize',
            'force_flag': '-f',
            'fsinfo': 'btrfs',
        },
    }
    dev = module.params['dev']
    fstype = module.params['fstype']
    opts = module.params['opts']
    force = module.boolean(module.params['force'])
    resizefs = module.boolean(module.params['resizefs'])
    changed = False
    try:
        _ = fs_cmd_map[fstype]
    except KeyError:
        module.exit_json(changed=False, msg=('WARNING: module does not support this filesystem yet. %s' % fstype))
    mkfscmd = fs_cmd_map[fstype]['mkfs']
    force_flag = fs_cmd_map[fstype]['force_flag']
    growcmd = fs_cmd_map[fstype]['grow']
    fssize_cmd = fs_cmd_map[fstype]['fsinfo']
    if (not os.path.exists(dev)):
        module.fail_json(msg=('Device %s not found.' % dev))
    cmd = module.get_bin_path('blkid', required=True)
    (rc, raw_fs, err) = module.run_command(('%s -c /dev/null -o value -s TYPE %s' % (cmd, dev)))
    fs = raw_fs.strip()
    if ((fs == fstype) and (resizefs is False) and (not force)):
        module.exit_json(changed=False)
    elif ((fs == fstype) and (resizefs is True)):
        devsize_in_bytes = _get_dev_size(dev, module)
        fssize_in_bytes = _get_fs_size(fssize_cmd, dev, module)
        if (fssize_in_bytes < devsize_in_bytes):
            fs_smaller = True
        else:
            fs_smaller = False
        if (module.check_mode and fs_smaller):
            module.exit_json(changed=True, msg=('Resizing filesystem %s on device %s' % (fstype, dev)))
        elif (module.check_mode and (not fs_smaller)):
            module.exit_json(changed=False, msg=('%s filesystem is using the whole device %s' % (fstype, dev)))
        elif fs_smaller:
            cmd = module.get_bin_path(growcmd, required=True)
            (rc, out, err) = module.run_command(('%s %s' % (cmd, dev)))
            if (rc == 0):
                module.exit_json(changed=True, msg=out)
            else:
                module.fail_json(msg=("Resizing filesystem %s on device '%s' failed" % (fstype, dev)), rc=rc, err=err)
        else:
            module.exit_json(changed=False, msg=('%s filesystem is using the whole device %s' % (fstype, dev)))
    elif (fs and (not force)):
        module.fail_json(msg=("'%s' is already used as %s, use force=yes to overwrite" % (dev, fs)), rc=rc, err=err)
    if module.check_mode:
        changed = True
    else:
        mkfs = module.get_bin_path(mkfscmd, required=True)
        cmd = None
        if (opts is None):
            cmd = ("%s %s '%s'" % (mkfs, force_flag, dev))
        else:
            cmd = ("%s %s %s '%s'" % (mkfs, force_flag, opts, dev))
        (rc, _, err) = module.run_command(cmd)
        if (rc == 0):
            changed = True
        else:
            module.fail_json(msg=("Creating filesystem %s on device '%s' failed" % (fstype, dev)), rc=rc, err=err)
    module.exit_json(changed=changed)