def parse_rpcs(module):
    items = list()
    for rpc in (module.params['rpcs'] or list()):
        parts = split(rpc)
        name = parts.pop(0)
        args = dict()
        for item in parts:
            (key, value) = item.split('=')
            if (str(value).upper() in ['TRUE', 'FALSE']):
                args[key] = bool(value)
            elif re.match('^[0-9]+$', value):
                args[key] = int(value)
            else:
                args[key] = str(value)
        display = (module.params['display'] or 'xml')
        if ((display == 'set') and (rpc != 'get-configuration')):
            module.fail_json(msg=("Invalid display option '%s' given for rpc '%s'" % ('set', name)))
        xattrs = {
            'format': display,
        }
        items.append({
            'name': name,
            'args': args,
            'xattrs': xattrs,
        })
    return items