

def ensure(module, state, packages, params):
    response = {
        'results': [],
        'msg': '',
    }
    behaviour = {
        'present': {
            'filter': (lambda p: (not is_installed(module, p))),
            'subcommand': 'install',
        },
        'latest': {
            'filter': (lambda p: ((not is_installed(module, p)) or (not is_latest(module, p)))),
            'subcommand': 'install',
        },
        'absent': {
            'filter': (lambda p: is_installed(module, p)),
            'subcommand': 'uninstall',
        },
    }
    if module.check_mode:
        dry_run = ['-n']
    else:
        dry_run = []
    if params['accept_licenses']:
        accept_licenses = ['--accept']
    else:
        accept_licenses = []
    to_modify = filter(behaviour[state]['filter'], packages)
    if to_modify:
        (rc, out, err) = module.run_command(((((['pkg', behaviour[state]['subcommand']] + dry_run) + accept_licenses) + ['-q', '--']) + to_modify))
        response['rc'] = rc
        response['results'].append(out)
        response['msg'] += err
        response['changed'] = True
        if (rc == 4):
            response['changed'] = False
            response['failed'] = False
        elif (rc != 0):
            module.fail_json(**response)
    module.exit_json(**response)
