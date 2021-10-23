def map_obj_to_commands(updates, module):
    commands = list()
    commands2 = list()
    (want, have) = updates
    args = ('speed', 'description', 'duplex', 'mtu')
    for w in want:
        name = w['name']
        mode = w['mode']
        ip_forward = w['ip_forward']
        fabric_forwarding_anycast_gateway = w['fabric_forwarding_anycast_gateway']
        admin_state = w['admin_state']
        state = w['state']
        interface_type = w['interface_type']
        del w['state']
        if name:
            w['interface_type'] = None
        if interface_type:
            obj_in_have = {
                
            }
            if (state in ('present', 'default')):
                module.fail_json(msg='The interface_type param can be used only with state absent.')
        else:
            obj_in_have = search_obj_in_list(name, have)
            is_default = is_default_interface(name, module)
        if name:
            interface = ('interface ' + name)
        if (state == 'absent'):
            if obj_in_have:
                commands.append('no interface {0}'.format(name))
            elif (interface_type and (not obj_in_have)):
                intfs = get_interfaces_dict(module)[interface_type]
                cmds = get_interface_type_removed_cmds(intfs)
                commands.extend(cmds)
        elif (state == 'present'):
            if obj_in_have:
                if (get_interface_type(name) in ('ethernet', 'portchannel')):
                    if ((mode == 'layer2') and (mode != obj_in_have.get('mode'))):
                        add_command_to_interface(interface, 'switchport', commands)
                    elif ((mode == 'layer3') and (mode != obj_in_have.get('mode'))):
                        add_command_to_interface(interface, 'no switchport', commands)
                if ((admin_state == 'up') and (admin_state != obj_in_have.get('admin_state'))):
                    add_command_to_interface(interface, 'no shutdown', commands)
                elif ((admin_state == 'down') and (admin_state != obj_in_have.get('admin_state'))):
                    add_command_to_interface(interface, 'shutdown', commands)
                if ((ip_forward == 'enable') and (ip_forward != obj_in_have.get('ip_forward'))):
                    add_command_to_interface(interface, 'ip forward', commands)
                elif ((ip_forward == 'disable') and (ip_forward != obj_in_have.get('ip forward'))):
                    add_command_to_interface(interface, 'no ip forward', commands)
                if ((fabric_forwarding_anycast_gateway is True) and (obj_in_have.get('fabric_forwarding_anycast_gateway') is False)):
                    add_command_to_interface(interface, 'fabric forwarding mode anycast-gateway', commands)
                elif ((fabric_forwarding_anycast_gateway is False) and (obj_in_have.get('fabric_forwarding_anycast_gateway') is True)):
                    add_command_to_interface(interface, 'no fabric forwarding mode anycast-gateway', commands)
                for item in args:
                    candidate = w.get(item)
                    if (candidate and (candidate != obj_in_have.get(item))):
                        cmd = ((item + ' ') + str(candidate))
                        add_command_to_interface(interface, cmd, commands)
                if (name and (get_interface_type(name) == 'ethernet')):
                    if (mode != obj_in_have.get('mode')):
                        admin_state = (w.get('admin_state') or obj_in_have.get('admin_state'))
                        if admin_state:
                            c1 = 'interface {0}'.format(normalize_interface(w['name']))
                            c2 = get_admin_state(admin_state)
                            commands2.append(c1)
                            commands2.append(c2)
            else:
                commands.append(interface)
                if (get_interface_type(name) in ('ethernet', 'portchannel')):
                    if (mode == 'layer2'):
                        commands.append('switchport')
                    elif (mode == 'layer3'):
                        commands.append('no switchport')
                if (admin_state == 'up'):
                    commands.append('no shutdown')
                elif (admin_state == 'down'):
                    commands.append('shutdown')
                if (ip_forward == 'enable'):
                    commands.append('ip forward')
                elif (ip_forward == 'disable'):
                    commands.append('no ip forward')
                if (fabric_forwarding_anycast_gateway is True):
                    commands.append('fabric forwarding mode anycast-gateway')
                elif (fabric_forwarding_anycast_gateway is False):
                    commands.append('no fabric forwarding mode anycast-gateway')
                for item in args:
                    candidate = w.get(item)
                    if candidate:
                        commands.append(((item + ' ') + str(candidate)))
        elif (state == 'default'):
            if (is_default is False):
                commands.append('default interface {0}'.format(name))
            elif (is_default == 'DNE'):
                module.exit_json(msg='interface you are trying to default does not exist')
    return (commands, commands2)