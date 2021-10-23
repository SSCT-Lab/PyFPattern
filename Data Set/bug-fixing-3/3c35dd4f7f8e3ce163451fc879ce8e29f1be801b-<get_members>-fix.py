def get_members(channel):
    members = []
    if ('TABLE_member' in channel.keys()):
        interfaces = channel['TABLE_member']['ROW_member']
    else:
        return list()
    if isinstance(interfaces, dict):
        members.append(normalize_interface(interfaces.get('port')))
    elif isinstance(interfaces, list):
        for i in interfaces:
            members.append(normalize_interface(i.get('port')))
    return members