def get_udld_global(module):
    command = 'show udld global | json'
    udld_table = run_commands(module, [command])[0]
    status = str(udld_table.get('udld-global-mode', None))
    if (status == 'enabled-aggressive'):
        aggressive = 'enabled'
    else:
        aggressive = 'disabled'
    interval = str(udld_table.get('message-interval', None))
    udld = dict(msg_time=interval, aggressive=aggressive)
    return udld