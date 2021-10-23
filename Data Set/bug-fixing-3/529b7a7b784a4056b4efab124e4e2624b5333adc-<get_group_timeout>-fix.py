def get_group_timeout(config):
    match = re.search('  Group timeout configured: (\\S+)', config, re.M)
    if match:
        value = match.group(1)
    else:
        value = ''
    return value