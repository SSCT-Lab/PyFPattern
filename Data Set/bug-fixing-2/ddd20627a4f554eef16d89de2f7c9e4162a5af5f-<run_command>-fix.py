

def run_command(self, args, check_rc=False, close_fds=True, executable=None, data=None, binary_data=False, path_prefix=None, cwd=None, use_unsafe_shell=False, prompt_regex=None, environ_update=None, umask=None, encoding='utf-8', errors='surrogate_or_strict'):
    '\n        Execute a command, returns rc, stdout, and stderr.\n\n        :arg args: is the command to run\n            * If args is a list, the command will be run with shell=False.\n            * If args is a string and use_unsafe_shell=False it will split args to a list and run with shell=False\n            * If args is a string and use_unsafe_shell=True it runs with shell=True.\n        :kw check_rc: Whether to call fail_json in case of non zero RC.\n            Default False\n        :kw close_fds: See documentation for subprocess.Popen(). Default True\n        :kw executable: See documentation for subprocess.Popen(). Default None\n        :kw data: If given, information to write to the stdin of the command\n        :kw binary_data: If False, append a newline to the data.  Default False\n        :kw path_prefix: If given, additional path to find the command in.\n            This adds to the PATH environment vairable so helper commands in\n            the same directory can also be found\n        :kw cwd: If given, working directory to run the command inside\n        :kw use_unsafe_shell: See `args` parameter.  Default False\n        :kw prompt_regex: Regex string (not a compiled regex) which can be\n            used to detect prompts in the stdout which would otherwise cause\n            the execution to hang (especially if no input data is specified)\n        :kw environ_update: dictionary to *update* os.environ with\n        :kw umask: Umask to be used when running the command. Default None\n        :kw encoding: Since we return native strings, on python3 we need to\n            know the encoding to use to transform from bytes to text.  If you\n            want to always get bytes back, use encoding=None.  The default is\n            "utf-8".  This does not affect transformation of strings given as\n            args.\n        :kw errors: Since we return native strings, on python3 we need to\n            transform stdout and stderr from bytes to text.  If the bytes are\n            undecodable in the ``encoding`` specified, then use this error\n            handler to deal with them.  The default is ``surrogate_or_strict``\n            which means that the bytes will be decoded using the\n            surrogateescape error handler if available (available on all\n            python3 versions we support) otherwise a UnicodeError traceback\n            will be raised.  This does not affect transformations of strings\n            given as args.\n        :returns: A 3-tuple of return code (integer), stdout (native string),\n            and stderr (native string).  On python2, stdout and stderr are both\n            byte strings.  On python3, stdout and stderr are text strings converted\n            according to the encoding and errors parameters.  If you want byte\n            strings on python3, use encoding=None to turn decoding to text off.\n        '
    shell = False
    if isinstance(args, list):
        if use_unsafe_shell:
            args = ' '.join([pipes.quote(x) for x in args])
            shell = True
    elif (isinstance(args, (binary_type, text_type)) and use_unsafe_shell):
        shell = True
    elif isinstance(args, (binary_type, text_type)):
        if PY2:
            args = to_bytes(args, errors='surrogate_or_strict')
        elif PY3:
            args = to_text(args, errors='surrogateescape')
        args = shlex.split(args)
    else:
        msg = "Argument 'args' to run_command must be list or string"
        self.fail_json(rc=257, cmd=args, msg=msg)
    prompt_re = None
    if prompt_regex:
        if isinstance(prompt_regex, text_type):
            if PY3:
                prompt_regex = to_bytes(prompt_regex, errors='surrogateescape')
            elif PY2:
                prompt_regex = to_bytes(prompt_regex, errors='surrogate_or_strict')
        try:
            prompt_re = re.compile(prompt_regex, re.MULTILINE)
        except re.error:
            self.fail_json(msg='invalid prompt regular expression given to run_command')
    if (not shell):
        args = [os.path.expanduser(os.path.expandvars(x)) for x in args if (x is not None)]
    rc = 0
    msg = None
    st_in = None
    old_env_vals = {
        
    }
    for (key, val) in self.run_command_environ_update.items():
        old_env_vals[key] = os.environ.get(key, None)
        os.environ[key] = val
    if environ_update:
        for (key, val) in environ_update.items():
            old_env_vals[key] = os.environ.get(key, None)
            os.environ[key] = val
    if path_prefix:
        old_env_vals['PATH'] = os.environ['PATH']
        os.environ['PATH'] = ('%s:%s' % (path_prefix, os.environ['PATH']))
    if ('PYTHONPATH' in os.environ):
        pypaths = os.environ['PYTHONPATH'].split(':')
        pypaths = [x for x in pypaths if ((not x.endswith('/ansible_modlib.zip')) and (not x.endswith('/debug_dir')))]
        os.environ['PYTHONPATH'] = ':'.join(pypaths)
        if (not os.environ['PYTHONPATH']):
            del os.environ['PYTHONPATH']
    to_clean_args = args
    if PY2:
        if isinstance(args, text_type):
            to_clean_args = to_bytes(args)
    elif isinstance(args, binary_type):
        to_clean_args = to_text(args)
    if isinstance(args, (text_type, binary_type)):
        to_clean_args = shlex.split(to_clean_args)
    clean_args = []
    is_passwd = False
    for arg in to_clean_args:
        if is_passwd:
            is_passwd = False
            clean_args.append('********')
            continue
        if PASSWD_ARG_RE.match(arg):
            sep_idx = arg.find('=')
            if (sep_idx > (- 1)):
                clean_args.append(('%s=********' % arg[:sep_idx]))
                continue
            else:
                is_passwd = True
        arg = heuristic_log_sanitize(arg, self.no_log_values)
        clean_args.append(arg)
    clean_args = ' '.join((pipes.quote(arg) for arg in clean_args))
    if data:
        st_in = subprocess.PIPE
    kwargs = dict(executable=executable, shell=shell, close_fds=close_fds, stdin=st_in, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if (cwd and os.path.isdir(cwd)):
        kwargs['cwd'] = cwd
    prev_dir = os.getcwd()
    if (cwd and os.path.isdir(cwd)):
        try:
            os.chdir(cwd)
        except (OSError, IOError):
            e = get_exception()
            self.fail_json(rc=e.errno, msg=('Could not open %s, %s' % (cwd, str(e))))
    old_umask = None
    if umask:
        old_umask = os.umask(umask)
    try:
        if self._debug:
            self.log(('Executing: ' + clean_args))
        cmd = subprocess.Popen(args, **kwargs)
        stdout = b('')
        stderr = b('')
        rpipes = [cmd.stdout, cmd.stderr]
        if data:
            if (not binary_data):
                data += '\n'
            if isinstance(data, text_type):
                data = to_bytes(data)
            cmd.stdin.write(data)
            cmd.stdin.close()
        while True:
            (rfd, wfd, efd) = select.select(rpipes, [], rpipes, 1)
            if (cmd.stdout in rfd):
                dat = os.read(cmd.stdout.fileno(), 9000)
                stdout += dat
                if (dat == b('')):
                    rpipes.remove(cmd.stdout)
            if (cmd.stderr in rfd):
                dat = os.read(cmd.stderr.fileno(), 9000)
                stderr += dat
                if (dat == b('')):
                    rpipes.remove(cmd.stderr)
            if prompt_re:
                if (prompt_re.search(stdout) and (not data)):
                    return (257, stdout, 'A prompt was encountered while running a command, but no input data was specified')
            if (((not rpipes) or (not rfd)) and (cmd.poll() is not None)):
                break
            elif ((not rpipes) and (cmd.poll() == None)):
                cmd.wait()
                break
        cmd.stdout.close()
        cmd.stderr.close()
        rc = cmd.returncode
    except (OSError, IOError):
        e = get_exception()
        self.fail_json(rc=e.errno, msg=to_native(e), cmd=clean_args)
    except Exception:
        e = get_exception()
        self.fail_json(rc=257, msg=to_native(e), exception=traceback.format_exc(), cmd=clean_args)
    for (key, val) in old_env_vals.items():
        if (val is None):
            del os.environ[key]
        else:
            os.environ[key] = val
    if old_umask:
        os.umask(old_umask)
    if ((rc != 0) and check_rc):
        msg = heuristic_log_sanitize(stderr.rstrip(), self.no_log_values)
        self.fail_json(cmd=clean_args, rc=rc, stdout=stdout, stderr=stderr, msg=msg)
    os.chdir(prev_dir)
    if (encoding is not None):
        return (rc, to_native(stdout, encoding=encoding, errors=errors), to_native(stderr, encoding=encoding, errors=errors))
    return (rc, stdout, stderr)
