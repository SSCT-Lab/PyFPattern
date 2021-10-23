def addOptionAfterLine(option, value, iface, lines, last_line_dict, iface_options):
    last_line = last_line_dict['line']
    prefix_start = last_line.find(last_line.split()[0])
    suffix_start = (last_line.rfind(last_line.split()[(- 1)]) + len(last_line.split()[(- 1)]))
    prefix = last_line[:prefix_start]
    if (len(iface_options) < 1):
        prefix += '    '
    line = ((prefix + ('%s %s' % (option, value))) + last_line[suffix_start:])
    option_dict = optionDict(line, iface, option, value)
    index = (len(lines) - lines[::(- 1)].index(last_line_dict))
    lines.insert(index, option_dict)
    return lines