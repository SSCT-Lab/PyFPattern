def response_to_hash(module, response):
    return {
        'name': module.params.get('name'),
        'labels': response.get('labels'),
    }