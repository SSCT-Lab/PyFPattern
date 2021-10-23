def get_members(channel):
    members = []
    if ('TABLE_member' in channel.keys()):
        interfaces = channel['TABLE_member']['ROW_member']
    else:
        return list()
    if isinstance(interfaces, dict):
        members.append(interfaces.get('port'))
    elif isinstance(interfaces, list):
        for i in interfaces:
            members.append(i.get('port'))
    return members