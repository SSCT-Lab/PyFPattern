def get_network_command(existing, key, value):
    commands = []
    existing_networks = existing.get('networks', [])
    for inet in value:
        if (not isinstance(inet, list)):
            inet = [inet]
        if (inet not in existing_networks):
            if (len(inet) == 1):
                command = '{0} {1}'.format(key, inet[0])
            elif (len(inet) == 2):
                command = '{0} {1} route-map {2}'.format(key, inet[0], inet[1])
            if command:
                commands.append(command)
    for enet in existing_networks:
        if (enet not in value):
            if (len(enet) == 1):
                command = 'no {0} {1}'.format(key, enet[0])
            elif (len(enet) == 2):
                command = 'no {0} {1} route-map {2}'.format(key, enet[0], enet[1])
            if command:
                commands.append(command)
    return commands