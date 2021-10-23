

def copy_file_from_remote(module, local, local_file_directory, file_system='bootflash:'):
    hostname = module.params['host']
    username = module.params['username']
    password = module.params['password']
    port = module.params['connect_ssh_port']
    try:
        child = pexpect.spawn(((((('ssh ' + username) + '@') + hostname) + ' -p') + str(port)))
        index = child.expect(['yes', '(?i)Password', '#'])
        if (index == 0):
            child.sendline('yes')
            child.expect('(?i)Password')
        if (index == 1):
            child.sendline(password)
            child.expect('#')
        ldir = '/'
        if local_file_directory:
            dir_array = local_file_directory.split('/')
            for each in dir_array:
                if each:
                    child.sendline((('mkdir ' + ldir) + each))
                    child.expect('#')
                    ldir += (each + '/')
        cmdroot = 'copy scp://'
        ruser = (module.params['remote_scp_server_user'] + '@')
        rserver = module.params['remote_scp_server']
        rfile = (module.params['remote_file'] + ' ')
        vrf = ' vrf management'
        command = (((((((cmdroot + ruser) + rserver) + rfile) + file_system) + ldir) + local) + vrf)
        child.sendline(command)
        index = child.expect(['timed out', 'existing', 'yes', '(?i)password'], timeout=180)
        if (index == 0):
            module.fail_json(msg='Timeout occured due to remote scp server not responding')
        elif (index == 1):
            child.sendline('y')
            sub_index = child.expect(['yes', '(?i)password'])
            if (sub_index == 0):
                child.sendline('yes')
                child.expect('(?i)password')
        elif (index == 2):
            child.sendline('yes')
            child.expect('(?i)password')
        child.sendline(module.params['remote_scp_server_password'])
        fpt = module.params['file_pull_timeout']
        index = child.expect(['No space', 'Permission denied', 'No such file', pexpect.TIMEOUT, '#'], timeout=fpt)
        if (index == 0):
            module.fail_json(msg='File copy failed due to no space left on the device')
        elif (index == 1):
            module.fail_json(msg='Username/Password for remote scp server is wrong')
        elif (index == 2):
            module.fail_json(msg='File copy failed due to remote file not present')
        elif (index == 3):
            module.fail_json(msg='Timeout occured, please increase "file_pull_timeout" and try again!')
    except pexpect.ExceptionPexpect as e:
        module.fail_json(msg=('%s' % to_native(e)), exception=traceback.format_exc())
    child.close()
