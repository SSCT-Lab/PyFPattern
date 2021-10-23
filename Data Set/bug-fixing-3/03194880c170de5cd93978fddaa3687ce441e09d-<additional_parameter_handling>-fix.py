def additional_parameter_handling(params):
    'Additional parameter validation and reformatting'
    params['b_src'] = to_bytes(params['src'], errors='surrogate_or_strict', nonstring='passthru')
    prev_state = get_state(to_bytes(params['path'], errors='surrogate_or_strict'))
    if (params['state'] is None):
        if (prev_state != 'absent'):
            params['state'] = prev_state
        elif params['recurse']:
            params['state'] = 'directory'
        else:
            params['state'] = 'file'
    if (params['recurse'] and (params['state'] != 'directory')):
        raise ParameterError(results={
            'msg': "recurse option requires state to be 'directory'",
            'path': params['path'],
        })