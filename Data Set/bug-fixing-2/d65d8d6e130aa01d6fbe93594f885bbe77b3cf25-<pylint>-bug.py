

@staticmethod
def pylint(args, context, paths, plugin_dir, plugin_names):
    'Run pylint using the config specified by the context on the specified paths.'
    rcfile = os.path.join(ANSIBLE_ROOT, ('test/sanity/pylint/config/%s' % context.split('/')[0]))
    if (not os.path.exists(rcfile)):
        rcfile = os.path.join(ANSIBLE_ROOT, 'test/sanity/pylint/config/default')
    parser = ConfigParser()
    parser.read(rcfile)
    if parser.has_section('ansible-test'):
        config = dict(parser.items('ansible-test'))
    else:
        config = dict()
    disable_plugins = set((i.strip() for i in config.get('disable-plugins', '').split(',') if i))
    load_plugins = (set(plugin_names) - disable_plugins)
    cmd = ([args.python_executable, '-m', 'pylint', '--jobs', '0', '--reports', 'n', '--max-line-length', '160', '--rcfile', rcfile, '--output-format', 'json', '--load-plugins', ','.join(load_plugins)] + paths)
    append_python_path = [plugin_dir]
    if data_context().content.collection:
        append_python_path.append(data_context().content.collection.root)
    env = ansible_environment(args)
    env['PYTHONPATH'] += (os.path.pathsep + os.path.pathsep.join(append_python_path))
    if paths:
        display.info(('Checking %d file(s) in context "%s" with config: %s' % (len(paths), context, rcfile)), verbosity=1)
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
