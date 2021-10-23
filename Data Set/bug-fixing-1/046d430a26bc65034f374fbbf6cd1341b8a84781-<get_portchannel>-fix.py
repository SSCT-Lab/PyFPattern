

def get_portchannel(module, netcfg=None):
    command = 'show port-channel summary'
    portchannel = {
        
    }
    portchannel_table = {
        
    }
    members = []
    try:
        body = execute_show_command(command, module)[0]
        pc_table = body['TABLE_channel']['ROW_channel']
        if isinstance(pc_table, dict):
            pc_table = [pc_table]
        for pc in pc_table:
            if (pc['group'] == module.params['group']):
                portchannel_table = pc
            elif (module.params['group'].isdigit() and (pc['group'] == int(module.params['group']))):
                portchannel_table = pc
    except (KeyError, AttributeError, TypeError, IndexError):
        return {
            
        }
    if portchannel_table:
        portchannel['group'] = portchannel_table['group']
        protocol = portchannel_table['prtcl']
        members_list = get_portchannel_members(portchannel_table)
        if isinstance(members_list, dict):
            members_list = [members_list]
        member_dictionary = {
            
        }
        for each_member in members_list:
            interface = each_member['port']
            members.append(interface)
            pc_member = {
                
            }
            pc_member['status'] = str(each_member['port-status'])
            pc_member['mode'] = get_portchannel_mode(interface, protocol, module, netcfg)
            member_dictionary[interface] = pc_member
            portchannel['members'] = members
            portchannel['members_detail'] = member_dictionary
        modes = set()
        for (each, value) in member_dictionary.items():
            modes.update([value['mode']])
        if (len(modes) == 1):
            portchannel['mode'] = value['mode']
        else:
            portchannel['mode'] = 'unknown'
    return portchannel
