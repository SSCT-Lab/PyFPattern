

def command_integration_role(args, target, start_at_task, test_dir, inventory_path, temp_path):
    '\n    :type args: IntegrationConfig\n    :type target: IntegrationTarget\n    :type start_at_task: str | None\n    :type test_dir: str\n    :type inventory_path: str\n    :type temp_path: str\n    '
    display.info(('Running %s integration test role' % target.name))
    env_config = None
    vars_files = []
    variables = dict(output_dir=test_dir)
    if isinstance(args, WindowsIntegrationConfig):
        hosts = 'windows'
        gather_facts = False
        variables.update(dict(win_output_dir='C:\\ansible_testing'))
    elif isinstance(args, NetworkIntegrationConfig):
        hosts = target.name[:target.name.find('_')]
        gather_facts = False
    else:
        hosts = 'testhost'
        gather_facts = True
        cloud_environment = get_cloud_environment(args, target)
        if cloud_environment:
            env_config = cloud_environment.get_environment_config()
    with integration_test_environment(args, target, inventory_path) as test_env:
        if os.path.exists(test_env.vars_file):
            vars_files.append(os.path.relpath(test_env.vars_file, test_env.integration_dir))
        play = dict(hosts=hosts, gather_facts=gather_facts, vars_files=vars_files, vars=variables, roles=[target.name])
        if env_config:
            if env_config.ansible_vars:
                variables.update(env_config.ansible_vars)
            play.update(dict(environment=env_config.env_vars, module_defaults=env_config.module_defaults))
        playbook = json.dumps([play], indent=4, sort_keys=True)
        with named_temporary_file(args=args, directory=test_env.integration_dir, prefix=('%s-' % target.name), suffix='.yml', content=playbook) as playbook_path:
            filename = os.path.basename(playbook_path)
            display.info(('>>> Playbook: %s\n%s' % (filename, playbook.strip())), verbosity=3)
            cmd = ['ansible-playbook', filename, '-i', os.path.relpath(test_env.inventory_path, test_env.integration_dir)]
            if start_at_task:
                cmd += ['--start-at-task', start_at_task]
            if args.tags:
                cmd += ['--tags', args.tags]
            if args.skip_tags:
                cmd += ['--skip-tags', args.skip_tags]
            if args.diff:
                cmd += ['--diff']
            if isinstance(args, NetworkIntegrationConfig):
                if args.testcase:
                    cmd += ['-e', ('testcase=%s' % args.testcase)]
            if args.verbosity:
                cmd.append(('-' + ('v' * args.verbosity)))
            env = integration_environment(args, target, test_dir, test_env.inventory_path, test_env.ansible_config, env_config)
            cwd = test_env.integration_dir
            env['ANSIBLE_ROLES_PATH'] = os.path.abspath(os.path.join(test_env.integration_dir, 'targets'))
            module_coverage = ('non_local/' not in target.aliases)
            intercept_command(args, cmd, target_name=target.name, env=env, cwd=cwd, temp_path=temp_path, module_coverage=module_coverage)
