def state_present(module, existing, proposed, candidate):
    commands = list()
    proposed_commands = apply_key_map(PARAM_TO_COMMAND_KEYMAP, proposed)
    existing_commands = apply_key_map(PARAM_TO_COMMAND_KEYMAP, existing)
    for (key, value) in proposed_commands.items():
        if (key == 'vrf'):
            continue
        if (value is True):
            commands.append(key)
        elif (value is False):
            if (key == 'passive-interface default'):
                if existing_commands.get(key):
                    commands.append('no {0}'.format(key))
            else:
                commands.append('no {0}'.format(key))
        elif ((value == 'default') or (value == '')):
            if (key == 'log-adjacency-changes'):
                commands.append('no {0}'.format(key))
            elif existing_commands.get(key):
                existing_value = existing_commands.get(key)
                commands.append('no {0} {1}'.format(key, existing_value))
        else:
            if (key == 'timers throttle lsa'):
                command = '{0} {1} {2} {3}'.format(key, get_timer_prd('timer_throttle_lsa_start', proposed), get_timer_prd('timer_throttle_lsa_hold', proposed), get_timer_prd('timer_throttle_lsa_max', proposed))
            elif (key == 'timers throttle spf'):
                command = '{0} {1} {2} {3}'.format(key, get_timer_prd('timer_throttle_spf_start', proposed), get_timer_prd('timer_throttle_spf_hold', proposed), get_timer_prd('timer_throttle_spf_max', proposed))
            elif (key == 'log-adjacency-changes'):
                if (value == 'log'):
                    command = key
                elif (value == 'detail'):
                    command = '{0} {1}'.format(key, value)
            elif (key == 'auto-cost reference-bandwidth'):
                if (len(value) < 5):
                    command = '{0} {1} Mbps'.format(key, value)
                else:
                    value = str((int(value) // 1000))
                    command = '{0} {1} Gbps'.format(key, value)
            elif (key == 'bfd'):
                command = ('no bfd' if (value == 'disable') else 'bfd')
            else:
                command = '{0} {1}'.format(key, value.lower())
            if (command not in commands):
                commands.append(command)
    if commands:
        parents = ['router ospf {0}'.format(module.params['ospf'])]
        if (module.params['vrf'] != 'default'):
            parents.append('vrf {0}'.format(module.params['vrf']))
        candidate.add(commands, parents=parents)