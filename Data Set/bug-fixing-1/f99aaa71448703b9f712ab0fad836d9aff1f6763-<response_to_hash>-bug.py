

def response_to_hash(module, response):
    return {
        'name': response.get('name'),
        'type': response.get('type'),
        'ttl': response.get('ttl'),
        'rrdatas': response.get('target'),
    }
