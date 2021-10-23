def import_pkcs12_path(module, executable, path, keystore_path, keystore_pass, pkcs12_pass, pkcs12_alias, alias, keystore_type):
    ' Import pkcs12 from path into keystore located on\n        keystore_path as alias '
    import_cmd = ("%s -importkeystore -noprompt -destkeystore '%s' -srcstoretype PKCS12 -deststorepass '%s' -destkeypass '%s' -srckeystore '%s' -srcstorepass '%s' -srcalias '%s' -destalias '%s' %s" % (executable, keystore_path, keystore_pass, keystore_pass, path, pkcs12_pass, pkcs12_alias, alias, get_keystore_type(keystore_type)))
    (import_rc, import_out, import_err) = module.run_command(import_cmd, check_rc=False)
    diff = {
        'before': '\n',
        'after': ('%s\n' % alias),
    }
    if (import_rc == 0):
        module.exit_json(changed=True, msg=import_out, rc=import_rc, cmd=import_cmd, stdout=import_out, error=import_err, diff=diff)
    else:
        module.fail_json(msg=import_out, rc=import_rc, cmd=import_cmd)