def format_allowed_section(allowed):
    'Format each section of the allowed list'
    if (allowed.count(':') == 0):
        protocol = allowed
        ports = []
    elif (allowed.count(':') == 1):
        (protocol, ports) = allowed.split(':')
    else:
        return []
    if ports.count(','):
        ports = ports.split(',')
    elif ports:
        ports = [ports]
    return_val = {
        'IPProtocol': protocol,
    }
    if ports:
        return_val['ports'] = ports
    return return_val