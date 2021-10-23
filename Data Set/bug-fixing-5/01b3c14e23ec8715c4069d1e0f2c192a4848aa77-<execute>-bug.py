def execute(module):
    state = module.params.get('state')
    if ((state == 'acquire') or (state == 'release')):
        lock(module, state)
    if (state == 'present'):
        add_value(module)
    else:
        remove_value(module)