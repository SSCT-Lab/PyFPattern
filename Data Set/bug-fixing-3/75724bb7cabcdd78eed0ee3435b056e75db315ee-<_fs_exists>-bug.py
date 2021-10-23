def _fs_exists(module, filesystem):
    '\n    Check if file system already exists on /etc/filesystems.\n\n    :param module: Ansible module.\n    :param filesystem: filesystem name.\n    :return: True or False.\n    '
    lsfs_cmd = module.get_bin_path('lsfs', True)
    (rc, lsfs_out, err) = module.run_command(('%s -l %s' % (lsfs_cmd, filesystem)))
    if (rc == 1):
        if re.findall('No record matching', err):
            return False
        else:
            module.fail_json(msg='Failed to run lsfs.', rc=rc, err=err)
    else:
        return True