def _get_packages(module, pip, chdir):
    'Return results of pip command to get packages.'
    command = ('%s list --format=freeze' % pip)
    lang_env = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C')
    (rc, out, err) = module.run_command(command, cwd=chdir, environ_update=lang_env)
    if (rc != 0):
        command = ('%s freeze' % pip)
        (rc, out, err) = module.run_command(command, cwd=chdir)
        if (rc != 0):
            _fail(module, command, out, err)
    return (command, out, err)