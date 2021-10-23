def map_config_to_obj(module):
    objs = list()
    output = run_commands(module, ['show port-channel summary | json'])[0]
    if (not output):
        return list()
    try:
        channels = output['TABLE_channel']['ROW_channel']
    except KeyError:
        return objs
    if channels:
        if isinstance(channels, list):
            for channel in channels:
                obj = parse_channel_options(module, output, channel)
                objs.append(obj)
        elif isinstance(channels, dict):
            obj = parse_channel_options(module, output, channels)
            objs.append(obj)
    return objs