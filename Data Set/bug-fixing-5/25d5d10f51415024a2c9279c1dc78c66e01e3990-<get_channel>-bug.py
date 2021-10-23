def get_channel(module, config, group):
    match = re.findall('interface (\\S+)', config, re.M)
    if (not match):
        return {
            
        }
    channel = {
        
    }
    for item in set(match):
        member = item
        channel['mode'] = parse_mode(module, config, group, member)
        channel['members'] = parse_members(module, config, group)
    return channel