def get_group_timeout(config):
    command = 'ip igmp snooping group-timeout'
    REGEX = re.compile('(?:{0}\\s)(?P<value>.*)$'.format(command), re.M)
    value = ''
    if (command in config):
        value = REGEX.search(config).group('value')
    return value