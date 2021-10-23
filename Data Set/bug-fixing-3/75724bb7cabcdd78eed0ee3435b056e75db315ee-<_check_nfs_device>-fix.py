def _check_nfs_device(module, nfs_host, device):
    '\n    Validate if NFS server is exporting the device (remote export).\n\n    :param module: Ansible module.\n    :param nfs_host: nfs_host parameter, NFS server.\n    :param device: device parameter, remote export.\n    :return: True or False.\n    '
    showmount_cmd = module.get_bin_path('showmount', True)
    (rc, showmount_out, err) = module.run_command(('%s -a %s' % (showmount_cmd, nfs_host)))
    if (rc != 0):
        module.fail_json(msg=('Failed to run showmount. Error message: %s' % err))
    else:
        showmount_data = showmount_out.splitlines()
        for line in showmount_data:
            if (line.split(':')[1] == device):
                return True
        return False