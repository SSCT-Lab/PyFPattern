def parse_version(self, data):
    facts = dict()
    match = re.search('HW Version(.+)\\s(\\d+)', data)
    (temp, temp_next) = data.split('---- ----------- ----------- -------------- --------------')
    for en in temp_next.splitlines():
        if (en == ''):
            continue
        match_image = re.search('^(\\S+)\\s+(\\S+)\\s+(\\S+)\\s+(\\S+)', en)
        version = match_image.group(4)
        facts['Version'] = list()
        fact = dict()
        fact['HW Version'] = match.group(2)
        fact['SW Version'] = match_image.group(4)
        facts['Version'].append(fact)
    return facts