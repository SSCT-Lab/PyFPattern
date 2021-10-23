def main():
    ssh_defaults = {
        'bits': 0,
        'type': 'rsa',
        'passphrase': None,
        'comment': ('ansible-generated on %s' % socket.gethostname()),
    }
    module = AnsibleModule(argument_spec=dict(state=dict(default='present', choices=['present', 'absent'], type='str'), name=dict(required=True, aliases=['user'], type='str'), uid=dict(default=None, type='str'), non_unique=dict(default='no', type='bool'), group=dict(default=None, type='str'), groups=dict(default=None, type='list'), comment=dict(default=None, type='str'), home=dict(default=None, type='path'), shell=dict(default=None, type='str'), password=dict(default=None, type='str', no_log=True), login_class=dict(default=None, type='str'), seuser=dict(default=None, type='str'), force=dict(default='no', type='bool'), remove=dict(default='no', type='bool'), createhome=dict(default='yes', type='bool'), skeleton=dict(default=None, type='str'), system=dict(default='no', type='bool'), move_home=dict(default='no', type='bool'), append=dict(default='no', type='bool'), generate_ssh_key=dict(type='bool'), ssh_key_bits=dict(default=ssh_defaults['bits'], type='int'), ssh_key_type=dict(default=ssh_defaults['type'], type='str'), ssh_key_file=dict(default=None, type='path'), ssh_key_comment=dict(default=ssh_defaults['comment'], type='str'), ssh_key_passphrase=dict(default=None, type='str', no_log=True), update_password=dict(default='always', choices=['always', 'on_create'], type='str'), expires=dict(default=None, type='float')), supports_check_mode=True)
    user = User(module)
    module.debug(('User instantiated - platform %s' % user.platform))
    if user.distribution:
        module.debug(('User instantiated - distribution %s' % user.distribution))
    rc = None
    out = ''
    err = ''
    result = {
        
    }
    result['name'] = user.name
    result['state'] = user.state
    if (user.state == 'absent'):
        if user.user_exists():
            if module.check_mode:
                module.exit_json(changed=True)
            (rc, out, err) = user.remove_user()
            if (rc != 0):
                module.fail_json(name=user.name, msg=err, rc=rc)
            result['force'] = user.force
            result['remove'] = user.remove
    elif (user.state == 'present'):
        if (not user.user_exists()):
            if module.check_mode:
                module.exit_json(changed=True)
            (rc, out, err) = user.create_user()
            if module.check_mode:
                result['system'] = user.name
            else:
                result['system'] = user.system
                result['createhome'] = user.createhome
        else:
            (rc, out, err) = user.modify_user()
            result['append'] = user.append
            result['move_home'] = user.move_home
        if ((rc is not None) and (rc != 0)):
            module.fail_json(name=user.name, msg=err, rc=rc)
        if (user.password is not None):
            result['password'] = 'NOT_LOGGING_PASSWORD'
    if (rc is None):
        result['changed'] = False
    else:
        result['changed'] = True
    if out:
        result['stdout'] = out
    if err:
        result['stderr'] = err
    if user.user_exists():
        info = user.user_info()
        if (info == False):
            result['msg'] = ('failed to look up user name: %s' % user.name)
            result['failed'] = True
        result['uid'] = info[2]
        result['group'] = info[3]
        result['comment'] = info[4]
        result['home'] = info[5]
        result['shell'] = info[6]
        result['uid'] = info[2]
        if (user.groups is not None):
            result['groups'] = user.groups
        info = user.user_info()
        if (user.home is None):
            user.home = info[5]
        if ((not os.path.exists(user.home)) and user.createhome):
            if (not module.check_mode):
                user.create_homedir(user.home)
                user.chown_homedir(info[2], info[3], user.home)
            result['changed'] = True
        if user.sshkeygen:
            (rc, out, err) = user.ssh_key_gen()
            if ((rc is not None) and (rc != 0)):
                module.fail_json(name=user.name, msg=err, rc=rc)
            if (rc == 0):
                result['changed'] = True
            (rc, out, err) = user.ssh_key_fingerprint()
            if (rc == 0):
                result['ssh_fingerprint'] = out.strip()
            else:
                result['ssh_fingerprint'] = err.strip()
            result['ssh_key_file'] = user.get_ssh_key_path()
            result['ssh_public_key'] = user.get_ssh_public_key()
    module.exit_json(**result)