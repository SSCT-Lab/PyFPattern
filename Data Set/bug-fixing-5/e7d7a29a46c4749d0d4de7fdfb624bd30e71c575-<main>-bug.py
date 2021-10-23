def main():
    module = AnsibleModule(argument_spec=dict(command=dict(default='install', type='str', required=False), arguments=dict(default='', type='str', required=False), executable=dict(type='path', required=False, aliases=['php_path']), working_dir=dict(type='path', aliases=['working-dir']), global_command=dict(default=False, type='bool', aliases=['global-command']), prefer_source=dict(default=False, type='bool', aliases=['prefer-source']), prefer_dist=dict(default=False, type='bool', aliases=['prefer-dist']), no_dev=dict(default=True, type='bool', aliases=['no-dev']), no_scripts=dict(default=False, type='bool', aliases=['no-scripts']), no_plugins=dict(default=False, type='bool', aliases=['no-plugins']), optimize_autoloader=dict(default=True, type='bool', aliases=['optimize-autoloader']), ignore_platform_reqs=dict(default=False, type='bool', aliases=['ignore-platform-reqs'])), required_if=[('global_command', False, ['working_dir'])], supports_check_mode=True)
    command = module.params['command']
    if re.search('\\s', command):
        module.fail_json(msg="Use the 'arguments' param for passing arguments with the 'command'")
    arguments = module.params['arguments']
    global_command = module.params['global_command']
    available_options = get_available_options(module=module, command=command)
    options = []
    default_options = ['no-ansi', 'no-interaction', 'no-progress']
    for option in default_options:
        if (option in available_options):
            option = ('--%s' % option)
            options.append(option)
    if (not global_command):
        options.extend(['--working-dir', ("'%s'" % module.params['working_dir'])])
    option_params = {
        'prefer_source': 'prefer-source',
        'prefer_dist': 'prefer-dist',
        'no_dev': 'no-dev',
        'no_scripts': 'no-scripts',
        'no_plugins': 'no_plugins',
        'optimize_autoloader': 'optimize-autoloader',
        'ignore_platform_reqs': 'ignore-platform-reqs',
    }
    for (param, option) in option_params.items():
        if (module.params.get(param) and (option in available_options)):
            option = ('--%s' % option)
            options.append(option)
    if module.check_mode:
        options.append('--dry-run')
    (rc, out, err) = composer_command(module, command, arguments, options, global_command)
    if (rc != 0):
        output = parse_out(err)
        module.fail_json(msg=output, stdout=err)
    else:
        output = parse_out((out + err))
        module.exit_json(changed=has_changed(output), msg=output, stdout=(out + err))