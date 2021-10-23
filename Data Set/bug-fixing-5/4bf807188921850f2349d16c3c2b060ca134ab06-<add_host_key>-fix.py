def add_host_key(module, fqdn, port=22, key_type='rsa', create_dir=False):
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
    if port:
        this_cmd = ('%s -t %s -p %s %s' % (keyscan_cmd, key_type, port, fqdn))
    else:
        this_cmd = ('%s -t %s %s' % (keyscan_cmd, key_type, fqdn))
    (rc, out, err) = module.run_command(this_cmd)
    if ((rc != 0) or (not out)):
        msg = 'failed to retrieve hostkey'
        if (not out):
            msg += ('. "%s" returned no matches.' % this_cmd)
        else:
            msg += (' using command "%s". [stdout]: %s' % (this_cmd, out))
        if err:
            msg += (' [stderr]: %s' % err)
        module.fail_json(msg=msg)
    module.append_to_file(user_host_file, out)
    return (rc, out, err)