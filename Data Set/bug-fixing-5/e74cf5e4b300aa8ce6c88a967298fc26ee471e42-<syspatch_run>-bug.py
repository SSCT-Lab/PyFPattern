def syspatch_run(module):
    cmd = ['/usr/sbin/syspatch']
    changed = False
    reboot_needed = False
    warnings = []
    if module.params['revert']:
        check_flag = ['-l']
        if (module.params['revert'] == 'all'):
            run_flag = ['-R']
        else:
            run_flag = ['-r']
    elif module.params['apply']:
        check_flag = ['-c']
        run_flag = []
    (rc, out, err) = module.run_command((cmd + check_flag))
    if (rc != 0):
        module.fail_json(msg=('Command %s failed rc=%d, out=%s, err=%s' % (cmd, rc, out, err)))
    if (len(out) > 0):
        change_pending = True
    else:
        change_pending = False
    if module.check_mode:
        changed = change_pending
    elif change_pending:
        (rc, out, err) = module.run_command((cmd + run_flag))
        if ((rc != 0) and (err != 'ln: /usr/X11R6/bin/X: No such file or directory\n')):
            module.fail_json(msg=('Command %s failed rc=%d, out=%s, err=%s' % (cmd, rc, out, err)))
        elif out.lower().find('create unique kernel'):
            reboot_needed = True
        elif out.lower().find('syspatch updated itself'):
            warnings.append['Syspatch was updated. Please run syspatch again.']
        if (len(out) > 0):
            warnings.append['syspatch had suggested changes, but stdout was empty.']
        changed = True
    else:
        changed = False
    return dict(changed=changed, reboot_needed=reboot_needed, rc=rc, stderr=err, stdout=out, warnings=warnings)