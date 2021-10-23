def guess_format(config):
    try:
        json.loads(config)
        return 'json'
    except ValueError:
        pass
    try:
        ElementTree.fromstring(config)
        return 'xml'
    except ParseError:
        pass
    if (config.startswith('set') or config.startswith('delete')):
        return 'set'
    return 'text'