def sorted_allowed_list(allowed_list):
    'Sort allowed_list (output of format_allowed) by protocol and port.'
    allowed_by_protocol = sorted(allowed_list, key=(lambda x: x['IPProtocol']))
    return sorted(allowed_by_protocol, key=(lambda y: y['ports'].sort()))