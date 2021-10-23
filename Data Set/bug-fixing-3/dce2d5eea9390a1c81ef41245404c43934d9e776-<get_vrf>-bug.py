def get_vrf(vrf, module):
    command = 'show vrf {0}'.format(vrf)
    vrf_key = {
        'vrf_name': 'vrf',
        'vrf_state': 'admin_state',
    }
    body = execute_show_command(command, module)
    try:
        vrf_table = body[0]['TABLE_vrf']['ROW_vrf']
    except (TypeError, IndexError):
        return {
            
        }
    parsed_vrf = apply_key_map(vrf_key, vrf_table)
    command = 'show run all | section vrf.context.{0}'.format(vrf)
    body = execute_show_command(command, module, 'cli_show_ascii')
    extra_params = ['vni', 'rd', 'description']
    for param in extra_params:
        parsed_vrf[param] = get_value(param, body[0], module)
    return parsed_vrf