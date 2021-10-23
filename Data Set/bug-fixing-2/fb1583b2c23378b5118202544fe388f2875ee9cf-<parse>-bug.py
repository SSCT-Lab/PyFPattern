

def parse(self, data):
    parsed = list()
    values = None
    for line in data.split('\n'):
        if (not line):
            continue
        elif (line[0] == ' '):
            values += ('\n%s' % line)
        elif line.startswith('Interface'):
            if values:
                parsed.append(values)
            values = line
    return parsed
