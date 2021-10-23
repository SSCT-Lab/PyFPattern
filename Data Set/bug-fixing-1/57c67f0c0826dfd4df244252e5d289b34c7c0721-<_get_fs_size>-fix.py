

def _get_fs_size(fssize_cmd, dev, module):
    ' Return size in bytes of filesystem on device. Returns int '
    cmd = module.get_bin_path(fssize_cmd, required=True)
    if ('tune2fs' == fssize_cmd):
        (rc, size, err) = module.run_command(('%s %s %s' % (cmd, '-l', dev)))
        if (rc == 0):
            for line in size.splitlines():
                if ('Block count:' in line):
                    block_count = int(line.split(':')[1].strip())
                elif ('Block size:' in line):
                    block_size = int(line.split(':')[1].strip())
                    break
        else:
            module.fail_json(msg=('Failed to get block count and block size of %s with %s' % (dev, cmd)), rc=rc, err=err)
    elif ('xfs_info' == fssize_cmd):
        (rc, size, err) = module.run_command(('%s %s' % (cmd, dev)))
        if (rc == 0):
            for line in size.splitlines():
                col = line.split('=')
                if (col[0].strip() == 'data'):
                    if (col[1].strip() != 'bsize'):
                        module.fail_json(msg='Unexpected output format from xfs_info (could not locate "bsize")')
                    if (col[2].split()[1] != 'blocks'):
                        module.fail_json(msg='Unexpected output format from xfs_info (could not locate "blocks")')
                    block_size = int(col[2].split()[0])
                    block_count = int(col[3].split(',')[0])
                    break
        else:
            module.fail_json(msg=('Failed to get block count and block size of %s with %s' % (dev, cmd)), rc=rc, err=err)
    elif ('btrfs' == fssize_cmd):
        block_size = 1
        block_count = 1
    return (block_size * block_count)
