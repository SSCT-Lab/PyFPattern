def parse_interfaces(self, data):
    parsed = list()
    for line in data.split('\n'):
        if (len(line) == 0):
            continue
        else:
            line = line.strip()
            match = re.match('^([0-9]+)', line)
            if match:
                key = match.group(1)
                parsed.append(line)
            match = re.match('^(INT+)', line)
            if match:
                key = match.group(1)
                parsed.append(line)
            match = re.match('^(EXT+)', line)
            if match:
                key = match.group(1)
                parsed.append(line)
            match = re.match('^(MGT+)', line)
            if match:
                key = match.group(1)
                parsed.append(line)
    return parsed