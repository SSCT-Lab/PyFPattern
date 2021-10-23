def _exec_command(command, use_shell=None, use_tee=None, **env):
    '\n    Internal workhorse for exec_command().\n    '
    if (use_shell is None):
        use_shell = (os.name == 'posix')
    if (use_tee is None):
        use_tee = (os.name == 'posix')
    if ((os.name == 'posix') and use_shell):
        sh = os.environ.get('SHELL', '/bin/sh')
        if is_sequence(command):
            command = [sh, '-c', ' '.join(command)]
        else:
            command = [sh, '-c', command]
        use_shell = False
    elif ((os.name == 'nt') and is_sequence(command)):
        command = ' '.join((_quote_arg(arg) for arg in command))
    env = (env or None)
    try:
        proc = subprocess.Popen(command, shell=use_shell, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=False)
    except EnvironmentError:
        return (127, '')
    (text, err) = proc.communicate()
    text = text.decode(locale.getpreferredencoding(False), errors='replace')
    text = text.replace('\r\n', '\n')
    if (text[(- 1):] == '\n'):
        text = text[:(- 1)]
    if (sys.version_info < (3, 0)):
        text = text.encode('ascii', errors='replace')
    if (use_tee and text):
        print(text)
    return (proc.returncode, text)