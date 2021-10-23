def record_sets_details(client, module):
    params = dict()
    if module.params.get('hosted_zone_id'):
        params['HostedZoneId'] = module.params.get('hosted_zone_id')
    else:
        module.fail_json(msg='Hosted Zone Id is required')
    if module.params.get('max_items'):
        params['MaxItems'] = module.params.get('max_items')
    if module.params.get('start_record_name'):
        params['StartRecordName'] = module.params.get('start_record_name')
    if (module.params.get('type') and (not module.params.get('start_record_name'))):
        module.fail_json(msg='start_record_name must be specified if type is set')
    elif module.params.get('type'):
        params['StartRecordType'] = module.params.get('type')
    return client.list_resource_record_sets(**params)