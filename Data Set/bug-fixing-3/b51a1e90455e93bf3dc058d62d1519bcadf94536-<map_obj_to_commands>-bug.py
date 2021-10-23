def map_obj_to_commands(updates, module):
    (want, have) = updates
    commands = list()
    if ((want['state'] == 'present') and (have['state'] == 'absent')):
        commands.append(('set system services netconf ssh port %s' % want['netconf_port']))
    elif ((want['state'] == 'absent') and (have['state'] == 'present')):
        commands.append('delete system services netconf')
    elif (want['state'] == 'present'):
        if (want['netconf_port'] != have.get('netconf_port')):
            commands.append(('set system services netconf ssh port %s' % want['netconf_port']))
    return commands