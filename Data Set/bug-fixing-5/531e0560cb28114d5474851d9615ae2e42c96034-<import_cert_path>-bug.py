def import_cert_path(module, executable, path, keystore_path, keystore_pass, alias, keystore_type):
    ' Import certificate from path into keystore located on\n        keystore_path as alias '
    import_cmd = ("%s -importcert -noprompt -keystore '%s' -storepass '%s' -file '%s' -alias '%s' %s" % (executable, keystore_path, keystore_pass, path, alias, get_keystore_type(keystore_type)))
    (import_rc, import_out, import_err) = module.run_command(import_cmd, check_rc=False)
    diff = {
        'before': '\n',
        'after': ('%s\n' % alias),
    }
    if (import_rc == 0):
        module.exit_json(changed=True, msg=import_out, rc=import_rc, cmd=import_cmd, stdout=import_out, error=import_err, diff=diff)
    else:
        module.fail_json(msg=import_out, rc=import_rc, cmd=import_cmd)