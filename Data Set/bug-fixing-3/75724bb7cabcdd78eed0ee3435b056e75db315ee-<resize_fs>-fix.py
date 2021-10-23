def resize_fs(module, filesystem, size):
    ' Resize LVM file system. '
    chfs_cmd = module.get_bin_path('chfs', True)
    if (not module.check_mode):
        (rc, chfs_out, err) = module.run_command(('%s -a size="%s" %s' % (chfs_cmd, size, filesystem)))
        if (rc == 28):
            changed = False
            return (changed, chfs_out)
        elif (rc != 0):
            if re.findall('Maximum allocation for logical', err):
                changed = False
                return (changed, err)
            else:
                module.fail_json(msg=('Failed to run chfs. Error message: %s' % err))
        else:
            if re.findall('The filesystem size is already', chfs_out):
                changed = False
            else:
                changed = True
            return (changed, chfs_out)
    else:
        changed = True
        msg = ''
        return (changed, msg)