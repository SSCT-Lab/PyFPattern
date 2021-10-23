

def exec_install(module, items, action, pkgs, res, yum_basecmd):
    cmd = ((yum_basecmd + [action]) + pkgs)
    if module.check_mode:
        module.exit_json(changed=True, results=res['results'], changes=dict(installed=pkgs))
    lang_env = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C')
    (rc, out, err) = module.run_command(cmd, environ_update=lang_env)
    if (rc == 1):
        for spec in items:
            if (('://' in spec) and ((('No package %s available.' % spec) in out) or (('Cannot open: %s. Skipping.' % spec) in err))):
                err = ('Package at %s could not be installed' % spec)
                module.fail_json(changed=False, msg=err, rc=rc)
    res['rc'] = rc
    res['results'].append(out)
    res['msg'] += err
    res['changed'] = True
    if ((('Nothing to do' in out) and (rc == 0)) or ('does not have any packages' in err)):
        res['changed'] = False
    if (rc != 0):
        res['changed'] = False
        module.fail_json(**res)
    if ('No space left on device' in (out or err)):
        res['changed'] = False
        res['msg'] = 'No space left on device'
        module.fail_json(**res)
    return res
