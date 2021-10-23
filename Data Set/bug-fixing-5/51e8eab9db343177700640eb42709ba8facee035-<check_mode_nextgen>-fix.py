def check_mode_nextgen(module, issu, image, kick=None):
    "Use the 'install all impact' command for check_mode"
    opts = {
        'ignore_timeout': True,
    }
    commands = build_install_cmd_set(issu, image, kick, 'impact')
    data = parse_show_install(load_config(module, commands, True, opts))
    if (data['error'] and (issu == 'desired')):
        issu = 'no'
        commands = build_install_cmd_set(issu, image, kick, 'impact')
        data = check_install_in_progress(module, commands, opts)
    if data['server_error']:
        data['error'] = True
    return data