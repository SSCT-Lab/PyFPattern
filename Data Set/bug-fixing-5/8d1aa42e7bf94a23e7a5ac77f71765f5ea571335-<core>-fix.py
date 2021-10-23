def core(module):
    region = module.params['region']
    wished_load_balancer = {
        'state': module.params['state'],
        'name': module.params['name'],
        'description': module.params['description'],
        'tags': module.params['tags'],
        'organization_id': module.params['organization_id'],
    }
    module.params['api_url'] = SCALEWAY_ENDPOINT
    api = Scaleway(module=module)
    api.api_path = ('lb/v1/regions/%s/lbs' % region)
    (changed, summary) = state_strategy[wished_load_balancer['state']](api=api, wished_lb=wished_load_balancer)
    module.exit_json(changed=changed, scaleway_lb=summary)