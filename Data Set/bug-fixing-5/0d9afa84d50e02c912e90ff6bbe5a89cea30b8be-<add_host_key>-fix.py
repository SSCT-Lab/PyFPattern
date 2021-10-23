def add_host_key(module, fqdn, key_type='rsa', create_dir=False):
    ' use ssh-keyscan to add the hostkey '
    keyscan_cmd = module.get_bin_path('ssh-keyscan', True)
    if ('USER' in os.environ):
        user_ssh_dir = os.path.expandvars('~${USER}/.ssh/')
        user_host_file = os.path.expandvars('~${USER}/.ssh/known_hosts')
    else:
        user_ssh_dir = '~/.ssh/'
        user_host_file = '~/.ssh/known_hosts'
    user_ssh_dir = os.path.expanduser(user_ssh_dir)
    if (not os.path.exists(user_ssh_dir)):
        if create_dir:
            try:
                os.makedirs(user_ssh_dir, int('700', 8))
            except:
                module.fail_json(msg=('failed to create host key directory: %s' % user_ssh_dir))
        else:
            module.fail_json(msg=('%s does not exist' % user_ssh_dir))
    elif (not os.path.isdir(user_ssh_dir)):
        module.fail_json(msg=('%s is not a directory' % user_ssh_dir))
    this_cmd = ('%s -t %s %s' % (keyscan_cmd, key_type, fqdn))
    (rc, out, err) = module.run_command(this_cmd)
    if ((rc != 0) or (not out)):
        module.fail_json(msg=('failed to get the hostkey for %s' % fqdn))
    module.append_to_file(user_host_file, out)
    return (rc, out, err)