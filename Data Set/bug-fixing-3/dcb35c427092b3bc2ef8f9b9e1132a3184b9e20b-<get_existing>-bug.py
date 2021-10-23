def get_existing(module, args):
    existing = {
        
    }
    netcfg = CustomNetworkConfig(indent=2, contents=get_config(module))
    parents = ['router ospf {0}'.format(module.params['ospf'])]
    if (module.params['vrf'] != 'default'):
        parents.append('vrf {0}'.format(module.params['vrf']))
    config = netcfg.get_section(parents)
    for arg in args:
        if (arg not in ['ospf', 'vrf']):
            existing[arg] = PARAM_TO_DEFAULT_KEYMAP.get(arg)
    if config:
        if (module.params['vrf'] == 'default'):
            splitted_config = config.splitlines()
            vrf_index = False
            for index in range(0, (len(splitted_config) - 1)):
                if ('vrf' in splitted_config[index].strip()):
                    vrf_index = index
                    break
            if vrf_index:
                config = '\n'.join(splitted_config[0:vrf_index])
        splitted_config = config.splitlines()
        for line in splitted_config:
            if ('passive' in line):
                existing['passive_interface'] = True
            elif ('router-id' in line):
                existing['router_id'] = re.search('router-id (\\S+)', line).group(1)
            elif ('metric' in line):
                existing['default_metric'] = re.search('default-metric (\\S+)', line).group(1)
            elif ('adjacency' in line):
                log = re.search('log-adjacency-changes(?: (\\S+))?', line).group(1)
                if log:
                    existing['log_adjacency'] = log
                else:
                    existing['log_adjacency'] = 'log'
            elif ('auto' in line):
                cost = re.search('auto-cost reference-bandwidth (\\d+) (\\S+)', line).group(1)
                if ('Gbps' in line):
                    cost *= 1000
                existing['auto_cost'] = str(cost)
            elif ('timers throttle lsa' in line):
                tmp = re.search('timers throttle lsa (\\S+) (\\S+) (\\S+)', line)
                existing['timer_throttle_lsa_start'] = tmp.group(1)
                existing['timer_throttle_lsa_hold'] = tmp.group(2)
                existing['timer_throttle_lsa_max'] = tmp.group(3)
            elif ('timers throttle spf' in line):
                tmp = re.search('timers throttle spf (\\S+) (\\S+) (\\S+)', line)
                existing['timer_throttle_spf_start'] = tmp.group(1)
                existing['timer_throttle_spf_hold'] = tmp.group(2)
                existing['timer_throttle_spf_max'] = tmp.group(3)
        existing['vrf'] = module.params['vrf']
        existing['ospf'] = module.params['ospf']
    return existing