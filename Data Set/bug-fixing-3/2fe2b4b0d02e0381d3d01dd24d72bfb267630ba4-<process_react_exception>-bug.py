@minified_error(vendor='react', mapping_url=REACT_MAPPING_URL, regex='Minified React error #(\\d+); visit https?://[^?]+\\?(\\S+)')
def process_react_exception(exc, match, mapping):
    (error_id, qs) = match.groups()
    msg_format = mapping.get(error_id)
    if (msg_format is None):
        return False
    arg_count = count_sprintf_parameters(msg_format)
    args = []
    for (k, v) in parse_qsl(qs, keep_blank_values=True):
        if (k == 'args[]'):
            args.append(v.decode('utf-8', 'replace'))
    args = tuple((args + (['<redacted>'] * (arg_count - len(args)))))[:arg_count]
    exc['value'] = (msg_format % args)
    return True