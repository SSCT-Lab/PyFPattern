def get_acl(module, acl_name, seq_number):
    command = 'show ip access-list'
    new_acl = []
    saveme = {
        
    }
    acl_body = {
        
    }
    body = execute_show_command(command, module)[0]
    if body:
        all_acl_body = body['TABLE_ip_ipv6_mac']['ROW_ip_ipv6_mac']
    else:
        return ({
            
        }, [])
    if isinstance(all_acl_body, dict):
        if (all_acl_body.get('acl_name') == acl_name):
            acl_body = all_acl_body
    else:
        for acl in all_acl_body:
            if (acl.get('acl_name') == acl_name):
                acl_body = acl
    try:
        acl_entries = acl_body['TABLE_seqno']['ROW_seqno']
        acl_name = acl_body.get('acl_name')
    except KeyError:
        return ({
            
        }, [{
            'acl': 'no_entries',
        }])
    if isinstance(acl_entries, dict):
        acl_entries = [acl_entries]
    for each in acl_entries:
        temp = {
            
        }
        options = {
            
        }
        remark = each.get('remark')
        temp['name'] = acl_name
        temp['seq'] = str(each.get('seqno'))
        if remark:
            temp['remark'] = remark
            temp['action'] = 'remark'
        else:
            temp['action'] = each.get('permitdeny')
            temp['proto'] = each.get('proto', each.get('proto_str', each.get('ip')))
            temp['src'] = each.get('src_any', each.get('src_ip_prefix'))
            temp['src_port_op'] = each.get('src_port_op')
            temp['src_port1'] = each.get('src_port1_num')
            temp['src_port2'] = each.get('src_port2_num')
            temp['dest'] = each.get('dest_any', each.get('dest_ip_prefix'))
            temp['dest_port_op'] = each.get('dest_port_op')
            temp['dest_port1'] = each.get('dest_port1_num')
            temp['dest_port2'] = each.get('dest_port2_num')
            options['log'] = each.get('log')
            options['urg'] = each.get('urg')
            options['ack'] = each.get('ack')
            options['psh'] = each.get('psh')
            options['rst'] = each.get('rst')
            options['syn'] = each.get('syn')
            options['fin'] = each.get('fin')
            options['established'] = each.get('established')
            options['dscp'] = each.get('dscp_str')
            options['precedence'] = each.get('precedence_str')
            options['fragments'] = each.get('fragments')
            options['time_range'] = each.get('timerange')
        keep = {
            
        }
        for (key, value) in temp.items():
            if value:
                keep[key] = value
        options_no_null = {
            
        }
        for (key, value) in options.items():
            if (value is not None):
                options_no_null[key] = value
        keep['options'] = options_no_null
        if (keep.get('seq') == seq_number):
            saveme = dict(keep)
        new_acl.append(keep)
    return (saveme, new_acl)