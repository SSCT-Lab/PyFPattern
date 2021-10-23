def parse_lookup_source(config):
    match = re.search('ip domain lookup source-interface (\\S+)', config, re.M)
    if match:
        return match.group(1)