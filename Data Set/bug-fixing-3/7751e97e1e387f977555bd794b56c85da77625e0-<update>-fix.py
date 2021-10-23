def update(module, link, fetch):
    auth = GcpSession(module, 'pubsub')
    params = {
        'updateMask': updateMask(resource_to_request(module), response_to_hash(module, fetch)),
    }
    request = resource_to_request(module)
    del request['name']
    return return_if_object(module, auth.patch(link, request, params=params))