def return_if_object(module, response, kind):
    if (response.status_code == 404):
        return None
    if (response.status_code == 204):
        return None
    try:
        module.raise_for_status(response)
        result = response.json()
    except getattr(json.decoder, 'JSONDecodeError', ValueError) as inst:
        module.fail_json(msg=('Invalid JSON response with error: %s' % inst))
    if navigate_hash(result, ['error', 'errors']):
        module.fail_json(msg=navigate_hash(result, ['error', 'errors']))
    return result