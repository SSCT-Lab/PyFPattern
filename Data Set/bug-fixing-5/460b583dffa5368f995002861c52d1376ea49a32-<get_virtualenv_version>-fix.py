def get_virtualenv_version(args, python):
    'Get the virtualenv version for the given python intepreter, if available.'
    try:
        return get_virtualenv_version.result
    except AttributeError:
        pass
    get_virtualenv_version.result = None
    cmd = [python, '-m', 'virtualenv', '--version']
    try:
        stdout = run_command(args, cmd, capture=True)[0]
    except SubprocessError as ex:
        if (args.verbosity > 1):
            display.error(ex)
        stdout = ''
    if stdout:
        try:
            get_virtualenv_version.result = tuple((int(v) for v in stdout.strip().split('.')))
        except Exception:
            pass
    return get_virtualenv_version.result