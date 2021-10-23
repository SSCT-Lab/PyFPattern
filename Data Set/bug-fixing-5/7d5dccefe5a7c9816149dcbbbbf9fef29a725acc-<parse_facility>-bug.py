def parse_facility(line):
    match = re.search('logging facility (\\S+)', line, re.M)
    if match:
        facility = match.group(1)
    else:
        facility = 'local7'
    return facility