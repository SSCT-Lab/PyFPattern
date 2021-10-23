def list_hosted_zones(client, module):
    params = dict()
    if module.params.get('max_items'):
        params['MaxItems'] = module.params.get('max_items')
    if module.params.get('next_marker'):
        params['Marker'] = module.params.get('next_marker')
    if module.params.get('delegation_set_id'):
        params['DelegationSetId'] = module.params.get('delegation_set_id')
    results = client.list_hosted_zones(**params)
    return results