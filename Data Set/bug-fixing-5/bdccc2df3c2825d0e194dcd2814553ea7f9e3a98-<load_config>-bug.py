def load_config(module, commands, warnings, commit=False, replace=False, comment=None, admin=False):
    cmd = 'configure terminal'
    if admin:
        cmd = ('admin ' + cmd)
    (rc, out, err) = exec_command(module, cmd)
    if (rc != 0):
        module.fail_json(msg='unable to enter configuration mode', err=to_text(err, errors='surrogate_or_strict'))
    failed = False
    for command in to_list(commands):
        if (command == 'end'):
            continue
        (rc, out, err) = exec_command(module, command)
        if (rc != 0):
            failed = True
            break
    if failed:
        exec_command(module, 'abort')
        module.fail_json(msg=to_text(err, errors='surrogate_or_strict'), commands=commands, rc=rc)
    (rc, diff, err) = exec_command(module, 'show commit changes diff')
    if (rc != 0):
        (rc, diff, err) = exec_command(module, 'show configuration')
        if module._diff:
            warnings.append('device platform does not support config diff')
    if commit:
        cmd = 'commit'
        if comment:
            cmd += ' comment {0}'.format(comment)
    else:
        cmd = 'abort'
        diff = None
    (rc, out, err) = exec_command(module, cmd)
    if (rc != 0):
        exec_command(module, 'abort')
        module.fail_json(msg=err, commands=commands, rc=rc)
    return to_text(diff, errors='surrogate_or_strict')