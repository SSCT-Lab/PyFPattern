

def ansible_environment(args, color=True):
    '\n    :type args: CommonConfig\n    :type color: bool\n    :rtype: dict[str, str]\n    '
    env = common_environment()
    path = env['PATH']
    ansible_path = os.path.join(os.getcwd(), 'bin')
    if (not path.startswith((ansible_path + os.path.pathsep))):
        path = ((ansible_path + os.path.pathsep) + path)
    if isinstance(args, IntegrationConfig):
        ansible_config = ('test/integration/%s.cfg' % args.command)
    else:
        ansible_config = ('test/%s/ansible.cfg' % args.command)
    if (not os.path.exists(ansible_config)):
        raise ApplicationError(('Configuration not found: %s' % ansible_config))
    ansible = dict(ANSIBLE_FORCE_COLOR=(('%s' % 'true') if (args.color and color) else 'false'), ANSIBLE_DEPRECATION_WARNINGS='false', ANSIBLE_HOST_KEY_CHECKING='false', ANSIBLE_CONFIG=os.path.abspath(ansible_config), ANSIBLE_LIBRARY='/dev/null', PYTHONPATH=os.path.abspath('lib'), PAGER='/bin/cat', PATH=path)
    env.update(ansible)
    if args.debug:
        env.update(dict(ANSIBLE_DEBUG='true', ANSIBLE_LOG_PATH=os.path.abspath('test/results/logs/debug.log')))
    return env
