

def get_vpc(module):
    body = run_commands(module, ['show vpc | json'])[0]
    domain = str(body['vpc-domain-id'])
    vpc = {
        
    }
    if (domain != 'not configured'):
        run = get_config(module, flags=['vpc'])
        if run:
            vpc['domain'] = domain
            for key in PARAM_TO_DEFAULT_KEYMAP.keys():
                vpc[key] = PARAM_TO_DEFAULT_KEYMAP.get(key)
            vpc['auto_recovery'] = get_auto_recovery_default(module)
            vpc_list = run.split('\n')
            for each in vpc_list:
                if ('role priority' in each):
                    line = each.split()
                    vpc['role_priority'] = line[(- 1)]
                if ('system-priority' in each):
                    line = each.split()
                    vpc['system_priority'] = line[(- 1)]
                if ('delay restore' in each):
                    line = each.split()
                    vpc['delay_restore'] = line[(- 1)]
                if ('no auto-recovery' in each):
                    vpc['auto_recovery'] = False
                elif ('auto-recovery' in each):
                    vpc['auto_recovery'] = True
                if ('peer-gateway' in each):
                    vpc['peer_gw'] = True
                if ('peer-keepalive destination' in each):
                    line = each.split()
                    vpc['pkl_dest'] = line[2]
                    vpc['pkl_vrf'] = 'management'
                    if ('source' in each):
                        vpc['pkl_src'] = line[4]
                        if ('vrf' in each):
                            vpc['pkl_vrf'] = line[6]
                    elif ('vrf' in each):
                        vpc['pkl_vrf'] = line[4]
    return vpc
