def main():
    command_allowed_param_map = dict(cleanup=(), createcachetable=('cache_table', 'database'), flush=('database',), loaddata=('database', 'fixtures'), syncdb=('database',), test=('failfast', 'testrunner', 'liveserver', 'apps'), validate=(), migrate=('apps', 'skip', 'merge', 'database'), collectstatic=('clear', 'link'))
    command_required_param_map = dict(loaddata=('fixtures',))
    noinput_commands = ('flush', 'syncdb', 'migrate', 'test', 'collectstatic')
    specific_params = ('apps', 'clear', 'database', 'failfast', 'fixtures', 'liveserver', 'testrunner')
    general_params = ('settings', 'pythonpath', 'database')
    specific_boolean_params = ('clear', 'failfast', 'skip', 'merge', 'link')
    end_of_command_params = ('apps', 'cache_table', 'fixtures')
    module = AnsibleModule(argument_spec=dict(command=dict(default=None, required=True), app_path=dict(default=None, required=True), settings=dict(default=None, required=False), pythonpath=dict(default=None, required=False, aliases=['python_path']), virtualenv=dict(default=None, required=False, aliases=['virtual_env']), apps=dict(default=None, required=False), cache_table=dict(default=None, required=False), clear=dict(default=None, required=False, type='bool'), database=dict(default=None, required=False), failfast=dict(default='no', required=False, type='bool', aliases=['fail_fast']), fixtures=dict(default=None, required=False), liveserver=dict(default=None, required=False, aliases=['live_server']), testrunner=dict(default=None, required=False, aliases=['test_runner']), skip=dict(default=None, required=False, type='bool'), merge=dict(default=None, required=False, type='bool'), link=dict(default=None, required=False, type='bool')))
    command = module.params['command']
    app_path = os.path.expanduser(module.params['app_path'])
    virtualenv = module.params['virtualenv']
    for param in specific_params:
        value = module.params[param]
        if (param in specific_boolean_params):
            value = module.boolean(value)
        if (value and (param not in command_allowed_param_map[command])):
            module.fail_json(msg=('%s param is incompatible with command=%s' % (param, command)))
    for param in command_required_param_map.get(command, ()):
        if (not module.params[param]):
            module.fail_json(msg=('%s param is required for command=%s' % (param, command)))
    _ensure_virtualenv(module)
    cmd = ('./manage.py %s' % (command,))
    if (command in noinput_commands):
        cmd = ('%s --noinput' % cmd)
    for param in general_params:
        if module.params[param]:
            cmd = ('%s --%s=%s' % (cmd, param, module.params[param]))
    for param in specific_boolean_params:
        if module.boolean(module.params[param]):
            cmd = ('%s --%s' % (cmd, param))
    for param in end_of_command_params:
        if module.params[param]:
            cmd = ('%s %s' % (cmd, module.params[param]))
    (rc, out, err) = module.run_command(cmd, cwd=os.path.expanduser(app_path))
    if (rc != 0):
        if ((command == 'createcachetable') and ('table' in err) and ('already exists' in err)):
            out = 'Already exists.'
        else:
            if ('Unknown command:' in err):
                _fail(module, cmd, err, ('Unknown django command: %s' % command))
            _fail(module, cmd, out, err, path=os.environ['PATH'], syspath=sys.path)
    changed = False
    lines = out.split('\n')
    filt = globals().get((command + '_filter_output'), None)
    if filt:
        filtered_output = filter(filt, lines)
        if len(filtered_output):
            changed = filtered_output
    module.exit_json(changed=changed, out=out, cmd=cmd, app_path=app_path, virtualenv=virtualenv, settings=module.params['settings'], pythonpath=module.params['pythonpath'])