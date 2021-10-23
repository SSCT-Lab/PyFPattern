

def core(module):
    region = module.params['region']
    wished_server = {
        'state': module.params['state'],
        'image': module.params['image'],
        'name': module.params['name'],
        'commercial_type': module.params['commercial_type'],
        'enable_ipv6': module.params['enable_ipv6'],
        'dynamic_ip_required': module.params['dynamic_ip_required'],
        'tags': module.params['tags'],
        'organization': module.params['organization'],
    }
    module.params['api_url'] = SCALEWAY_LOCATION[region]['api_endpoint']
    compute_api = Scaleway(module=module)
    ip_payload = public_ip_payload(compute_api=compute_api, public_ip=module.params['public_ip'])
    wished_server.update(ip_payload)
    (changed, summary) = state_strategy[wished_server['state']](compute_api=compute_api, wished_server=wished_server)
    module.exit_json(changed=changed, msg=summary)
