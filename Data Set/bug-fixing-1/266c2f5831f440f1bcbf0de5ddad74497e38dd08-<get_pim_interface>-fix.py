

def get_pim_interface(module, interface):
    pim_interface = {
        
    }
    command = 'show ip pim interface {0}'.format(interface)
    body = execute_show_command(command, module, text=True)
    if body:
        if ('not running' not in body[0]):
            body = execute_show_command(command, module)
    try:
        get_data = body[0]['TABLE_vrf']['ROW_vrf']['TABLE_iod']['ROW_iod']
    except (KeyError, AttributeError, TypeError, IndexError):
        try:
            get_data = body[0]['TABLE_iod']['ROW_iod']
        except (KeyError, AttributeError, TypeError, IndexError):
            return pim_interface
    if isinstance(get_data.get('dr-priority'), list):
        pim_interface['dr_prio'] = get_data.get('dr-priority')[0]
    else:
        pim_interface['dr_prio'] = str(get_data.get('dr-priority'))
    hello_interval = get_data.get('hello-interval-sec')
    if hello_interval:
        hello_interval_msec = (int(get_data.get('hello-interval-sec')) * 1000)
        pim_interface['hello_interval'] = str(hello_interval_msec)
    border = get_data.get('is-border')
    border = (border.lower() if border else border)
    if (border == 'true'):
        pim_interface['border'] = True
    elif (border == 'false'):
        pim_interface['border'] = False
    isauth = get_data.get('isauth-config')
    isauth = (isauth.lower() if isauth else isauth)
    if (isauth == 'true'):
        pim_interface['isauth'] = True
    elif (isauth == 'false'):
        pim_interface['isauth'] = False
    pim_interface['neighbor_policy'] = get_data.get('nbr-policy-name')
    if (pim_interface['neighbor_policy'] == 'none configured'):
        pim_interface['neighbor_policy'] = None
    jp_in_policy = get_data.get('jp-in-policy-name')
    pim_interface['jp_policy_in'] = jp_in_policy
    if (jp_in_policy == 'none configured'):
        pim_interface['jp_policy_in'] = None
    pim_interface['jp_policy_out'] = get_jp_policy_out(module, interface)
    body = get_config(module, flags=['interface {0}'.format(interface)])
    jp_configs = []
    neigh = None
    if body:
        all_lines = body.splitlines()
        for each in all_lines:
            if ('jp-policy' in each):
                jp_configs.append(str(each.strip()))
            elif ('neighbor-policy' in each):
                neigh = str(each)
            elif ('sparse-mode' in each):
                pim_interface['sparse'] = True
    pim_interface['neighbor_type'] = None
    neigh_type = None
    if neigh:
        if ('prefix-list' in neigh):
            neigh_type = 'prefix'
        else:
            neigh_type = 'routemap'
    pim_interface['neighbor_type'] = neigh_type
    len_existing = len(jp_configs)
    list_of_prefix_type = len([x for x in jp_configs if ('prefix-list' in x)])
    jp_type_in = None
    jp_type_out = None
    jp_bidir = False
    if (len_existing == 1):
        last_word = jp_configs[0].split(' ')[(- 1)]
        if (last_word == 'in'):
            if list_of_prefix_type:
                jp_type_in = 'prefix'
            else:
                jp_type_in = 'routemap'
        elif (last_word == 'out'):
            if list_of_prefix_type:
                jp_type_out = 'prefix'
            else:
                jp_type_out = 'routemap'
        else:
            jp_bidir = True
            if list_of_prefix_type:
                jp_type_in = 'prefix'
                jp_type_out = 'routemap'
            else:
                jp_type_in = 'routemap'
                jp_type_out = 'routemap'
    else:
        for each in jp_configs:
            last_word = each.split(' ')[(- 1)]
            if (last_word == 'in'):
                if ('prefix-list' in each):
                    jp_type_in = 'prefix'
                else:
                    jp_type_in = 'routemap'
            elif (last_word == 'out'):
                if ('prefix-list' in each):
                    jp_type_out = 'prefix'
                else:
                    jp_type_out = 'routemap'
    pim_interface['jp_type_in'] = jp_type_in
    pim_interface['jp_type_out'] = jp_type_out
    pim_interface['jp_bidir'] = jp_bidir
    return pim_interface
