def check_interface(module, netcfg):
    config = str(netcfg)
    REGEX = re.compile('\\s+interface port-channel{0}*$'.format(module.params['group']), re.M)
    value = False
    try:
        if REGEX.search(config):
            value = True
    except TypeError:
        value = False
    return value