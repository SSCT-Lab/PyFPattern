def command_integration_role(args, target, start_at_task):
    '\n    :type args: IntegrationConfig\n    :type target: IntegrationTarget\n    :type start_at_task: str\n    '
    display.info(('Running %s integration test role' % target.name))
    vars_file = 'integration_config.yml'
    if ('windows/' in target.aliases):
        inventory = 'inventory.winrm'
        hosts = 'windows'
        gather_facts = False
    elif ('network/' in target.aliases):
        inventory = 'inventory.networking'
        hosts = target.name[:target.name.find('_')]
        gather_facts = False
        if (hosts == 'net'):
            hosts = 'all'
    else:
        inventory = 'inventory'
        hosts = 'testhost'
        gather_facts = True
    playbook = ('\n- hosts: %s\n  gather_facts: %s\n  roles:\n    - { role: %s }\n    ' % (hosts, gather_facts, target.name))
    with tempfile.NamedTemporaryFile(dir='test/integration', prefix=('%s-' % target.name), suffix='.yml') as pb_fd:
        pb_fd.write(playbook.encode('utf-8'))
        pb_fd.flush()
        filename = os.path.basename(pb_fd.name)
        display.info(('>>> Playbook: %s\n%s' % (filename, playbook.strip())), verbosity=3)
        cmd = ['ansible-playbook', filename, '-i', inventory, '-e', ('@%s' % vars_file)]
        if start_at_task:
            cmd += ['--start-at-task', start_at_task]
        if args.verbosity:
            cmd.append(('-' + ('v' * args.verbosity)))
        env = integration_environment(args)
        cwd = 'test/integration'
        env['ANSIBLE_ROLES_PATH'] = os.path.abspath('test/integration/targets')
        intercept_command(args, cmd, env=env, cwd=cwd)