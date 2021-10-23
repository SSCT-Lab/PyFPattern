def map_obj_to_commands(updates, module):
    commands = list()
    (want, have) = updates
    for w in want:
        name = w['name']
        state = w['state']
        mode = w['mode']
        access_vlan = w['access_vlan']
        native_vlan = w['native_vlan']
        trunk_allowed_vlans = w['trunk_allowed_vlans']
        interface = ('interface ' + name)
        commands.append(interface)
        obj_in_have = search_obj_in_list(name, have)
        if (not obj_in_have):
            module.fail_json(msg='invalid interface {0}'.format(name))
        if (state == 'absent'):
            if (obj_in_have['mode'] == 'access'):
                commands.append('no switchport access vlan {0}'.format(obj_in_have['access_vlan']))
            if (obj_in_have['mode'] == 'trunk'):
                commands.append('no switchport mode trunk')
            if obj_in_have['native_vlan']:
                commands.append('no switchport trunk native vlan {0}'.format(obj_in_have['native_vlan']))
            if obj_in_have['trunk_allowed_vlans']:
                commands.append('no switchport trunk allowed vlan {0}'.format(obj_in_have['trunk_allowed_vlans']))
            if (obj_in_have['state'] == 'present'):
                commands.append('no switchport')
        elif (obj_in_have['state'] == 'absent'):
            commands.append('switchport')
            commands.append('switchport mode {0}'.format(mode))
            if access_vlan:
                commands.append('switchport access vlan {0}'.format(access_vlan))
            if native_vlan:
                commands.append('switchport trunk native vlan {0}'.format(native_vlan))
            if trunk_allowed_vlans:
                commands.append('switchport trunk allowed vlan {0}'.format(trunk_allowed_vlans))
        elif (mode != obj_in_have['mode']):
            if (obj_in_have['mode'] == 'access'):
                commands.append('no switchport access vlan {0}'.format(obj_in_have['access_vlan']))
                if native_vlan:
                    commands.append('switchport mode trunk')
                    commands.append('switchport trunk native vlan {0}'.format(native_vlan))
                if trunk_allowed_vlans:
                    commands.append('switchport mode trunk')
                    commands.append('switchport trunk allowed vlan {0}'.format(trunk_allowed_vlans))
            else:
                if obj_in_have['native_vlan']:
                    commands.append('no switchport trunk native vlan {0}'.format(obj_in_have['native_vlan']))
                    commands.append('no switchport mode trunk')
                if obj_in_have['trunk_allowed_vlans']:
                    commands.append('no switchport trunk allowed vlan {0}'.format(obj_in_have['trunk_allowed_vlans']))
                    commands.append('no switchport mode trunk')
                commands.append('switchport access vlan {0}'.format(access_vlan))
        elif (mode == 'access'):
            if (access_vlan != obj_in_have['access_vlan']):
                commands.append('switchport access vlan {0}'.format(access_vlan))
        else:
            if ((native_vlan != obj_in_have['native_vlan']) and native_vlan):
                commands.append('switchport trunk native vlan {0}'.format(native_vlan))
            if ((trunk_allowed_vlans != obj_in_have['trunk_allowed_vlans']) and trunk_allowed_vlans):
                commands.append('switchport trunk allowed vlan {0}'.format(trunk_allowed_vlans))
        if (commands[(- 1)] == interface):
            commands.pop((- 1))
    return commands