def get_resource_tags(client, module):
    params = dict()
    if module.params.get('resource_id'):
        params['ResourceIds'] = module.params.get('resource_id')
    else:
        module.fail_json(msg='resource_id or resource_ids is required')
    if (module.params.get('query') == 'health_check'):
        params['ResourceType'] = 'healthcheck'
    else:
        params['ResourceType'] = 'hostedzone'
    results = client.list_tags_for_resources(**params)
    return results