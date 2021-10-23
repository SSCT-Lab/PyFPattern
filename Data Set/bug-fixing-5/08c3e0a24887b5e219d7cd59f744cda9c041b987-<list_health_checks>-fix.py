def list_health_checks(client, module):
    params = dict()
    if module.params.get('max_items'):
        params['MaxItems'] = module.params.get('max_items')
    if module.params.get('next_marker'):
        params['Marker'] = module.params.get('next_marker')
    return client.list_health_checks(**params)