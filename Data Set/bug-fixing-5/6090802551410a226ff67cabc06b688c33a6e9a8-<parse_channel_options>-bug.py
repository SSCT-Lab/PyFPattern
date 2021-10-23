def parse_channel_options(module, output, channel):
    obj = {
        
    }
    group = channel['group']
    obj['group'] = group
    obj['min-links'] = parse_min_links(module, group)
    members = parse_members(output, group)
    obj['members'] = members
    for m in members:
        obj['mode'] = parse_mode(module, m)
    return obj