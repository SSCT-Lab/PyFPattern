def config_igmp_interface(delta, existing, existing_oif_prefix_source):
    CMDS = {
        'version': 'ip igmp version {0}',
        'startup_query_interval': 'ip igmp startup-query-interval {0}',
        'startup_query_count': 'ip igmp startup-query-count {0}',
        'robustness': 'ip igmp robustness-variable {0}',
        'querier_timeout': 'ip igmp querier-timeout {0}',
        'query_mrt': 'ip igmp query-max-response-time {0}',
        'query_interval': 'ip igmp query-interval {0}',
        'last_member_qrt': 'ip igmp last-member-query-response-time {0}',
        'last_member_query_count': 'ip igmp last-member-query-count {0}',
        'group_timeout': 'ip igmp group-timeout {0}',
        'report_llg': 'ip igmp report-link-local-groups',
        'immediate_leave': 'ip igmp immediate-leave',
        'oif_prefix_source': 'ip igmp static-oif {0} source {1} ',
        'oif_routemap': 'ip igmp static-oif route-map {0}',
        'oif_prefix': 'ip igmp static-oif {0}',
    }
    commands = []
    command = None
    def_vals = get_igmp_interface_defaults()
    for (key, value) in delta.items():
        if ((key == 'oif_ps') and (value != 'default')):
            for each in value:
                if (each in existing_oif_prefix_source):
                    existing_oif_prefix_source.remove(each)
                else:
                    pf = each['prefix']
                    src = ''
                    if ('source' in each.keys()):
                        src = each['source']
                    if src:
                        commands.append(CMDS.get('oif_prefix_source').format(pf, src))
                    else:
                        commands.append(CMDS.get('oif_prefix').format(pf))
            if existing_oif_prefix_source:
                for each in existing_oif_prefix_source:
                    pf = each['prefix']
                    src = ''
                    if ('source' in each.keys()):
                        src = each['source']
                    if src:
                        commands.append(('no ' + CMDS.get('oif_prefix_source').format(pf, src)))
                    else:
                        commands.append(('no ' + CMDS.get('oif_prefix').format(pf)))
        elif (key == 'oif_routemap'):
            if (value == 'default'):
                if existing.get(key):
                    command = ('no ' + CMDS.get(key).format(existing.get(key)))
            else:
                command = CMDS.get(key).format(value)
        elif value:
            if (value == 'default'):
                if (def_vals.get(key) != existing.get(key)):
                    command = CMDS.get(key).format(def_vals.get(key))
            else:
                command = CMDS.get(key).format(value)
        elif (not value):
            command = 'no {0}'.format(CMDS.get(key).format(value))
        if command:
            if (command not in commands):
                commands.append(command)
        command = None
    return commands