def main():
    module = AnsibleModule(argument_spec=dict(list_all=dict(required=False, type='bool', default=False), name=dict(type='str'), repo=dict(type='path'), scope=dict(required=False, type='str', choices=['local', 'global', 'system']), value=dict(required=False)), mutually_exclusive=[['list_all', 'name'], ['list_all', 'value']], required_if=[('scope', 'local', ['repo'])], required_one_of=[['list_all', 'name']], supports_check_mode=True)
    git_path = module.get_bin_path('git', True)
    params = module.params
    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')
    if params['name']:
        name = params['name']
    else:
        name = None
    if params['scope']:
        scope = params['scope']
    elif params['list_all']:
        scope = None
    else:
        scope = 'system'
    if params['value']:
        new_value = params['value']
    else:
        new_value = None
    args = [git_path, 'config', '--includes']
    if params['list_all']:
        args.append('-l')
    if scope:
        args.append(('--' + scope))
    if name:
        args.append(name)
    if (scope == 'local'):
        dir = params['repo']
    elif (params['list_all'] and params['repo']):
        dir = params['repo']
    else:
        dir = '/'
    (rc, out, err) = module.run_command(' '.join(args), cwd=dir)
    if (params['list_all'] and scope and (rc == 128) and ('unable to read config file' in err)):
        module.exit_json(changed=False, msg='', config_values={
            
        })
    elif (rc >= 2):
        module.fail_json(rc=rc, msg=err, cmd=' '.join(args))
    if params['list_all']:
        values = out.rstrip().splitlines()
        config_values = {
            
        }
        for value in values:
            (k, v) = value.split('=', 1)
            config_values[k] = v
        module.exit_json(changed=False, msg='', config_values=config_values)
    elif (not new_value):
        module.exit_json(changed=False, msg='', config_value=out.rstrip())
    else:
        old_value = out.rstrip()
        if (old_value == new_value):
            module.exit_json(changed=False, msg='')
    if (not module.check_mode):
        new_value_quoted = (("'" + new_value) + "'")
        (rc, out, err) = module.run_command(' '.join((args + [new_value_quoted])), cwd=dir)
        if err:
            module.fail_json(rc=rc, msg=err, cmd=' '.join((args + [new_value_quoted])))
    module.exit_json(msg='setting changed', diff=dict(before_header=' '.join(args), before=(old_value + '\n'), after_header=' '.join(args), after=(new_value + '\n')), changed=True)