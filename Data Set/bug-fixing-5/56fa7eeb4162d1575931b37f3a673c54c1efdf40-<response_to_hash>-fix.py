def response_to_hash(module, response):
    return {
        'affinityCookieTtlSec': response.get('affinityCookieTtlSec'),
        'backends': BackendServiceBackendsArray(response.get('backends', []), module).from_response(),
        'cdnPolicy': BackendServiceCdnPolicy(response.get('cdnPolicy', {
            
        }), module).from_response(),
        'connectionDraining': BackendServiceConnectionDraining(response.get('connectionDraining', {
            
        }), module).from_response(),
        'creationTimestamp': response.get('creationTimestamp'),
        'description': response.get('description'),
        'enableCDN': response.get('enableCDN'),
        'healthChecks': response.get('healthChecks'),
        'id': response.get('id'),
        'iap': BackendServiceIap(response.get('iap', {
            
        }), module).from_response(),
        'loadBalancingScheme': response.get('loadBalancingScheme'),
        'name': response.get('name'),
        'portName': response.get('portName'),
        'protocol': response.get('protocol'),
        'region': response.get('region'),
        'sessionAffinity': response.get('sessionAffinity'),
        'timeoutSec': response.get('timeoutSec'),
    }