def get_hsrp_group(group, interface, module):
    command = 'show hsrp group {0} all | json'.format(group)
    hsrp = {
        
    }
    hsrp_key = {
        'sh_if_index': 'interface',
        'sh_group_num': 'group',
        'sh_group_version': 'version',
        'sh_cfg_prio': 'priority',
        'sh_preempt': 'preempt',
        'sh_vip': 'vip',
        'sh_authentication_type': 'auth_type',
        'sh_keystring_attr': 'auth_enc',
        'sh_authentication_data': 'auth_string',
    }
    try:
        body = run_commands(module, [command])[0]
        hsrp_table = body['TABLE_grp_detail']['ROW_grp_detail']
        if ('sh_keystring_attr' not in hsrp_table):
            del hsrp_key['sh_keystring_attr']
        if ('unknown enum:' in str(hsrp_table)):
            hsrp_table = get_hsrp_group_unknown_enum(module, command, hsrp_table)
    except (AttributeError, IndexError, TypeError, KeyError):
        return {
            
        }
    if isinstance(hsrp_table, dict):
        hsrp_table = [hsrp_table]
    for hsrp_group in hsrp_table:
        parsed_hsrp = apply_key_map(hsrp_key, hsrp_group)
        parsed_hsrp['interface'] = parsed_hsrp['interface'].lower()
        if (parsed_hsrp['version'] == 'v1'):
            parsed_hsrp['version'] = '1'
        elif (parsed_hsrp['version'] == 'v2'):
            parsed_hsrp['version'] = '2'
        if (parsed_hsrp['auth_type'] == 'md5'):
            if (parsed_hsrp['auth_enc'] == 'hidden'):
                parsed_hsrp['auth_enc'] = '7'
            else:
                parsed_hsrp['auth_enc'] = '0'
        if (parsed_hsrp['interface'] == interface):
            return parsed_hsrp
    return hsrp