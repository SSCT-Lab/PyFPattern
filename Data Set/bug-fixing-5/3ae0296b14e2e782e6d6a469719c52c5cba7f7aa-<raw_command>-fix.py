def raw_command(cmd, capture=False, env=None, data=None, cwd=None, explain=False, stdin=None, stdout=None, cmd_verbosity=1, str_errors='strict'):
    '\n    :type cmd: collections.Iterable[str]\n    :type capture: bool\n    :type env: dict[str, str] | None\n    :type data: str | None\n    :type cwd: str | None\n    :type explain: bool\n    :type stdin: file | None\n    :type stdout: file | None\n    :type cmd_verbosity: int\n    :type str_errors: str\n    :rtype: str | None, str | None\n    '
    if (not cwd):
        cwd = os.getcwd()
    if (not env):
        env = common_environment()
    cmd = list(cmd)
    escaped_cmd = ' '.join((pipes.quote(c) for c in cmd))
    display.info(('Run command: %s' % escaped_cmd), verbosity=cmd_verbosity, truncate=True)
    display.info(('Working directory: %s' % cwd), verbosity=2)
    program = find_executable(cmd[0], cwd=cwd, path=env['PATH'], required='warning')
    if program:
        display.info(('Program found: %s' % program), verbosity=2)
    for key in sorted(env.keys()):
        display.info(('%s=%s' % (key, env[key])), verbosity=2)
    if explain:
        return (None, None)
    communicate = False
    if (stdin is not None):
        data = None
        communicate = True
    elif (data is not None):
        stdin = subprocess.PIPE
        communicate = True
    if stdout:
        communicate = True
    if capture:
        stdout = (stdout or subprocess.PIPE)
        stderr = subprocess.PIPE
        communicate = True
    else:
        stderr = None
    start = time.time()
    try:
        process = subprocess.Popen(cmd, env=env, stdin=stdin, stdout=stdout, stderr=stderr, cwd=cwd)
    except OSError as ex:
        if (ex.errno == errno.ENOENT):
            raise ApplicationError(('Required program "%s" not found.' % cmd[0]))
        raise
    if communicate:
        encoding = 'utf-8'
        if ((data is None) or isinstance(data, bytes)):
            data_bytes = data
        else:
            data_bytes = data.encode(encoding, 'surrogateescape')
        (stdout_bytes, stderr_bytes) = process.communicate(data_bytes)
        stdout_text = (stdout_bytes.decode(encoding, str_errors) if stdout_bytes else '')
        stderr_text = (stderr_bytes.decode(encoding, str_errors) if stderr_bytes else '')
    else:
        process.wait()
        (stdout_text, stderr_text) = (None, None)
    status = process.returncode
    runtime = (time.time() - start)
    display.info(('Command exited with status %s after %s seconds.' % (status, runtime)), verbosity=4)
    if (status == 0):
        return (stdout_text, stderr_text)
    raise SubprocessError(cmd, status, stdout_text, stderr_text, runtime)