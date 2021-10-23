def get_inject_map_command(existing, key, value):
    commands = []
    existing_maps = existing.get('inject_map', [])
    for maps in value:
        if (not isinstance(maps, list)):
            maps = [maps]
        if (maps not in existing_maps):
            if (len(maps) == 2):
                command = 'inject-map {0} exist-map {1}'.format(maps[0], maps[1])
            elif (len(maps) == 3):
                command = 'inject-map {0} exist-map {1} copy-attributes'.format(maps[0], maps[1])
            commands.append(command)
    for emaps in existing_maps:
        if (emaps not in value):
            if (len(emaps) == 2):
                command = 'no inject-map {0} exist-map {1}'.format(emaps[0], emaps[1])
            elif (len(emaps) == 3):
                command = 'no inject-map {0} exist-map {1} copy-attributes'.format(emaps[0], emaps[1])
            commands.append(command)
    return commands