def state_present(module, existing, proposed, candidate):
    commands = list()
    proposed_commands = apply_key_map(PARAM_TO_COMMAND_KEYMAP, proposed)
    existing_commands = apply_key_map(PARAM_TO_COMMAND_KEYMAP, existing)
    for (key, value) in proposed_commands.items():
        if (value is True):
            commands.append(key)
        elif (value is False):
            commands.append('no {0}'.format(key))
        elif (value == 'default'):
            if existing_commands.get(key):
                existing_value = existing_commands.get(key)
                commands.append('no {0} {1}'.format(key, existing_value))
        elif (key == 'log-neighbor-changes'):
            if (value == 'enable'):
                commands.append('{0}'.format(key))
            elif (value == 'disable'):
                commands.append('{0} {1}'.format(key, value))
            elif (value == 'inherit'):
                if existing_commands.get(key):
                    commands.append('no {0}'.format(key))
        elif (key == 'password'):
            pwd_type = module.params['pwd_type']
            if (pwd_type == '3des'):
                pwd_type = 3
            else:
                pwd_type = 7
            command = '{0} {1} {2}'.format(key, pwd_type, value)
            if (command not in commands):
                commands.append(command)
        elif (key == 'remove-private-as'):
            if (value == 'enable'):
                command = '{0}'.format(key)
                commands.append(command)
            elif (value == 'disable'):
                if (existing_commands.get(key) != 'disable'):
                    command = 'no {0}'.format(key)
                    commands.append(command)
            else:
                command = '{0} {1}'.format(key, value)
                commands.append(command)
        elif (key == 'timers'):
            command = 'timers {0} {1}'.format(proposed['timers_keepalive'], proposed['timers_holdtime'])
            if (command not in commands):
                commands.append(command)
        else:
            command = '{0} {1}'.format(key, value)
            commands.append(command)
    if commands:
        parents = ['router bgp {0}'.format(module.params['asn'])]
        if (module.params['vrf'] != 'default'):
            parents.append('vrf {0}'.format(module.params['vrf']))
        parents.append('neighbor {0}'.format(module.params['neighbor']))
        local_as_command = 'local-as {0}'.format(module.params['local_as'])
        if (local_as_command in commands):
            commands.remove(local_as_command)
            commands.append(local_as_command)
        candidate.add(commands, parents=parents)