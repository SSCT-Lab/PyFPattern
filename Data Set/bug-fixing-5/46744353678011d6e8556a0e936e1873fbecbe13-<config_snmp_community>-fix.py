def config_snmp_community(delta, community):
    CMDS = {
        'group': 'snmp-server community {0} group {group}',
        'acl': 'snmp-server community {0} use-acl {acl}',
        'no_acl': 'no snmp-server community {0} use-acl {no_acl}',
    }
    commands = []
    for k in delta.keys():
        cmd = CMDS.get(k).format(community, **delta)
        if cmd:
            if ('group' in cmd):
                commands.insert(0, cmd)
            else:
                commands.append(cmd)
            cmd = None
    return commands