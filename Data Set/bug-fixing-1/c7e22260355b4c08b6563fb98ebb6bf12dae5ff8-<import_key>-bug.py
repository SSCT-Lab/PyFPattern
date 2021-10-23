

def import_key(module, keyring, keyserver, key_id):
    if keyring:
        cmd = ('%s --keyring %s adv --keyserver %s --recv %s' % (apt_key_bin, keyring, keyserver, key_id))
    else:
        cmd = ('%s adv --keyserver %s --recv %s' % (apt_key_bin, keyserver, key_id))
    for retry in range(5):
        lang_env = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C')
        (rc, out, err) = module.run_command(cmd, environ_update=lang_env)
        if (rc == 0):
            break
    else:
        if ((rc == 2) and ('not found on keyserver' in out)):
            msg = ('Key %s not found on keyserver %s' % (key_id, keyserver))
            module.fail_json(cmd=cmd, msg=msg)
        else:
            msg = ('Error fetching key %s from keyserver: %s' % (key_id, keyserver))
            module.fail_json(cmd=cmd, msg=msg, rc=rc, stdout=out, stderr=err)
    return True
