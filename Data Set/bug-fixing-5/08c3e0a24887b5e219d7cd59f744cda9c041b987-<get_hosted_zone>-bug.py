def get_hosted_zone(client, module):
    params = dict()
    if module.params.get('hosted_zone_id'):
        params['Id'] = module.params.get('hosted_zone_id')
    else:
        module.fail_json(msg='Hosted Zone Id is required')
    results = client.get_hosted_zone(**params)
    return results