def delete_cert(module, executable, keystore_path, keystore_pass, alias, keystore_type):
    ' Delete certificate identified with alias from keystore on keystore_path '
    del_cmd = ("%s -delete -keystore '%s' -storepass '%s' -alias '%s' %s" % (executable, keystore_path, keystore_pass, alias, get_keystore_type(keystore_type)))
    if module.check_mode:
        module.exit_json(changed=True)
    (del_rc, del_out, del_err) = module.run_command(del_cmd, check_rc=True)
    diff = {
        'before': ('%s\n' % alias),
        'after': None,
    }
    return module.exit_json(changed=True, msg=del_out, rc=del_rc, cmd=del_cmd, stdout=del_out, error=del_err, diff=diff)