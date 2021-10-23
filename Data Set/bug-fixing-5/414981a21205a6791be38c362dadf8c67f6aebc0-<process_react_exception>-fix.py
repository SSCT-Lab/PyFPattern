@minified_error(vendor='react', mapping_url=REACT_MAPPING_URL, regex='Minified React error #(\\d+); visit https?://[^?]+\\?(\\S+)')
def process_react_exception(exc, match, mapping):
    (error_id, qs) = match.groups()
    msg_format = mapping.get(error_id)
    if (msg_format is None):
        return False
    args = []
    for (k, v) in parse_qsl(qs, keep_blank_values=True):
        if (k == 'args[]'):
            args.append(v)
    exc['value'] = (msg_format % tuple(args))
    return True