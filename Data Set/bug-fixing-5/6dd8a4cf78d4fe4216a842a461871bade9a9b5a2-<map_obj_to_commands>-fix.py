def map_obj_to_commands(want, have, module):
    commands = list()
    if (module.params['state'] == 'absent'):
        if have:
            templatized_command = '%(ovs-vsctl)s -t %(timeout)s del-br %(bridge)s'
            command = (templatized_command % module.params)
            commands.append(command)
    elif have:
        if (want['fail_mode'] != have['fail_mode']):
            templatized_command = '%(ovs-vsctl)s -t %(timeout)s set-fail-mode %(bridge)s %(fail_mode)s'
            command = (templatized_command % module.params)
            commands.append(command)
        if (want['external_ids'] != have['external_ids']):
            templatized_command = '%(ovs-vsctl)s -t %(timeout)s br-set-external-id %(bridge)s'
            command = (templatized_command % module.params)
            if want['external_ids']:
                for (k, v) in iteritems(want['external_ids']):
                    if ((k not in have['external_ids']) or (want['external_ids'][k] != have['external_ids'][k])):
                        command += (((' ' + k) + ' ') + v)
                        commands.append(command)
    else:
        templatized_command = '%(ovs-vsctl)s -t %(timeout)s add-br %(bridge)s'
        command = (templatized_command % module.params)
        if want['parent']:
            templatized_command = '%(parent)s %(vlan)s'
            command += (' ' + (templatized_command % module.params))
        if want['set']:
            templatized_command = ' -- set %(set)s'
            command += (templatized_command % module.params)
        commands.append(command)
        if want['fail_mode']:
            templatized_command = '%(ovs-vsctl)s -t %(timeout)s set-fail-mode %(bridge)s %(fail_mode)s'
            command = (templatized_command % module.params)
            commands.append(command)
        if want['external_ids']:
            for (k, v) in iteritems(want['external_ids']):
                templatized_command = '%(ovs-vsctl)s -t %(timeout)s br-set-external-id %(bridge)s'
                command = (templatized_command % module.params)
                command += (((' ' + k) + ' ') + v)
                commands.append(command)
    return commands