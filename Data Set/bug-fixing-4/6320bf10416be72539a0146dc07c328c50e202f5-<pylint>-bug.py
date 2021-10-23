def pylint(self, args, context, paths):
    '\n        :type args: SanityConfig\n        :type context: str\n        :type paths: list[str]\n        :rtype: list[dict[str, str]]\n        '
    rcfile = ('test/sanity/pylint/config/%s' % context)
    if (not os.path.exists(rcfile)):
        rcfile = 'test/sanity/pylint/config/default'
    parser = ConfigParser()
    parser.read(rcfile)
    if parser.has_section('ansible-test'):
        config = dict(parser.items('ansible-test'))
    else:
        config = dict()
    disable_plugins = set((i.strip() for i in config.get('disable-plugins', '').split(',') if i))
    load_plugins = (set(self.plugin_names) - disable_plugins)
    cmd = ([args.python_executable, '-m', 'pylint', '--jobs', '0', '--reports', 'n', '--max-line-length', '160', '--rcfile', rcfile, '--output-format', 'json', '--load-plugins', ','.join(load_plugins)] + paths)
    env = ansible_environment(args)
    env['PYTHONPATH'] += ('%s%s' % (os.path.pathsep, self.plugin_dir))
    if paths:
        try:
            (stdout, stderr) = run_command(args, cmd, env=env, capture=True)
            status = 0
        except SubprocessError as ex:
            stdout = ex.stdout
            stderr = ex.stderr
            status = ex.status
        if (stderr or (status >= 32)):
            raise SubprocessError(cmd=cmd, status=status, stderr=stderr, stdout=stdout)
    else:
        stdout = None
    if ((not args.explain) and stdout):
        messages = json.loads(stdout)
    else:
        messages = []
    return messages