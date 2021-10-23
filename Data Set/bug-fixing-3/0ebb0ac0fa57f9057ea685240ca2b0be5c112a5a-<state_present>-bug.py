def state_present(module, existing, proposed, candidate):
    commands = list()
    proposed_commands = apply_key_map(PARAM_TO_COMMAND_KEYMAP, proposed)
    existing_commands = apply_key_map(PARAM_TO_COMMAND_KEYMAP, existing)
    for (key, value) in proposed_commands.items():
        if (key == 'associate-vrf'):
            command = 'member vni {0} {1}'.format(module.params['vni'], key)
            if (not value):
                command = 'no {0}'.format(command)
            commands.append(command)
        elif ((key == 'peer-ip') and (value != [])):
            for peer in value:
                commands.append('{0} {1}'.format(key, peer))
        elif ((key == 'mcast-group') and (value != existing_commands.get(key))):
            commands.append('no {0}'.format(key))
            vni_command = 'member vni {0}'.format(module.params['vni'])
            if (vni_command not in commands):
                commands.append('member vni {0}'.format(module.params['vni']))
            if (value != PARAM_TO_DEFAULT_KEYMAP.get('multicast_group', 'default')):
                commands.append('{0} {1}'.format(key, value))
        elif ((key == 'ingress-replication protocol') and (value != existing_commands.get(key))):
            evalue = existing_commands.get(key)
            dvalue = PARAM_TO_DEFAULT_KEYMAP.get('ingress_replication', 'default')
            if (value != dvalue):
                if (evalue and (evalue != dvalue)):
                    commands.append('no {0} {1}'.format(key, evalue))
                commands.append('{0} {1}'.format(key, value))
            elif evalue:
                commands.append('no {0} {1}'.format(key, evalue))
        elif (value is True):
            commands.append(key)
        elif (value is False):
            commands.append('no {0}'.format(key))
        elif ((value == 'default') or (value == [])):
            if existing_commands.get(key):
                existing_value = existing_commands.get(key)
                if (key == 'peer-ip'):
                    for peer in existing_value:
                        commands.append('no {0} {1}'.format(key, peer))
                else:
                    commands.append('no {0} {1}'.format(key, existing_value))
            elif (key.replace(' ', '_').replace('-', '_') in BOOL_PARAMS):
                commands.append('no {0}'.format(key.lower()))
        else:
            command = '{0} {1}'.format(key, value.lower())
            commands.append(command)
    if commands:
        vni_command = 'member vni {0}'.format(module.params['vni'])
        ingress_replications_command = 'ingress-replication protocol static'
        ingress_replicationb_command = 'ingress-replication protocol bgp'
        ingress_replicationns_command = 'no ingress-replication protocol static'
        ingress_replicationnb_command = 'no ingress-replication protocol bgp'
        interface_command = 'interface {0}'.format(module.params['interface'])
        if any(((c in commands) for c in (ingress_replications_command, ingress_replicationb_command, ingress_replicationnb_command, ingress_replicationns_command))):
            static_level_cmds = [cmd for cmd in commands if ('peer' in cmd)]
            parents = [interface_command, vni_command]
            for cmd in commands:
                parents.append(cmd)
            candidate.add(static_level_cmds, parents=parents)
            commands = [cmd for cmd in commands if ('peer' not in cmd)]
        elif ('peer-ip' in commands[0]):
            static_level_cmds = [cmd for cmd in commands]
            parents = [interface_command, vni_command, ingress_replications_command]
            candidate.add(static_level_cmds, parents=parents)
        if (vni_command in commands):
            parents = [interface_command]
            commands.remove(vni_command)
            if (module.params['assoc_vrf'] is None):
                parents.append(vni_command)
            candidate.add(commands, parents=parents)