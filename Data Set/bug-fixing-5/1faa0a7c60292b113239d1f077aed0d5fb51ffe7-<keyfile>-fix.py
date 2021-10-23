def keyfile(module, user, write=False, path=None, manage_dir=True):
    "\n    Calculate name of authorized keys file, optionally creating the\n    directories and file, properly setting permissions.\n\n    :param str user: name of user in passwd file\n    :param bool write: if True, write changes to authorized_keys file (creating directories if needed)\n    :param str path: if not None, use provided path rather than default of '~user/.ssh/authorized_keys'\n    :param bool manage_dir: if True, create and set ownership of the parent dir of the authorized_keys file\n    :return: full path string to authorized_keys for user\n    "
    if (module.check_mode and (path is not None)):
        keysfile = path
        return keysfile
    try:
        user_entry = pwd.getpwnam(user)
    except KeyError as e:
        if (module.check_mode and (path is None)):
            module.fail_json(msg='Either user must exist or you must provide full path to key file in check mode')
        module.fail_json(msg=('Failed to lookup user %s: %s' % (user, to_native(e))))
    if (path is None):
        homedir = user_entry.pw_dir
        sshdir = os.path.join(homedir, '.ssh')
        keysfile = os.path.join(sshdir, 'authorized_keys')
    else:
        sshdir = os.path.dirname(path)
        keysfile = path
    if (not write):
        return keysfile
    uid = user_entry.pw_uid
    gid = user_entry.pw_gid
    if manage_dir:
        if (not os.path.exists(sshdir)):
            os.mkdir(sshdir, int('0700', 8))
            if module.selinux_enabled():
                module.set_default_selinux_context(sshdir, False)
        os.chown(sshdir, uid, gid)
        os.chmod(sshdir, int('0700', 8))
    if (not os.path.exists(keysfile)):
        basedir = os.path.dirname(keysfile)
        if (not os.path.exists(basedir)):
            os.makedirs(basedir)
        try:
            f = open(keysfile, 'w')
        finally:
            f.close()
        if module.selinux_enabled():
            module.set_default_selinux_context(keysfile, False)
    try:
        os.chown(keysfile, uid, gid)
        os.chmod(keysfile, int('0600', 8))
    except OSError:
        pass
    return keysfile