def map_obj_to_commands(updates, module):
    (want, have) = updates
    commands = list()
    if (want['state'] == 'absent'):
        if (have['state'] == 'present'):
            commands.append('delete system services netconf')
    elif ((have['state'] == 'absent') or (want['netconf_port'] != have.get('netconf_port'))):
        commands.append(('set system services netconf ssh port %s' % want['netconf_port']))
    return commands