

def command_integration_role(args, target, start_at_task):
    '\n    :type args: IntegrationConfig\n    :type target: IntegrationTarget\n    :type start_at_task: str\n    '
    display.info(('Running %s integration test role' % target.name))
    vars_file = 'integration_config.yml'
    if isinstance(args, WindowsIntegrationConfig):
        inventory = 'inventory.winrm'
        hosts = 'windows'
        gather_facts = False
    elif isinstance(args, NetworkIntegrationConfig):
        inventory = (args.inventory or 'inventory.networking')
        hosts = target.name[:target.name.find('_')]
        gather_facts = False
    else:
        inventory = 'inventory'
        hosts = 'testhost'
        gather_facts = True
        cloud_environment = get_cloud_environment(args, target)
        if cloud_environment:
            hosts = (cloud_environment.inventory_hosts or hosts)
    playbook = ('\n- hosts: %s\n  gather_facts: %s\n  roles:\n    - { role: %s }\n    ' % (hosts, gather_facts, target.name))
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
        if args.verbosity:
            cmd.append(('-' + ('v' * args.verbosity)))
        env = integration_environment(args, target, cmd)
        cwd = 'test/integration'
        env['ANSIBLE_ROLES_PATH'] = os.path.abspath('test/integration/targets')
        intercept_command(args, cmd, target_name=target.name, env=env, cwd=cwd)
