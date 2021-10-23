def response_to_hash(module, response):
    return {
        'name': response.get('name'),
        'labels': response.get('labels'),
    }