def command_integration_role(args, target, start_at_task, test_dir, inventory_path):
    '\n    :type args: IntegrationConfig\n    :type target: IntegrationTarget\n    :type start_at_task: str | None\n    :type test_dir: str\n    :type inventory_path: str\n    '
    display.info(('Running %s integration test role' % target.name))
    vars_file = 'integration_config.yml'
    if isinstance(args, WindowsIntegrationConfig):
        hosts = 'windows'
        gather_facts = False
    elif isinstance(args, NetworkIntegrationConfig):
        hosts = target.name[:target.name.find('_')]
        gather_facts = False
    else:
        hosts = 'testhost'
        gather_facts = True
        cloud_environment = get_cloud_environment(args, target)
        if cloud_environment:
            hosts = (cloud_environment.inventory_hosts or hosts)
    playbook = ('\n- hosts: %s\n  gather_facts: %s\n  roles:\n    - { role: %s }\n    ' % (hosts, gather_facts, target.name))
    inventory = os.path.relpath(inventory_path, 'test/integration')
    if ('/' in inventory):
        inventory = inventory_path
    with tempfile.NamedTemporaryFile(dir='test/integration', prefix=('%s-' % target.name), suffix='.yml') as pb_fd:
        pb_fd.write(playbook.encode('utf-8'))
        pb_fd.flush()
        filename = os.path.basename(pb_fd.name)
        display.info(('>>> Playbook: %s\n%s' % (filename, playbook.strip())), verbosity=3)
        cmd = ['ansible-playbook', filename, '-i', inventory, '-e', ('@%s' % vars_file)]
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
        env = integration_environment(args, target, cmd, test_dir, inventory_path)
        cwd = 'test/integration'
        env['ANSIBLE_ROLES_PATH'] = os.path.abspath('test/integration/targets')
        intercept_command(args, cmd, target_name=target.name, env=env, cwd=cwd)