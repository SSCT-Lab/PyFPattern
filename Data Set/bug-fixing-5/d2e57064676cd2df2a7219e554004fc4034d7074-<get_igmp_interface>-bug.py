def get_igmp_interface(module, interface):
    command = 'show ip igmp interface {0}'.format(interface)
    igmp = {
        
    }
    key_map = {
        'IGMPVersion': 'version',
        'ConfiguredStartupQueryInterval': 'startup_query_interval',
        'StartupQueryCount': 'startup_query_count',
        'RobustnessVariable': 'robustness',
        'ConfiguredQuerierTimeout': 'querier_timeout',
        'ConfiguredMaxResponseTime': 'query_mrt',
        'ConfiguredQueryInterval': 'query_interval',
        'LastMemberMTR': 'last_member_qrt',
        'LastMemberQueryCount': 'last_member_query_count',
        'ConfiguredGroupTimeout': 'group_timeout',
    }
    body = execute_show_command(command, module)[0]
    if body:
        resource = body['TABLE_vrf']['ROW_vrf']['TABLE_if']['ROW_if']
        igmp = apply_key_map(key_map, resource)
        report_llg = str(resource['ReportingForLinkLocal']).lower()
        if (report_llg == 'true'):
            igmp['report_llg'] = True
        elif (report_llg == 'false'):
            igmp['report_llg'] = False
        immediate_leave = str(resource['ImmediateLeave']).lower()
        if ((immediate_leave == 'en') or (immediate_leave == 'true')):
            igmp['immediate_leave'] = True
        elif ((immediate_leave == 'dis') or (immediate_leave == 'false')):
            igmp['immediate_leave'] = False
    command = 'show run interface {0} | inc oif'.format(interface)
    body = execute_show_command(command, module, command_type='cli_show_ascii')[0]
    staticoif = []
    if body:
        split_body = body.split('\n')
        route_map_regex = '.*ip igmp static-oif route-map\\s+(?P<route_map>\\S+).*'
        prefix_source_regex = '.*ip igmp static-oif\\s+(?P<prefix>((\\d+.){3}\\d+))(\\ssource\\s(?P<source>\\S+))?.*'
        for line in split_body:
            temp = {
                
            }
            try:
                match_route_map = re.match(route_map_regex, line, re.DOTALL)
                route_map = match_route_map.groupdict()['route_map']
            except AttributeError:
                route_map = ''
            try:
                match_prefix_source = re.match(prefix_source_regex, line, re.DOTALL)
                prefix_source_group = match_prefix_source.groupdict()
                prefix = prefix_source_group['prefix']
                source = prefix_source_group['source']
            except AttributeError:
                prefix = ''
                source = ''
            if route_map:
                temp['route_map'] = route_map
            if prefix:
                temp['prefix'] = prefix
            if source:
                temp['source'] = source
            if temp:
                staticoif.append(temp)
    igmp['oif_routemap'] = None
    igmp['oif_prefix_source'] = []
    if staticoif:
        if ((len(staticoif) == 1) and staticoif[0].get('route_map')):
            igmp['oif_routemap'] = staticoif[0]['route_map']
        else:
            igmp['oif_prefix_source'] = staticoif
    return igmp