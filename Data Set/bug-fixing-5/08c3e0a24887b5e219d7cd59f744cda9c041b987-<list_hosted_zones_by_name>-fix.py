def list_hosted_zones_by_name(client, module):
    params = dict()
    if module.params.get('hosted_zone_id'):
        params['HostedZoneId'] = module.params.get('hosted_zone_id')
    if module.params.get('dns_name'):
        params['DNSName'] = module.params.get('dns_name')
    if module.params.get('max_items'):
        params['MaxItems'] = module.params.get('max_items')
    return client.list_hosted_zones_by_name(**params)