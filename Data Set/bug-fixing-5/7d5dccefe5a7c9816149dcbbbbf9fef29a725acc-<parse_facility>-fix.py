def parse_facility(line, dest):
    facility = None
    if (dest == 'facility'):
        match = re.search('logging facility (\\S+)', line, re.M)
        if match:
            facility = match.group(1)
    return facility