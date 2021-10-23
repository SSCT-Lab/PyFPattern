def execute(module):
    state = module.params.get('state')
    if ((state == 'acquire') or (state == 'release')):
        lock(module, state)
    elif (state == 'present'):
        if (module.params.get('value') is NOT_SET):
            get_value(module)
        else:
            set_value(module)
    elif (state == 'absent'):
        remove_value(module)
    else:
        module.exit_json(msg=('Unsupported state: %s' % (state,)))