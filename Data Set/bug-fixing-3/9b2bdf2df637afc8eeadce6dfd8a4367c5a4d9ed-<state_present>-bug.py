def state_present(module, existing, proposed):
    commands = list()
    parents = list()
    proposed_commands = apply_key_map(PARAM_TO_COMMAND_KEYMAP, proposed)
    existing_commands = apply_key_map(PARAM_TO_COMMAND_KEYMAP, existing)
    for (key, value) in proposed_commands.items():
        if key.startswith('route-target'):
            if (value == ['default']):
                existing_value = existing_commands.get(key)
                if existing_value:
                    for target in existing_value:
                        commands.append('no {0} {1}'.format(key, target))
            else:
                if (not isinstance(value, list)):
                    value = [value]
                for target in value:
                    if existing:
                        if (target not in existing.get(key.replace('-', '_').replace(' ', '_'))):
                            commands.append('{0} {1}'.format(key, target))
                    else:
                        commands.append('{0} {1}'.format(key, target))
        elif (value == 'default'):
            existing_value = existing_commands.get(key)
            if existing_value:
                commands.append('no {0} {1}'.format(key, existing_value))
        else:
            command = '{0} {1}'.format(key, value)
            commands.append(command)
    if commands:
        parents = ['evpn', 'vni {0} l2'.format(module.params['vni'])]
    return (commands, parents)