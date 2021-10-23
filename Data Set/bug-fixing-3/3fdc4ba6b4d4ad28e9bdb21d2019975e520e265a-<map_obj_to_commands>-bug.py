def map_obj_to_commands(want, have):
    commands = list()
    for w in want:
        state = w['state']
        del w['state']
        for h in have:
            diff = list((set(w.items()) ^ set(h.items())))
            if (not diff):
                break
            elif ((len(diff) == 2) and (diff[0][0] == diff[1][0] == 'name') and ((not w['name']) or h['name'].startswith(w['name']))):
                break
        else:
            h = None
        command = 'ip route'
        prefix = w['prefix']
        mask = w['mask']
        vrf = w.get('vrf')
        if vrf:
            command = ' '.join((command, 'vrf', vrf, prefix, mask))
        else:
            command = ' '.join((command, prefix, mask))
        for key in ['interface', 'next_hop', 'admin_distance', 'tag', 'name', 'track']:
            if w.get(key):
                if ((key == 'name') and (len(w.get(key).split()) > 1)):
                    command = ' '.join((command, key, ('"%s"' % w.get(key))))
                elif (key in ('name', 'tag', 'track')):
                    command = ' '.join((command, key, w.get(key)))
                else:
                    command = ' '.join((command, w.get(key)))
        if ((state == 'absent') and h):
            commands.append(('no %s' % command))
        elif ((state == 'present') and (not h)):
            commands.append(command)
    return commands