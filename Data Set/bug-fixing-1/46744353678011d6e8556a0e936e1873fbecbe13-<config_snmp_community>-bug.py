

def config_snmp_community(delta, community):
    CMDS = {
        'group': 'snmp-server community {0} group {group}',
        'acl': 'snmp-server community {0} use-acl {acl}',
        'no_acl': 'no snmp-server community {0} use-acl {no_acl}',
    }
    commands = []
    for (k, v) in delta.items():
        cmd = CMDS.get(k).format(community, **delta)
        if cmd:
            commands.append(cmd)
            cmd = None
    return commands
