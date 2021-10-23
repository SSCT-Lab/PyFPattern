def read_interfaces_lines(module, line_strings):
    lines = []
    ifaces = {
        
    }
    currently_processing = None
    i = 0
    for line in line_strings:
        i += 1
        words = line.split()
        if (len(words) < 1):
            lines.append(lineDict(line))
            continue
        if (words[0][0] == '#'):
            lines.append(lineDict(line))
            continue
        if (words[0] == 'mapping'):
            lines.append(lineDict(line))
            currently_processing = 'MAPPING'
        elif (words[0] == 'source'):
            lines.append(lineDict(line))
            currently_processing = 'NONE'
        elif (words[0] == 'source-dir'):
            lines.append(lineDict(line))
            currently_processing = 'NONE'
        elif (words[0] == 'iface'):
            currif = {
                'pre-up': [],
                'up': [],
                'down': [],
                'post-up': [],
            }
            (iface_name, address_family_name, method_name) = words[1:4]
            if (len(words) != 4):
                module.fail_json(msg=('Incorrect number of parameters (%d) in line %d, must be exectly 3' % (len(words), i)))
                return (None, None)
            currif['address_family'] = address_family_name
            currif['method'] = method_name
            ifaces[iface_name] = currif
            lines.append({
                'line': line,
                'iface': iface_name,
                'line_type': 'iface',
                'params': currif,
            })
            currently_processing = 'IFACE'
        elif (words[0] == 'auto'):
            lines.append(lineDict(line))
            currently_processing = 'NONE'
        elif (words[0] == 'allow-'):
            lines.append(lineDict(line))
            currently_processing = 'NONE'
        elif (words[0] == 'no-auto-down'):
            lines.append(lineDict(line))
            currently_processing = 'NONE'
        elif (words[0] == 'no-scripts'):
            lines.append(lineDict(line))
            currently_processing = 'NONE'
        elif (currently_processing == 'IFACE'):
            option_name = words[0]
            value = getValueFromLine(line)
            lines.append(optionDict(line, iface_name, option_name, value))
            if (option_name in ['pre-up', 'up', 'down', 'post-up']):
                currif[option_name].append(value)
            else:
                currif[option_name] = value
        elif (currently_processing == 'MAPPING'):
            lines.append(lineDict(line))
        elif (currently_processing == 'NONE'):
            lines.append(lineDict(line))
        else:
            module.fail_json(msg=('misplaced option %s in line %d' % (line, i)))
            return (None, None)
    return (lines, ifaces)