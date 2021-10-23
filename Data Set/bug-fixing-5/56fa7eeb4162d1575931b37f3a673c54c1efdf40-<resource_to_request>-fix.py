def resource_to_request(module):
    request = {
        'kind': 'compute#backendService',
        'affinityCookieTtlSec': module.params.get('affinity_cookie_ttl_sec'),
        'backends': BackendServiceBackendsArray(module.params.get('backends', []), module).to_request(),
        'cdnPolicy': BackendServiceCdnPolicy(module.params.get('cdn_policy', {
            
        }), module).to_request(),
        'connectionDraining': BackendServiceConnectionDraining(module.params.get('connection_draining', {
            
        }), module).to_request(),
        'description': module.params.get('description'),
        'enableCDN': module.params.get('enable_cdn'),
        'healthChecks': module.params.get('health_checks'),
        'iap': BackendServiceIap(module.params.get('iap', {
            
        }), module).to_request(),
        'loadBalancingScheme': module.params.get('load_balancing_scheme'),
        'name': module.params.get('name'),
        'portName': module.params.get('port_name'),
        'protocol': module.params.get('protocol'),
        'region': region_selflink(module.params.get('region'), module.params),
        'sessionAffinity': module.params.get('session_affinity'),
        'timeoutSec': module.params.get('timeout_sec'),
    }
    return_vals = {
        
    }
    for (k, v) in request.items():
        if v:
            return_vals[k] = v
    return return_vals